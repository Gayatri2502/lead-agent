"""Customers: CRM-lite, fully Firestore-backed."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

from .. import state, theme


def _save(customer_id: Optional[str]) -> None:
    prefix = "cust_new" if customer_id is None else f"cust_edit_{customer_id}"
    name = st.session_state[f"{prefix}_name"].strip()
    if not name:
        st.error("Name is required.")
        return
    payload = {
        "name": name,
        "phone": st.session_state[f"{prefix}_phone"].strip(),
        "email": st.session_state[f"{prefix}_email"].strip(),
        "notes": st.session_state.get(f"{prefix}_notes", "").strip(),
        "tags": [t.strip() for t in st.session_state.get(f"{prefix}_tags", "").split(",") if t.strip()],
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    if customer_id:
        state.upsert("customers", customer_id, payload)
        st.success("Customer updated.")
    else:
        payload["created_at"] = payload["updated_at"]
        payload["last_seen"] = ""
        state.insert("customers", payload)
        st.success("Customer added.")


def _form(customer: Optional[Dict[str, Any]] = None) -> None:
    cid = customer.get("id") if customer else None
    prefix = "cust_new" if cid is None else f"cust_edit_{cid}"
    c1, c2 = st.columns(2)
    c1.text_input("Full name", value=(customer or {}).get("name", ""), key=f"{prefix}_name")
    c2.text_input("Phone", value=(customer or {}).get("phone", ""), key=f"{prefix}_phone")
    c1, c2 = st.columns(2)
    c1.text_input("Email", value=(customer or {}).get("email", ""), key=f"{prefix}_email")
    c2.text_input("Tags (comma separated)", value=", ".join((customer or {}).get("tags", [])),
                  key=f"{prefix}_tags", placeholder="vip, referral")
    st.text_area("Notes", value=(customer or {}).get("notes", ""), key=f"{prefix}_notes", height=70)
    if st.form_submit_button("Save customer", type="primary", use_container_width=True):
        _save(cid)


def render(cfg: Dict[str, Any]) -> None:
    theme.page_header("Customers", "Everyone who has called or booked — captured automatically by the receptionist.")

    customers: List[Dict[str, Any]] = sorted(
        state.load_customers(), key=lambda c: c.get("created_at", ""), reverse=True)
    appointments = state.load_appointments()
    calls = state.load_calls()

    with st.expander("Add a customer manually", expanded=False):
        with st.form("new_customer_form"):
            _form()

    if not customers:
        theme.empty_state("🧑‍🤝‍🧑", "No customers yet",
                          "Callers who book through the AI receptionist become customers automatically.")
        return

    query = st.text_input("Search", placeholder="Name, phone, email or tag…",
                          label_visibility="collapsed")
    if query:
        q = query.lower()
        customers = [c for c in customers if q in
                     f"{c.get('name','')} {c.get('phone','')} {c.get('email','')} {' '.join(c.get('tags', []))}".lower()]

    frame = pd.DataFrame([{
        "Name": c.get("name", ""),
        "Phone": c.get("phone", ""),
        "Email": c.get("email", ""),
        "Tags": ", ".join(c.get("tags", [])),
        "Bookings": sum(1 for a in appointments if a.get("customer_phone") == c.get("phone")),
        "Calls": sum(1 for c2 in calls if c2.get("customer_phone") == c.get("phone")),
        "Added": (c.get("created_at") or "")[:10],
    } for c in customers])
    st.dataframe(frame, use_container_width=True, hide_index=True)

    st.markdown("##### Customer detail")
    selected_id = st.selectbox(
        "Select customer", [c["id"] for c in customers],
        format_func=lambda i: next(c for c in customers if c["id"] == i).get("name", ""),
        label_visibility="collapsed")
    selected = next((c for c in customers if c["id"] == selected_id), None)
    if not selected:
        return

    c1, c2 = st.columns([3, 2])
    with c1:
        with st.form(f"customer_edit_{selected['id']}"):
            _form(selected)
    with c2:
        with st.container(border=True):
            st.markdown(f"**{selected.get('name','')}**")
            cust_appts = [a for a in appointments
                          if a.get("customer_phone") == selected.get("phone")]
            st.caption(f"{len(cust_appts)} appointment(s) on record")
            for a in sorted(cust_appts, key=lambda x: x.get("start_iso", ""), reverse=True)[:5]:
                st.markdown(
                    f"- {a.get('date','')} {a.get('time','')} — {a.get('service','')} "
                    f"({a.get('status','')})")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        confirm_key = f"confirm_cust_del_{selected['id']}"
        if st.button("Delete customer", key=f"del_cust_{selected['id']}"):
            st.session_state[confirm_key] = True
        if st.session_state.get(confirm_key):
            st.warning("This removes the customer record (not past appointments).")
            if st.button("Yes, delete", key=f"really_del_cust_{selected['id']}", type="primary"):
                state.delete("customers", selected["id"])
                st.session_state.pop(confirm_key, None)
                st.rerun()
