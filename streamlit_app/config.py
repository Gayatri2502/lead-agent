"""Application configuration: constants, role presets, and local Firebase config persistence."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

APP_NAME = "VoiceDesk AI"
APP_TAGLINE = "AI Voice Receptionist Platform"
APP_ICON = "🎙️"
APP_URL_DEFAULT = "http://localhost:8501"

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIREBASE_CONFIG_PATH = os.path.join(ROOT_DIR, ".firebase_config.json")
MODELS_DIR = os.path.join(ROOT_DIR, "models")

# ---------------------------------------------------------------------------
# Firebase local config (web API key etc. — not secret, identifies the project)
# ---------------------------------------------------------------------------

def load_firebase_config() -> Optional[Dict[str, str]]:
    """Load Firebase web config saved locally. Returns None if not configured."""
    if not os.path.exists(FIREBASE_CONFIG_PATH):
        return None
    try:
        with open(FIREBASE_CONFIG_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if data.get("api_key") and data.get("project_id"):
            return data
        return None
    except (json.JSONDecodeError, OSError):
        return None


def save_firebase_config(data: Dict[str, str]) -> None:
    with open(FIREBASE_CONFIG_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    try:
        os.chmod(FIREBASE_CONFIG_PATH, 0o600)
    except OSError:
        pass


def clear_firebase_config() -> None:
    if os.path.exists(FIREBASE_CONFIG_PATH):
        os.remove(FIREBASE_CONFIG_PATH)


# ---------------------------------------------------------------------------
# Receptionist role presets — drive onboarding defaults and ML training data
# ---------------------------------------------------------------------------

ROLE_PRESETS: Dict[str, Dict[str, Any]] = {
    "Dental Clinic": {
        "industry": "Healthcare",
        "agent_name": "Riley",
        "services": [
            {"name": "Dental Cleaning", "duration": 45, "price": 120},
            {"name": "Check-up & Exam", "duration": 30, "price": 95},
            {"name": "Teeth Whitening", "duration": 60, "price": 350},
            {"name": "Filling", "duration": 60, "price": 220},
            {"name": "Emergency Visit", "duration": 30, "price": 150},
        ],
        "faqs": [
            {"q": "Do you accept insurance?", "a": "Yes, we accept most major dental insurance plans. Bring your card to your first visit and we will verify coverage."},
            {"q": "How often should I get a cleaning?", "a": "We recommend a professional cleaning every six months."},
        ],
        "vocabulary": ["tooth", "teeth", "cleaning", "cavity", "filling", "whitening", "dentist", "gums", "braces"],
    },
    "Medical Practice": {
        "industry": "Healthcare",
        "agent_name": "Jordan",
        "services": [
            {"name": "General Consultation", "duration": 30, "price": 150},
            {"name": "Annual Physical", "duration": 60, "price": 250},
            {"name": "Follow-up Visit", "duration": 20, "price": 90},
            {"name": "Vaccination", "duration": 15, "price": 45},
        ],
        "faqs": [
            {"q": "Do I need to fast before a blood test?", "a": "For most blood panels we recommend fasting for 8 to 12 hours. We will confirm when you book."},
            {"q": "Can I get a same-day appointment?", "a": "We keep a few same-day slots for urgent needs. Call early in the morning for the best chance."},
        ],
        "vocabulary": ["doctor", "physician", "symptoms", "prescription", "referral", "lab", "physical", "vaccine"],
    },
    "Hair Salon & Spa": {
        "industry": "Beauty & Wellness",
        "agent_name": "Bella",
        "services": [
            {"name": "Haircut", "duration": 45, "price": 60},
            {"name": "Hair Coloring", "duration": 120, "price": 180},
            {"name": "Manicure", "duration": 40, "price": 45},
            {"name": "Facial", "duration": 60, "price": 110},
            {"name": "Massage", "duration": 60, "price": 130},
        ],
        "faqs": [
            {"q": "Should I wash my hair before coloring?", "a": "Come with hair that was washed a day before — slightly lived-in hair holds color better."},
            {"q": "What is your cancellation policy?", "a": "We kindly ask for at least 24 hours notice to reschedule or cancel."},
        ],
        "vocabulary": ["haircut", "color", "highlights", "trim", "blowout", "manicure", "pedicure", "facial", "massage", "stylist"],
    },
    "Restaurant": {
        "industry": "Hospitality",
        "agent_name": "Marco",
        "services": [
            {"name": "Table for 2", "duration": 90, "price": 0},
            {"name": "Table for 4", "duration": 90, "price": 0},
            {"name": "Large Party (6+)", "duration": 120, "price": 0},
            {"name": "Private Dining Room", "duration": 180, "price": 0},
        ],
        "faqs": [
            {"q": "Do you have vegetarian options?", "a": "Yes, our menu includes vegetarian, vegan and gluten-free dishes."},
            {"q": "Is parking available?", "a": "We offer validated parking in the garage next door after 5 PM."},
        ],
        "vocabulary": ["table", "reservation", "dinner", "lunch", "menu", "party", "dining", "patio"],
    },
    "Real Estate Agency": {
        "industry": "Real Estate",
        "agent_name": "Sophia",
        "services": [
            {"name": "Property Viewing", "duration": 45, "price": 0},
            {"name": "Buyer Consultation", "duration": 60, "price": 0},
            {"name": "Listing Consultation", "duration": 60, "price": 0},
            {"name": "Valuation Visit", "duration": 45, "price": 0},
        ],
        "faqs": [
            {"q": "Do you handle rentals as well?", "a": "Yes, we manage both sales and rental listings across the metro area."},
            {"q": "What areas do you cover?", "a": "We cover the greater metro area and surrounding suburbs."},
        ],
        "vocabulary": ["property", "house", "apartment", "viewing", "listing", "mortgage", "agent", "open house"],
    },
    "Law Firm": {
        "industry": "Legal",
        "agent_name": "Alexandra",
        "services": [
            {"name": "Initial Consultation", "duration": 60, "price": 200},
            {"name": "Contract Review", "duration": 45, "price": 300},
            {"name": "Case Follow-up", "duration": 30, "price": 150},
        ],
        "faqs": [
            {"q": "Is the first consultation confidential?", "a": "Yes, everything you share with us is protected by attorney-client privilege from the first conversation."},
            {"q": "What documents should I bring?", "a": "Bring any contracts, correspondence, or court documents related to your matter, plus a photo ID."},
        ],
        "vocabulary": ["attorney", "lawyer", "case", "contract", "consultation", "litigation", "estate", "custody"],
    },
    "Fitness Studio": {
        "industry": "Fitness",
        "agent_name": "Kai",
        "services": [
            {"name": "Personal Training", "duration": 60, "price": 80},
            {"name": "Yoga Class", "duration": 60, "price": 25},
            {"name": "HIIT Class", "duration": 45, "price": 25},
            {"name": "Intro Assessment", "duration": 30, "price": 0},
        ],
        "faqs": [
            {"q": "Do I need to bring my own mat?", "a": "Mats and towels are provided free of charge, but you are welcome to bring your own."},
            {"q": "Is there a free trial?", "a": "Yes — your first group class is free. Just book an Intro Assessment to get started."},
        ],
        "vocabulary": ["class", "training", "trainer", "yoga", "hiit", "membership", "workout", "session"],
    },
    "Auto Repair Shop": {
        "industry": "Automotive",
        "agent_name": "Sam",
        "services": [
            {"name": "Oil Change", "duration": 30, "price": 60},
            {"name": "Brake Inspection", "duration": 45, "price": 50},
            {"name": "Diagnostic Check", "duration": 60, "price": 120},
            {"name": "Tire Rotation", "duration": 30, "price": 40},
        ],
        "faqs": [
            {"q": "Do I need an appointment for an oil change?", "a": "Appointments are recommended but we take walk-ins for oil changes when the bays are free."},
            {"q": "Do you offer a shuttle service?", "a": "Yes, we offer a complimentary shuttle within 5 miles of the shop."},
        ],
        "vocabulary": ["car", "vehicle", "oil", "brakes", "tires", "engine", "diagnostic", "inspection"],
    },
    "Veterinary Clinic": {
        "industry": "Veterinary",
        "agent_name": "Luna",
        "services": [
            {"name": "Wellness Exam", "duration": 30, "price": 85},
            {"name": "Vaccination", "duration": 20, "price": 45},
            {"name": "Dental Cleaning", "duration": 90, "price": 300},
            {"name": "Nail Trim", "duration": 15, "price": 25},
        ],
        "faqs": [
            {"q": "Do you treat exotic pets?", "a": "Yes, we see birds, rabbits and most small exotics. Please mention the species when booking."},
            {"q": "What should I bring to the first visit?", "a": "Please bring any previous medical records and a list of current medications for your pet."},
        ],
        "vocabulary": ["pet", "dog", "cat", "vet", "vaccine", "exam", "puppy", "kitten"],
    },
    "Custom Business": {
        "industry": "General",
        "agent_name": "Ava",
        "services": [{"name": "Appointment", "duration": 30, "price": 0}],
        "faqs": [],
        "vocabulary": ["appointment", "booking", "service", "schedule"],
    },
}

ROLE_NAMES = list(ROLE_PRESETS.keys())

TONES = ["Professional", "Friendly", "Warm", "Energetic", "Calm"]
LANGUAGES = ["English", "Spanish", "French", "German", "Hindi", "Portuguese"]
VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
TIMEZONES = [
    "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
    "America/Phoenix", "America/Anchorage", "Pacific/Honolulu", "Europe/London",
    "Europe/Berlin", "Europe/Paris", "Asia/Dubai", "Asia/Kolkata", "Asia/Singapore",
    "Asia/Tokyo", "Australia/Sydney",
]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

DEFAULT_HOURS: Dict[str, Dict[str, Any]] = {
    day: {"closed": False, "open": "09:00", "close": "17:00"} for day in WEEKDAYS
}
DEFAULT_HOURS["Saturday"] = {"closed": False, "open": "10:00", "close": "14:00"}
DEFAULT_HOURS["Sunday"] = {"closed": True, "open": "10:00", "close": "14:00"}

APPOINTMENT_STATUSES = ["scheduled", "confirmed", "completed", "cancelled"]

# ---------------------------------------------------------------------------
# System prompt builder (stored in Firestore; consumed by telephony backends)
# ---------------------------------------------------------------------------

def build_system_prompt(cfg: Dict[str, Any]) -> str:
    services = ", ".join(
        f"{s['name']} ({s['duration']} min" + (f", ${s['price']}" if s.get("price") else "") + ")"
        for s in cfg.get("services", [])
    ) or "general appointments"
    hours_lines = []
    for day in WEEKDAYS:
        h = cfg.get("hours", {}).get(day, {})
        if h.get("closed"):
            hours_lines.append(f"  {day}: Closed")
        else:
            hours_lines.append(f"  {day}: {h.get('open', '09:00')} - {h.get('close', '17:00')}")
    faqs = "\n".join(f"  Q: {f['q']}\n  A: {f['a']}" for f in cfg.get("faqs", [])) or "  (none provided)"
    esc = cfg.get("escalation", {})
    if esc.get("mode") == "transfer":
        esc_text = f"Transfer the call to {esc.get('phone', 'the business line')}."
    elif esc.get("mode") == "message":
        esc_text = "Take a detailed message and assure the caller a human will call back."
    else:
        esc_text = "Politely explain limits and offer to book a callback appointment."

    return f"""You are {cfg.get('agent_name', 'Ava')}, the AI voice receptionist for {cfg.get('business_name', 'the business')} ({cfg.get('role', 'business')}, {cfg.get('industry', 'General')} industry).

PERSONALITY
- Tone: {cfg.get('tone', 'Professional')}. Language: {cfg.get('language', 'English')}.
- Keep spoken replies under 2 sentences unless the caller asks for detail.
- Never invent prices, hours or services. Use only the facts below.

BUSINESS FACTS
- Address: {cfg.get('address', 'not provided')}
- Phone: {cfg.get('phone', 'not provided')}
- Email: {cfg.get('email', 'not provided')}
- Timezone: {cfg.get('timezone', 'America/New_York')}

HOURS
{chr(10).join(hours_lines)}

SERVICES
{services}

POLICIES & FAQs
{faqs}

BOOKING RULES
- Book, reschedule and cancel appointments. Always confirm service, date, time, name and phone before finalizing.
- Do not book when the business is closed or beyond {cfg.get('booking_window_days', 30)} days out.
- If the caller asks for a human or you cannot help: {esc_text}

CUSTOM INSTRUCTIONS
{cfg.get('custom_instructions', '(none)')}

GREETING
{cfg.get('greeting', '')}

FALLBACK
{cfg.get('fallback', '')}
""".strip()
