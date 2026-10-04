"""Dialogue manager: turns the trained intent model + agent configuration into a
working voice-receptionist conversation (booking, cancellation, Q&A, escalation).

State machine:  idle → booking_service → booking_date → booking_time
             → booking_name → booking_phone → booking_confirm → done
(with cancel_lookup as a side branch).
"""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple

from .train import match_faq, predict_intent

CONFIDENCE_THRESHOLD = 0.30
FAQ_THRESHOLD = 0.40

_WEEKDAYS = {w.lower(): i for i, w in enumerate(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])}
_MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}
for _alias, _m in [("jan", 1), ("feb", 2), ("mar", 3), ("apr", 4), ("jun", 6), ("jul", 7),
                   ("aug", 8), ("sep", 9), ("sept", 9), ("oct", 10), ("nov", 11), ("dec", 12)]:
    _MONTHS[_alias] = _m


class Conversation:
    def __init__(self) -> None:
        self.state = "idle"
        self.slots: Dict[str, Any] = {}
        self.strikes = 0
        self.transcript: List[Dict[str, str]] = []
        self.done = False
        self.intents_seen: List[str] = []


# ---------------------------------------------------------------------------
# Entity extractors
# ---------------------------------------------------------------------------

def extract_service(text: str, services: List[Dict[str, Any]]) -> Optional[str]:
    low = text.lower()
    for svc in services:
        if svc["name"].lower() in low:
            return svc["name"]
    for svc in services:  # partial word match, longest first
        words = [w for w in re.split(r"\W+", svc["name"].lower()) if len(w) > 3]
        if any(w in low for w in sorted(words, key=len, reverse=True)[:1]):
            return svc["name"]
    return None


def extract_date(text: str, today: Optional[date] = None) -> Optional[date]:
    today = today or date.today()
    low = text.lower()

    if "day after tomorrow" in low:
        return today + timedelta(days=2)
    if "tomorrow" in low:
        return today + timedelta(days=1)
    if "today" in low or "tonight" in low:
        return today
    m = re.search(r"in (\d+) days?", low)
    if m:
        return today + timedelta(days=int(m.group(1)))

    for name, idx in _WEEKDAYS.items():
        if re.search(rf"\b{name}\b", low):
            delta = (idx - today.weekday()) % 7
            if delta == 0 or "next" in low:
                delta += 7
            return today + timedelta(days=delta)

    for name, month in _MONTHS.items():
        m = re.search(rf"\b{name}\s+(\d{{1,2}})(?:st|nd|rd|th)?\b", low)
        if m:
            day = int(m.group(1))
            year = today.year
            try:
                parsed = date(year, month, day)
            except ValueError:
                return None
            if parsed < today:
                parsed = date(year + 1, month, day)
            return parsed

    m = re.search(r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b", text)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", text)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        year = int(m.group(3)) if m.group(3) else today.year
        year += 2000 if year < 100 else 0
        try:
            parsed = date(year, month, day)
        except ValueError:
            return None
        if parsed < today and not m.group(3):
            parsed = date(year + 1, month, day)
        return parsed
    if "next week" in low:
        return today + timedelta(days=7)
    return None


def extract_time(text: str, require_marker: bool = False) -> Optional[str]:
    """Parse a time. With require_marker=True, only accept explicit times
    (meridiem, colon, or time-of-day words) — avoids misfiring on dates."""
    low = text.lower()
    if "noon" in low or "midday" in low or "mid day" in low:
        return "12:00"
    if re.search(r"\bmorning\b", low):
        return "10:00"
    if re.search(r"\bafternoon\b", low):
        return "14:00"
    if re.search(r"\bevening\b", low):
        return "17:00"
    m = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?\b", low)
    if not m:
        return None
    if require_marker and not (m.group(3) or m.group(2)):
        return None
    hour, minute, meridiem = int(m.group(1)), int(m.group(2) or 0), m.group(3)
    if hour > 24 or minute > 59:
        return None
    if meridiem:
        meridiem = meridiem.replace(".", "")
        if meridiem == "pm" and hour < 12:
            hour += 12
        if meridiem == "am" and hour == 12:
            hour = 0
    elif hour <= 7:
        hour += 12  # "let's do 3" in a business context means 3 PM
    return f"{hour:02d}:{minute:02d}"


def extract_phone(text: str) -> Optional[str]:
    m = re.search(r"(\+?\d[\d\s\-().]{6,}\d)", text)
    if not m:
        return None
    digits = re.sub(r"\D", "", m.group(1))
    return digits if 7 <= len(digits) <= 15 else None


def extract_name(text: str) -> Optional[str]:
    m = re.search(r"(?:my name is|this is|i am|i'm|it's)\s+([A-Za-z][A-Za-z\s.'-]{1,40})",
                  text, re.IGNORECASE)
    if m:
        return " ".join(w.capitalize() for w in m.group(1).strip().split())
    cleaned = text.strip()
    words = cleaned.split()
    if 1 <= len(words) <= 3 and all(re.fullmatch(r"[A-Za-z.'-]+", w) for w in words):
        low = cleaned.lower()
        if low not in {"yes", "no", "ok", "okay", "sure", "hi", "hello", "bye"}:
            return " ".join(w.capitalize() for w in words)
    return None


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------

def _parse_hhmm(value: str) -> Optional[int]:
    try:
        hour, minute = value.split(":")
        return int(hour) * 60 + int(minute)
    except (ValueError, AttributeError):
        return None


def day_hours(cfg: Dict[str, Any], day: date) -> Optional[Tuple[str, str]]:
    info = cfg.get("hours", {}).get(day.strftime("%A"), {})
    if not info or info.get("closed"):
        return None
    return info.get("open", "09:00"), info.get("close", "17:00")


def available_slots(cfg: Dict[str, Any], day: date, duration_min: int,
                    existing: List[Dict[str, Any]]) -> List[str]:
    hours = day_hours(cfg, day)
    if not hours:
        return []
    open_min, close_min = _parse_hhmm(hours[0]), _parse_hhmm(hours[1])
    if open_min is None or close_min is None:
        return []

    busy: List[Tuple[int, int]] = []
    for appt in existing:
        if appt.get("date") != day.isoformat() or appt.get("status") == "cancelled":
            continue
        start = _parse_hhmm(appt.get("time", ""))
        if start is None:
            continue
        busy.append((start, start + int(appt.get("duration_min", 30))))

    slots = []
    step = 30
    cursor = open_min
    while cursor + duration_min <= close_min:
        overlap = any(cursor < end and cursor + duration_min > start for start, end in busy)
        if not overlap:
            slots.append(f"{cursor // 60:02d}:{cursor % 60:02d}")
        cursor += step
    return slots


# ---------------------------------------------------------------------------
# Dialogue manager
# ---------------------------------------------------------------------------

class DialogueManager:
    def __init__(self, cfg: Dict[str, Any], model_bundle=None):
        self.cfg = cfg
        self.bundle = model_bundle
        self.services = cfg.get("services", [])

    # -- helpers -----------------------------------------------------------

    def _faq_answer(self, text: str) -> Optional[str]:
        answer, _ = match_faq(self.bundle, text, self.cfg.get("faqs", []), FAQ_THRESHOLD)
        return answer

    def _service_summary(self) -> str:
        names = [s["name"] for s in self.services]
        if not names:
            return "general appointments"
        if len(names) <= 3:
            return ", ".join(names)
        return ", ".join(names[:3]) + f", and {len(names) - 3} more"

    def _price_answer(self, text: str) -> str:
        svc_name = extract_service(text, self.services)
        if svc_name:
            svc = next((s for s in self.services if s["name"] == svc_name), None)
            price = svc.get("price", 0) if svc else 0
            return (f"A {svc_name} takes about {svc['duration']} minutes"
                    + (f" and costs ${price}." if price else "."))
        priced = [f"{s['name']} ${s['price']}" for s in self.services if s.get("price")]
        if priced:
            return "Here's a quick price list: " + "; ".join(priced[:4]) + "."
        return "There's no charge listed for our standard appointments."

    def _hours_answer(self) -> str:
        parts = []
        for day, info in self.cfg.get("hours", {}).items():
            if not info.get("closed"):
                parts.append(f"{day[:3]} {info.get('open','09:00')}–{info.get('close','17:00')}")
        return ("We're open " + ", ".join(parts) + ".") if parts else \
            "Our hours aren't published yet — a teammate will confirm when we call back."

    def _escalation_answer(self) -> str:
        esc = self.cfg.get("escalation", {})
        if esc.get("mode") == "transfer" and esc.get("phone"):
            return (f"Of course — I'm noting this down and our team at {esc['phone']} "
                    "will take it from here. Is there anything else before I go?")
        return ("No problem. I'll take a message and a member of the team will call you "
                "back shortly. Can I get your name and number?")

    def _validate_booking_date(self, day: date) -> Optional[str]:
        """Return an error string if the date can't be booked."""
        if day < date.today():
            return "That date has already passed. Which future date works for you?"
        window = int(self.cfg.get("booking_window_days", 30))
        if day > date.today() + timedelta(days=window):
            return f"We only book up to {window} days out. Could you pick a closer date?"
        if day_hours(self.cfg, day) is None:
            return (f"We're closed on {day.strftime('%A')}s. "
                    "Would another day this week work?")
        return None

    def _time_within_hours(self, day: date, hhmm: str) -> bool:
        hours = day_hours(self.cfg, day)
        if not hours:
            return False
        mins = _parse_hhmm(hhmm)
        if mins is None:
            return False
        open_min, close_min = _parse_hhmm(hours[0]), _parse_hhmm(hours[1])
        duration = self._slot_duration()
        return open_min is not None and close_min is not None and \
            open_min <= mins and mins + duration <= close_min

    def _slot_duration(self) -> int:
        svc = self._current_service()
        return int(svc.get("duration", 30)) if svc else 30

    def _current_service(self) -> Optional[Dict[str, Any]]:
        name = self._slots.get("service")
        return next((s for s in self.services if s["name"] == name), None)

    # -- main entry ---------------------------------------------------------

    _slots: Dict[str, Any]  # per-handle call view of the conversation slots

    def opening(self) -> str:
        return self.cfg.get("greeting") or (
            f"Thank you for calling {self.cfg.get('business_name', 'us')}, "
            f"this is {self.cfg.get('agent_name', 'your AI receptionist')}. How can I help you today?")

    def handle(self, conv: Conversation, user_text: str,
               appointments_provider: Callable[[], List[Dict[str, Any]]]
               ) -> Tuple[str, List[Dict[str, Any]]]:
        """Process one caller turn. Returns (reply, events)."""
        self._slots = conv.slots
        events: List[Dict[str, Any]] = []
        intent, conf = predict_intent(self.bundle, user_text) if self.bundle else ("unknown", 0.0)
        if conf >= CONFIDENCE_THRESHOLD and intent != "unknown":
            conv.intents_seen.append(intent)
        text = user_text.strip()

        state = conv.state
        reply = ""

        # --- mid-booking state machine -------------------------------------
        if state.startswith("booking_") and state != "booking_service":
            reply, events = self._continue_booking(conv, text, appointments_provider)
            if reply is not None:
                return self._finish(conv, reply, events)

        # --- faq short-circuit ---------------------------------------------
        faq = self._faq_answer(text)
        if faq and intent in ("ask_services", "ask_hours", "ask_location", "ask_price", "unknown"):
            return self._finish(conv, faq + " Anything else I can help with?", events)

        # --- intent routing -------------------------------------------------
        if intent == "greeting":
            reply = f"Hello! You've reached {self.cfg.get('business_name','us')}. How can I help?"
        elif intent == "goodbye":
            reply = self._closing()
            events.append({"type": "end_call"})
        elif intent == "book_appointment":
            conv.state = "booking_service"
            reply = self._start_booking(conv, text)
        elif intent == "reschedule_appointment":
            reply = ("I can help with that. Rescheduling over the phone is quickest with a "
                     "teammate — otherwise tell me your name and I'll note the request.")
            conv.state = "cancel_lookup"
            self._slots["lookup_mode"] = "reschedule"
        elif intent == "cancel_appointment":
            conv.state = "cancel_lookup"
            self._slots["lookup_mode"] = "cancel"
            reply = "I'm sorry to hear that. May I have the name and phone number on the booking?"
        elif intent == "check_availability":
            reply = self._availability_reply(text, appointments_provider)
        elif intent == "ask_services":
            reply = f"We offer {self._service_summary()}. Would you like to book one?"
        elif intent == "ask_price":
            reply = self._price_answer(text)
        elif intent == "ask_hours":
            reply = self._hours_answer()
        elif intent == "ask_location":
            reply = (f"We're at {self.cfg.get('address')}." if self.cfg.get("address")
                     else "I'll have the team text you our address. Anything else?")
        elif intent == "ask_human":
            reply = self._escalation_answer()
            if self.cfg.get("escalation", {}).get("mode") == "transfer":
                events.append({"type": "escalate"})
        elif intent == "affirm":
            reply = "Great — what would you like me to do for you?"
        elif intent == "deny":
            reply = "No problem. Is there anything else I can help with?"
        else:
            conv.strikes += 1
            fallback = self.cfg.get("fallback") or (
                "I'm sorry, I didn't quite catch that. I can help with bookings, "
                "cancellations, and questions about our services and hours.")
            reply = fallback
            if conv.strikes >= 3:
                reply += " " + self._escalation_answer()
                conv.strikes = 0

        if state == "cancel_lookup" and conv.state == "cancel_lookup":
            reply, events = self._handle_cancel_lookup(conv, text, appointments_provider)

        return self._finish(conv, reply, events)

    # -- booking flow --------------------------------------------------------

    def _start_booking(self, conv: Conversation, text: str) -> str:
        svc = extract_service(text, self.services)
        day = extract_date(text)
        time_str = extract_time(text)
        if svc:
            conv.slots["service"] = svc
        if day and self._validate_booking_date(day) is None:
            conv.slots["date"] = day.isoformat()
        if time_str:
            conv.slots["time"] = time_str

        if not conv.slots.get("service"):
            conv.state = "booking_service"
            return f"Happy to help with a booking. Which service — {self._service_summary()}?"
        err = self._validate_booking_date(day) if day and not conv.slots.get("date") else None
        conv.state = "booking_date"
        if not conv.slots.get("date"):
            return f"A {conv.slots['service']} — sure. What date works for you?"
        conv.state = "booking_time"
        if err:
            return err
        return f"Got it, {conv.slots['service']} on {self._fmt_date(conv.slots['date'])}. What time?"

    def _continue_booking(self, conv: Conversation, text: str,
                          appointments_provider: Callable[[], List[Dict[str, Any]]]):
        state, slots = conv.state, conv.slots
        low = text.lower()

        if any(w in low for w in ("cancel", "never mind", "forget it", "stop")) and "booking" in state:
            conv.state = "idle"
            conv.slots = {}
            return "No problem, I've cancelled that request. Anything else I can do?", []

        if state == "booking_service":
            svc = extract_service(text, self.services)
            if not svc:
                return (f"I didn't catch that. We offer {self._service_summary()} — "
                        "which one would you like?"), []
            slots["service"] = svc
            conv.state = "booking_date"
            return f"Great choice. What date works for your {svc}?", []

        if state == "booking_date":
            day = extract_date(text)
            time_str = extract_time(text, require_marker=True)
            if not day:
                return "Which date would you like? For example, 'tomorrow' or 'Friday'.", []
            err = self._validate_booking_date(day)
            if err:
                return err, []
            slots["date"] = day.isoformat()
            if time_str and self._time_within_hours(day, time_str):
                slots["time"] = time_str
                conv.state = "booking_name"
                return (f"{self._fmt_date(slots['date'])} at {self._fmt_time(time_str)} — "
                        "locked in. May I have your name?"), []
            conv.state = "booking_time"
            slots_hint = available_slots(self.cfg, day, self._slot_duration(),
                                         appointments_provider())[:4]
            hint = f" Open times include {', '.join(slots_hint)}." if slots_hint else ""
            return f"{self._fmt_date(slots['date'])} — noted. What time suits you?{hint}", []

        if state == "booking_time":
            time_str = extract_time(text)
            if not time_str:
                return "What time should I put you down for? For example, '2:30 PM'.", []
            day = datetime.strptime(slots["date"], "%Y-%m-%d").date()
            if not self._time_within_hours(day, time_str):
                hours = day_hours(self.cfg, day)
                return (f"We're open {hours[0]} to {hours[1]} that day. "
                        "Pick a time within those hours?"), []
            existing = appointments_provider()
            if time_str not in available_slots(self.cfg, day, self._slot_duration(), existing):
                alts = available_slots(self.cfg, day, self._slot_duration(), existing)[:3]
                if alts:
                    return (f"That time is already taken. I could offer "
                            f"{', '.join(alts)} instead?"), []
                return "That day is fully booked. Would another day work?", []
            slots["time"] = time_str
            conv.state = "booking_name"
            return "Perfect. May I have your name?", []

        if state == "booking_name":
            name = extract_name(text)
            if not name:
                return "I didn't catch the name — could you say it again?", []
            slots["name"] = name
            conv.state = "booking_phone"
            return f"Thanks, {name.split()[0]}. And the best phone number to reach you?", []

        if state == "booking_phone":
            phone = extract_phone(text)
            if not phone:
                return "Could you give me a phone number with at least 7 digits?", []
            slots["phone"] = phone
            conv.state = "booking_confirm"
            svc = slots["service"]
            return (f"Just to confirm: {svc} on {self._fmt_date(slots['date'])} at "
                    f"{self._fmt_time(slots['time'])} for {slots['name']} (phone {phone}). "
                    "Shall I book it?"), []

        if state == "booking_confirm":
            intent, conf = predict_intent(self.bundle, text) if self.bundle else ("unknown", 0)
            if intent == "affirm" or re.search(r"\b(yes|yeah|confirm|book it|sure|correct)\b", low):
                events = [{
                    "type": "book_appointment",
                    "data": {
                        "service": slots["service"],
                        "date": slots["date"],
                        "time": slots["time"],
                        "duration_min": self._slot_duration(),
                        "customer_name": slots["name"],
                        "customer_phone": slots["phone"],
                    },
                }]
                conv.state = "done"
                conv.done = True
                return (f"You're all set, {slots['name'].split()[0]}! Your {slots['service']} is booked for "
                        f"{self._fmt_date(slots['date'])} at {self._fmt_time(slots['time'])}. "
                        "We look forward to seeing you. Goodbye!"), events + [{"type": "end_call"}]
            if intent == "deny" or "no" in low:
                conv.state = "idle"
                conv.slots = {}
                return "Alright, I've scrapped that. Would you like to pick a different time?", []
            return "Should I go ahead and book it? Just say yes or no.", []

        return None, []  # fall through to routing

    def _handle_cancel_lookup(self, conv: Conversation, text: str,
                              appointments_provider):
        name = extract_name(text)
        phone = extract_phone(text)
        if not (name or phone):
            return "I need the name or phone number on the booking to find it.", []

        matches = []
        for appt in appointments_provider():
            if appt.get("status") == "cancelled":
                continue
            if phone and appt.get("customer_phone", "") == phone:
                matches.append(appt)
            elif name and name.lower() in appt.get("customer_name", "").lower():
                matches.append(appt)

        mode = conv.slots.get("lookup_mode", "cancel")
        conv.state = "idle"
        conv.slots = {}
        if not matches:
            return ("I couldn't find an upcoming booking under those details. "
                    "The team will follow up to double-check."), []
        target = sorted(matches, key=lambda a: (a.get("date", ""), a.get("time", "")))[0]
        if mode == "cancel":
            return (f"Done — I've cancelled the {target.get('service')} on "
                    f"{self._fmt_date(target.get('date',''))} at {self._fmt_time(target.get('time',''))} "
                    f"for {target.get('customer_name')}. Anything else?"), \
                [{"type": "cancel_appointment", "data": {"id": target["id"]}}]
        return (f"I found your {target.get('service')} on {self._fmt_date(target.get('date',''))}. "
                "Our team will call you to choose the new time — reschedules are confirmed "
                "by a person for accuracy."), []

    def _availability_reply(self, text: str, appointments_provider) -> str:
        day = extract_date(text) or (date.today() + timedelta(days=1))
        err = self._validate_booking_date(day)
        if err:
            return err
        slots = available_slots(self.cfg, day, 30, appointments_provider())
        if not slots:
            return f"We're fully booked on {self._fmt_date(day.isoformat())}. Try another day?"
        preview = ", ".join(self._fmt_time(s) for s in slots[:5])
        more = f" and {len(slots) - 5} more" if len(slots) > 5 else ""
        return f"On {self._fmt_date(day.isoformat())} we have {preview}{more}. Shall I book one?"

    # -- utilities -----------------------------------------------------------

    def _closing(self) -> str:
        return self.cfg.get("closing") or (
            f"Thank you for calling {self.cfg.get('business_name','us')}. Have a great day!")

    @staticmethod
    def _fmt_date(iso: str) -> str:
        try:
            return datetime.strptime(iso, "%Y-%m-%d").strftime("%A, %B %-d")
        except (ValueError, TypeError):
            return iso

    @staticmethod
    def _fmt_time(hhmm: str) -> str:
        try:
            return datetime.strptime(hhmm, "%H:%M").strftime("%-I:%M %p")
        except (ValueError, TypeError):
            return hhmm

    @staticmethod
    def _finish(conv: Conversation, reply: str,
                events: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
        if conv.done and conv.state != "done":
            conv.done = False
        return reply, events
