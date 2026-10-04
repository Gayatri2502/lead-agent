"""Appointments: full CRUD backed by Firestore."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

from .. import state, theme
from ..config import APPOINTMENT_STATUSES


def _appt_label(a: Dict[str, Any]) -> str:
    return (f"{a.get('date', '')} {a.get('time', '')} — "
            f"{a.get('customer_name', 'Unknown')} · {a.get('service', '')}")


def _save(appointment_id: Optional[str], cfg: Dict[str, Any]) -> None:
    """Form-submit handler shared by create and edit."""
    prefix = "new" if appointment_id is None else f"edit_{appointment_id}"
    customer_mode = st.session_state[f"{prefix}_cust_mode"]
    if customer_mode == "Existing customer":
        cust_id = st.session_state[f"{prefix}_cust_id"]
        customers = state.load_customers()
        cust = next((c for c in customers if c["id"] == cust_id), None)
        name = cust.get("name", "") if cust else ""
        phone = cust.get("phone", "") if cust else ""
        email = cust.get("email", "") if cust else ""
    else:
        name = st.session_state[f"{prefix}_name"].strip()
        phone = st.session_state[f"{prefix}_phone"].strip()
        email = st.session_state[f"{prefix}_email"].strip()
        cust_id = ""

    service_name = st.session_state[f"{prefix}_service"]
    service = next((s for s in cfg.get("services", []) if s["name"] == service_name), {})
    appt_date = st.session_state[f"{prefix}_date"]
    appt_time = st.session_state[f"{prefix}_time"]

    if not name:
        st.error("A customer name is required.")
        return

    payload = {
        "customer_id": cust_id,
        "customer_name": name,
        "customer_phone": phone,
        "customer_email": email,
        "service": service_name,
        "duration_min": int(service.get("duration", 30)),
        "date": appt_date.isoformat(),
        "time": appt_time.strftime("%H:%M"),
        "start_iso": f"{appt_date.isoformat()}T{appt_time.strftime('%H:%M')}:00",
        "status": st.session_state.get(f"{prefix}_status", "scheduled"),
        "notes": st.session_state.get(f"{prefix}_notes", "").strip(),
        "source": st.session_state.get(f"{prefix}_source", "manual"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }

    if appointment_id:
        state.upsert("appointments", appointment_id, payload)
        st.success("Appointment updated.")
    else:
        payload["created_at"] = payload["updated_at"]
        state.insert("appointments", payload)
        st.success("Appointment booked.")
    st.session_state.pop("appt_modal", None)


def _form(cfg: Dict[str, Any], appointment: Optional[Dict[str, Any]] = None) -> None:
    appt_id = appointment.get("id") if appointment else None
    prefix = "new" if appt_id is None else f"edit_{appt_id}"
    customers = state.load_customers()

    mode_default = "Existing customer" if (appointment and appointment.get("customer_id")) else (
        "Existing customer" if not appointment and customers else "New contact")
    st.radio("Customer", ["Existing customer", "New contact"], horizontal=True,
             key=f"{prefix}_cust_mode",
             index=["Existing customer", "New contact"].index(mode_default)
             if customers or appointment else 1,
             disabled=not customers and mode_default == "New contact")

    if st.session_state.get(f"{prefix}_cust_mode", mode_default) == "Existing customer" and customers:
        labels = {c["id"]: f"{c.get('name','')} · {c.get('phone','')}" for c in customers}
        current = (appointment or {}).get("customer_id")
        st.selectbox("Select customer", list(labels.keys()),
                     format_func=lambda i: labels[i],
                     index=list(labels.keys()).index(current) if current in labels else 0,
                     key=f"{prefix}_cust_id")
    else:
        c1, c2, c3 = st.columns(3)
        c1.text_input("Full name", value=(appointment or {}).get("customer_name", ""), key=f"{prefix}_name")
        c2.text_input("Phone", value=(appointment or {}).get("customer_phone", ""), key=f"{prefix}_phone")
        c3.text_input("Email", value=(appointment or {}).get("customer_email", ""), key=f"{prefix}_email")

    services = [s["name"] for s in cfg.get("services", [])] or ["Appointment"]
    c1, c2, c3 = st.columns(3)
    c1.selectbox("Service", services,
                 index=services.index(appointment["service"])
                 if appointment and appointment.get("service") in services else 0,
                 key=f"{prefix}_service")
    date_default = date.today()
    if appointment and appointment.get("date"):
        try:
            date_default = datetime.strptime(appointment["date"], "%Y-%m-%d").date()
        except ValueError:
            pass
    c2.date_input("Date", value=date_default, min_value=date.today(), key=f"{prefix}_date")
    time_default = datetime.strptime("10:00", "%H:%M").time()
    if appointment and appointment.get("time"):
        try:
            time_default = datetime.strptime(appointment["time"], "%H:%M").time()
        except ValueError:
            pass
    c3.time_input("Time", value=time_default, step=1800, key=f"{prefix}_time")

    c1, c2 = st.columns(2)
    c1.selectbox("Status", APPOINTMENT_STATUSES,
                 index=APPOINTMENT_STATUSES.index((appointment or {}).get("status", "scheduled"))
                 if (appointment or {}).get("status") in APPOINTMENT_STATUSES else 0,
                 key=f"{prefix}_status")
    c2.text_input("Notes", value=(appointment or {}).get("notes", ""), key=f"{prefix}_notes")

    if st.form_submit_button("Save appointment", type="primary", use_container_width=True):
        _save(appt_id, cfg)


def render(cfg: Dict[str, Any]) -> None:
    theme.page_header("Appointments", "Every booking across channels — phone, simulator and manual entry.")

    appointments = sorted(state.load_appointments(),
                          key=lambda a: (a.get("date", ""), a.get("time", "")))

    with st.expander("Book an appointment manually", expanded=False):
        with st.form("new_appointment_form"):
            _form(cfg)

    if not appointments:
        theme.empty_state("📅", "No appointments yet",
                          "Bookings made by the AI receptionist will land here automatically.")
        return

    f1, f2, f3 = st.columns([2, 1, 1])
    query = f1.text_input("Search", placeholder="Name, service or phone…", label_visibility="collapsed")
    status_filter = f2.selectbox("Status", ["All"] + [s.title() for s in APPOINTMENT_STATUSES])
    window = f3.selectbox("Window", ["Upcoming", "Past", "All"])

    today = date.today().isoformat()
    filtered: List[Dict[str, Any]] = []
    for a in appointments:
        if status_filter != "All" and a.get("status") != status_filter.lower():
            continue
        if window == "Upcoming" and a.get("date", "") < today:
            continue
        if window == "Past" and a.get("date", "") >= today:
            continue
        hay = f"{a.get('customer_name','')} {a.get('service','')} {a.get('customer_phone','')}".lower()
        if query and query.lower() not in hay:
            continue
        filtered.append(a)

    if not filtered:
        st.caption("No appointments match those filters.")
        return

    frame = pd.DataFrame([{
        "Date": a.get("date", ""),
        "Time": a.get("time", ""),
        "Customer": a.get("customer_name", ""),
        "Service": a.get("service", ""),
        "Phone": a.get("customer_phone", ""),
        "Status": a.get("status", "").title(),
        "Source": (a.get("source") or "manual").title(),
    } for a in filtered])
    st.dataframe(frame, use_container_width=True, hide_index=True)

    st.markdown("##### Manage an appointment")
    selected_id = st.selectbox(
        "Select", [a["id"] for a in filtered],
        format_func=lambda i: _appt_label(next(a for a in filtered if a["id"] == i)),
        label_visibility="collapsed")
    selected = next((a for a in filtered if a["id"] == selected_id), None)
    if selected:
        c1, c2 = st.columns([3, 1])
        with c1:
            with st.form(f"edit_form_{selected['id']}"):
                _form(cfg, selected)
        with c2:
            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
            st.warning("Danger zone")
            if selected["status"] != "cancelled" and st.button("Cancel appointment",
                    key=f"cancel_{selected['id']}", use_container_width=True):
                state.upsert("appointments", selected["id"],
                             {**selected, "status": "cancelled"})
                st.rerun()
            confirm_key = f"confirm_del_{selected['id']}"
            if st.button("Delete permanently", key=f"del_{selected['id']}", use_container_width=True):
                st.session_state[confirm_key] = True
            if st.session_state.get(confirm_key):
                if st.button("Yes, delete it", key=f"really_del_{selected['id']}",
                             type="primary", use_container_width=True):
                    state.delete("appointments", selected["id"])
                    st.session_state.pop(confirm_key, None)
                    st.rerun()
