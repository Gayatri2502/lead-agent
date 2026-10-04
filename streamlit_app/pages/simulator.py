"""Simulator: live test calls against the trained receptionist.

Bookings/cancellations made here are real — they are written to Firestore and
show up in Appointments, Customers, Calls and Dashboard.
"""
from __future__ import annotations

from datetime import datetime, date
from typing import Any, Dict

import streamlit as st

from .. import state, theme
from ..ml.dialogue import Conversation, DialogueManager
from ..ml.train import load_model


def _manager(cfg: Dict[str, Any]) -> DialogueManager:
    return DialogueManager(cfg, load_model(state.current_user()["uid"]))


def _reset(cfg: Dict[str, Any]) -> None:
    conv = Conversation()
    greeting = _manager(cfg).opening()
    st.session_state["sim_conv"] = conv
    st.session_state["sim_started_at"] = datetime.now()
    st.session_state["sim_messages"] = [{"speaker": "agent", "text": greeting}]
    st.session_state["sim_ended"] = False
    st.session_state["sim_outcome"] = "info"
    st.session_state["sim_saved"] = False


def _upsert_customer(name: str, phone: str) -> str:
    customers = state.load_customers()
    existing = next((c for c in customers if phone and c.get("phone") == phone), None)
    now = datetime.now().isoformat(timespec="seconds")
    if existing:
        state.upsert("customers", existing["id"],
                     {**existing, "name": existing.get("name") or name,
                      "last_seen": now})
        return existing["id"]
    doc = state.insert("customers", {
        "name": name, "phone": phone, "email": "", "notes": "Captured by AI receptionist",
        "tags": ["phone-booking"], "created_at": now, "last_seen": now,
    })
    return doc["id"]


def _process_events(conv: Conversation, events) -> None:
    for event in events:
        etype = event.get("type")
        if etype == "book_appointment":
            d = event["data"]
            start = f"{d['date']}T{d['time']}:00"
            cust_id = _upsert_customer(d["customer_name"], d["customer_phone"])
            state.insert("appointments", {
                "customer_id": cust_id,
                "customer_name": d["customer_name"],
                "customer_phone": d["customer_phone"],
                "customer_email": "",
                "service": d["service"],
                "duration_min": d["duration_min"],
                "date": d["date"],
                "time": d["time"],
                "start_iso": start,
                "status": "confirmed",
                "notes": "Booked by AI receptionist (simulator call)",
                "source": "simulator",
                "created_at": datetime.now().isoformat(timespec="seconds"),
            })
            st.session_state["sim_outcome"] = "booked"
        elif etype == "cancel_appointment":
            appts = state.load_appointments()
            target = next((a for a in appts if a.get("id") == event["data"]["id"]), None)
            if target:
                state.upsert("appointments", target["id"], {**target, "status": "cancelled"})
            st.session_state["sim_outcome"] = "cancelled"
        elif etype == "escalate":
            if st.session_state["sim_outcome"] == "info":
                st.session_state["sim_outcome"] = "escalated"
        elif etype == "end_call":
            st.session_state["sim_ended"] = True


def _save_call(cfg: Dict[str, Any]) -> None:
    conv: Conversation = st.session_state["sim_conv"]
    messages = st.session_state["sim_messages"]
    started = st.session_state["sim_started_at"]
    duration = int((datetime.now() - started).total_seconds())
    slots = conv.slots
    state.insert("calls", {
        "customer_name": slots.get("name", ""),
        "customer_phone": slots.get("phone", ""),
        "direction": "inbound",
        "source": "simulator",
        "started_at": started.isoformat(timespec="seconds"),
        "date": date.today().isoformat(),
        "duration_sec": duration,
        "intents": list(dict.fromkeys(conv.intents_seen)),
        "outcome": st.session_state.get("sim_outcome", "info"),
        "summary": f"Simulated call handled by {cfg.get('agent_name', 'the receptionist')}: "
                   f"{st.session_state.get('sim_outcome', 'info').title()} outcome.",
        "transcript": [
            {"speaker": m["speaker"], "text": m["text"],
             "time": m.get("time", "")} for m in messages
        ],
    })
    st.session_state["sim_saved"] = True


def render(cfg: Dict[str, Any]) -> None:
    theme.page_header("Simulator",
                      f"Place a test call to {cfg.get('agent_name', 'your receptionist')}. "
                      "Type what a caller would say.")

    if not load_model(state.current_user()["uid"]):
        theme.empty_state("🧠", "Model not trained yet",
                          "Train the receptionist on the AI Training page before taking calls.")
        if st.button("Go to AI Training", type="primary"):
            state.navigate("AI Training")
            st.rerun()
        return

    if "sim_conv" not in st.session_state:
        _reset(cfg)
    conv: Conversation = st.session_state["sim_conv"]

    # ---- conversation window ----------------------------------------------
    with st.container(border=True):
        for msg in st.session_state["sim_messages"]:
            if msg["speaker"] == "agent":
                with st.chat_message("assistant", avatar="🎙️"):
                    st.markdown(msg["text"])
            else:
                with st.chat_message("user", avatar="🧑"):
                    st.markdown(msg["text"])

        if st.session_state.get("sim_ended"):
            if not st.session_state.get("sim_saved"):
                _save_call(cfg)
                st.toast("Call saved to Firebase.", icon="☎️")
            st.info(f"📴 Call ended — outcome: "
                    f"**{st.session_state.get('sim_outcome', 'info').title()}**. "
                    "The full transcript is on the Calls page.", icon=None)

    # ---- controls ----------------------------------------------------------
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.caption("Try: *“I'd like to book a {svc} tomorrow at 3pm”*".format(
        svc=(cfg.get("services") or [{}])[0].get("name", "appointment").lower()))
    c2.button("🔁  New call", use_container_width=True,
              on_click=lambda: _reset(cfg))
    if c3.button("⏹️  End & save call", use_container_width=True,
                 disabled=st.session_state.get("sim_ended", False)):
        st.session_state["sim_ended"] = True
        st.rerun()

    prompt = st.chat_input(
        "Speak as the caller…",
        disabled=st.session_state.get("sim_ended", False))
    if prompt:
        now = datetime.now().strftime("%-I:%M %p")
        st.session_state["sim_messages"].append(
            {"speaker": "caller", "text": prompt, "time": now})
        manager = _manager(cfg)
        reply, events = manager.handle(conv, prompt, state.load_appointments)
        st.session_state["sim_messages"].append(
            {"speaker": "agent", "text": reply, "time": datetime.now().strftime("%-I:%M %p")})
        _process_events(conv, events)
        st.rerun()
