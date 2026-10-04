"""Receptionist setup wizard — the page shown before the dashboard.

The persona defined here is pushed to Firestore and used to (re)train the
intent model, so the receptionist actually behaves like the designated role.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import streamlit as st

from . import state, theme
from .config import (DEFAULT_HOURS, LANGUAGES, ROLE_NAMES, ROLE_PRESETS,
                     TIMEZONES, TONES, VOICES, WEEKDAYS, build_system_prompt)

_SERVICE_COLS = ["name", "duration", "price"]
_FAQ_COLS = ["q", "a"]


# ---------------------------------------------------------------------------
# Session-backed editors (data_editor outside of forms)
# ---------------------------------------------------------------------------

def _editor_rows(base_key: str, editor_key: str, columns: List[str]) -> List[Dict[str, Any]]:
    """Materialize a data_editor's change log into concrete rows."""
    changes = st.session_state.get(editor_key) or {}
    rows = [dict(r) for r in st.session_state.get(base_key, [])]
    for idx, patch in changes.get("edited_rows", {}).items():
        i = int(idx)
        if 0 <= i < len(rows):
            rows[i].update(patch)
    for idx in sorted(changes.get("deleted_rows", []), reverse=True):
        if 0 <= int(idx) < len(rows):
            rows.pop(int(idx))
    for row in changes.get("added_rows", []):
        rows.append({c: row.get(c, "") for c in columns})
    return [r for r in rows if any(str(r.get(c, "")).strip() for c in columns)]


def _apply_preset(role: str) -> None:
    preset = ROLE_PRESETS[role]
    st.session_state["ob_defaults"] = {
        "role": role,
        "agent_name": preset["agent_name"],
        "industry": preset["industry"],
        "vocabulary": preset["vocabulary"],
    }
    st.session_state["ob_services_base"] = [dict(s) for s in preset["services"]]
    st.session_state["ob_faqs_base"] = [dict(f) for f in preset["faqs"]]
    for key in ("ob_services_editor", "ob_faqs_editor"):
        if key in st.session_state:
            del st.session_state[key]


def _init_state(existing: Dict[str, Any] | None) -> None:
    if "ob_defaults" not in st.session_state:
        if existing:
            st.session_state["ob_defaults"] = {
                "role": existing.get("role", "Custom Business"),
                "agent_name": existing.get("agent_name", "Ava"),
                "industry": existing.get("industry", "General"),
                "vocabulary": existing.get("vocabulary", []),
            }
            st.session_state["ob_services_base"] = [
                {"name": s.get("name", ""), "duration": int(s.get("duration", 30)),
                 "price": float(s.get("price", 0))}
                for s in existing.get("services", []) if s.get("name")]
            st.session_state["ob_faqs_base"] = [
                {"q": f.get("q", ""), "a": f.get("a", "")}
                for f in existing.get("faqs", []) if f.get("q")]
        else:
            _apply_preset(ROLE_NAMES[0])
    st.session_state.setdefault("ob_services_base", [])
    st.session_state.setdefault("ob_faqs_base", [])


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------

def render_onboarding(existing: Dict[str, Any] | None) -> None:
    _init_state(existing)
    defaults = st.session_state["ob_defaults"]

    theme.page_header(
        "Design your AI receptionist" if not existing else "Receptionist setup",
        "Define who answers your calls — the role, voice, services and rules. "
        "Saving pushes this profile to Firebase and trains the receptionist model.",
    )

    # ---- role picker (live) ----------------------------------------------
    top = st.columns([2, 2, 1])
    with top[0]:
        role = st.selectbox(
            "What kind of receptionist do you need?",
            ROLE_NAMES,
            index=ROLE_NAMES.index(defaults["role"]) if defaults["role"] in ROLE_NAMES else len(ROLE_NAMES) - 1,
            help="Presets load realistic services, vocabulary and FAQs for that business type.",
        )
    if role != defaults.get("role"):
        _apply_preset(role)
        st.session_state["ob_defaults_role_applied"] = role
        st.rerun()

    with top[1]:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.caption("Pick a preset, then customize every field below.")
    with top[2]:
        if not existing:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            st.info("Step 1 of 1")

    defaults = st.session_state["ob_defaults"]  # refresh after potential rerun

    # ---- services & FAQs editors (live, form-free) ------------------------
    with st.container(border=True):
        st.markdown("**Services callers can book**")
        st.caption("Add, edit or remove rows. These feed the booking flow, pricing answers and model training.")
        st.data_editor(
            st.session_state["ob_services_base"],
            key="ob_services_editor",
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "name": st.column_config.TextColumn("Service", required=True, width="medium"),
                "duration": st.column_config.NumberColumn("Duration (min)", min_value=5, max_value=480, step=5, required=True),
                "price": st.column_config.NumberColumn("Price ($)", min_value=0, step=5, format="$%d"),
            },
        )

    with st.container(border=True):
        st.markdown("**Knowledge base — questions callers ask**")
        st.caption("The receptionist answers these verbatim. They also become training examples.")
        st.data_editor(
            st.session_state["ob_faqs_base"],
            key="ob_faqs_editor",
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "q": st.column_config.TextColumn("Caller question", required=True, width="medium"),
                "a": st.column_config.TextColumn("Receptionist answer", required=True, width="large"),
            },
        )

    services = [
        {"name": str(r["name"]).strip(),
         "duration": int(r["duration"] or 30),
         "price": float(r["price"] or 0)}
        for r in _editor_rows("ob_services_base", "ob_services_editor", _SERVICE_COLS)
        if str(r.get("name", "")).strip()
    ]
    faqs = [
        {"q": str(r["q"]).strip(), "a": str(r["a"]).strip()}
        for r in _editor_rows("ob_faqs_base", "ob_faqs_editor", _FAQ_COLS)
        if str(r.get("q", "")).strip()
    ]

    # ---- main form ---------------------------------------------------------
    with st.form("onboarding_form"):
        st.markdown("#### Persona")
        c1, c2, c3 = st.columns(3)
        agent_name = c1.text_input("Receptionist name", value=defaults.get("agent_name", "Ava"),
                                   help="How the agent introduces itself.")
        business_name = c2.text_input("Business name", value=(existing or {}).get("business_name", ""),
                                      placeholder="Bright Smile Dental")
        industry = c3.text_input("Industry", value=defaults.get("industry", "General"))

        c1, c2, c3 = st.columns(3)
        tone = c1.selectbox("Tone of voice", TONES,
                            index=TONES.index((existing or {}).get("tone", TONES[1]))
                            if (existing or {}).get("tone") in TONES else 1)
        language = c2.selectbox("Language", LANGUAGES, index=0)
        voice = c3.selectbox("Voice", VOICES,
                             index=VOICES.index((existing or {}).get("voice", "nova"))
                             if (existing or {}).get("voice") in VOICES else 4)

        st.markdown("#### Contact & location")
        c1, c2, c3 = st.columns(3)
        phone = c1.text_input("Business phone", value=(existing or {}).get("phone", ""),
                              placeholder="+1 555 123 4567")
        email = c2.text_input("Business email", value=(existing or {}).get("email", ""))
        timezone = c3.selectbox("Timezone", TIMEZONES,
                                index=TIMEZONES.index((existing or {}).get("timezone", TIMEZONES[0]))
                                if (existing or {}).get("timezone") in TIMEZONES else 0)
        address = st.text_input("Street address", value=(existing or {}).get("address", ""),
                                placeholder="118 Harbor Ave, Springfield")

        st.markdown("#### Business hours")
        existing_hours = (existing or {}).get("hours", {})
        hours: Dict[str, Dict[str, Any]] = {}
        for day in WEEKDAYS:
            dflt = existing_hours.get(day, DEFAULT_HOURS[day])
            c1, c2, c3, c4 = st.columns([1.4, 1, 1, 3])
            c1.markdown(f"<div style='padding-top:8px;font-weight:600;font-size:13.5px;'>{day}</div>",
                        unsafe_allow_html=True)
            closed = c2.checkbox("Closed", value=bool(dflt.get("closed")), key=f"ob_closed_{day}")
            if not closed:
                h_open = _hhmm_obj(dflt.get("open", "09:00"))
                h_close = _hhmm_obj(dflt.get("close", "17:00"))
                open_t = c3.time_input("Open", value=h_open, key=f"ob_open_{day}",
                                       label_visibility="collapsed")
                close_t = c4.time_input("Close", value=h_close, key=f"ob_close_{day}",
                                        label_visibility="collapsed")
                hours[day] = {"closed": False,
                              "open": open_t.strftime("%H:%M"),
                              "close": close_t.strftime("%H:%M")}
            else:
                hours[day] = {"closed": True, "open": dflt.get("open", "09:00"),
                              "close": dflt.get("close", "17:00")}

        st.markdown("#### Conversation design")
        greeting = st.text_area(
            "Greeting (first thing callers hear)",
            value=(existing or {}).get("greeting",
                f"Thank you for calling {business_name or 'us'}, this is "
                f"{agent_name or 'your AI receptionist'}. How can I help you today?"),
            height=70)
        fallback = st.text_area(
            "Fallback (when the caller can't be understood)",
            value=(existing or {}).get("fallback",
                "I'm sorry, I didn't quite catch that. I can help with bookings, "
                "cancellations, and questions about our services and hours."),
            height=70)

        c1, c2 = st.columns(2)
        esc_mode = c1.selectbox(
            "When a caller needs a human",
            ["transfer", "message", "none"],
            format_func=lambda m: {
                "transfer": "Transfer the call to my team",
                "message": "Take a message for a callback",
                "none": "Handle it without escalation",
            }[m],
            index=["transfer", "message", "none"].index(
                (existing or {}).get("escalation", {}).get("mode", "message")),
        )
        esc_phone = c2.text_input("Escalation phone (for transfers)",
                                  value=(existing or {}).get("escalation", {}).get("phone", ""))
        booking_window = st.slider("How far ahead can callers book? (days)",
                                   min_value=7, max_value=120,
                                   value=int((existing or {}).get("booking_window_days", 30)))
        custom_instructions = st.text_area(
            "Custom instructions for the model (optional)",
            value=(existing or {}).get("custom_instructions", ""),
            placeholder="e.g. Always ask new patients if they have insurance. Never quote exact surgery prices.",
            height=80)

        submitted = st.form_submit_button(
            "Save & train my receptionist" if not existing else "Save changes & retrain",
            use_container_width=True, type="primary")

    # ---- save --------------------------------------------------------------
    if not submitted:
        return

    errors = []
    if not business_name.strip():
        errors.append("Business name is required.")
    if not agent_name.strip():
        errors.append("Receptionist name is required.")
    if not services:
        errors.append("Add at least one bookable service.")
    for svc in services:
        if svc["duration"] <= 0:
            errors.append(f"Service '{svc['name']}' needs a duration of at least 5 minutes.")
    if esc_mode == "transfer" and not esc_phone.strip():
        errors.append("Add an escalation phone number, or choose a different escalation mode.")
    if errors:
        for e in errors:
            st.error(e)
        return

    config = {
        "role": role,
        "agent_name": agent_name.strip(),
        "business_name": business_name.strip(),
        "industry": industry.strip() or "General",
        "tone": tone,
        "language": language,
        "voice": voice,
        "phone": phone.strip(),
        "email": email.strip(),
        "address": address.strip(),
        "timezone": timezone,
        "hours": hours,
        "services": services,
        "faqs": faqs,
        "greeting": greeting.strip(),
        "fallback": fallback.strip(),
        "escalation": {"mode": esc_mode, "phone": esc_phone.strip()},
        "booking_window_days": booking_window,
        "custom_instructions": custom_instructions.strip(),
        "vocabulary": defaults.get("vocabulary", []),
        "onboarding_complete": True,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    config["system_prompt"] = build_system_prompt(config)

    with st.status("Deploying your receptionist…", expanded=True) as status:
        st.write("Saving profile to Firebase…")
        try:
            state.save_agent_config(config)
        except Exception as exc:
            status.update(label="Save failed", state="error")
            st.error(str(exc))
            return

        st.write("Generating training data from your configuration…")
        from .ml.train import train_receptionist
        meta = train_receptionist(config, state.current_user()["uid"])

        st.write("Uploading training report to Firebase…")
        state.insert("trainings", meta)
        status.update(
            label=f"Receptionist trained — {meta['accuracy']}% intent accuracy ({meta['samples']} samples)",
            state="complete")

    st.success("Your AI receptionist is live. Open the Simulator to test it, or the Dashboard to see your workspace.")
    if not existing:
        st.session_state.pop("ob_defaults", None)
        state.navigate("Dashboard")
    st.balloons()


def _hhmm_obj(value: str):
    try:
        return datetime.strptime(value, "%H:%M").time()
    except (ValueError, TypeError):
        return datetime.strptime("09:00", "%H:%M").time()
