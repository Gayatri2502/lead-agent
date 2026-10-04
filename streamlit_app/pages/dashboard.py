"""Dashboard: live business overview computed from Firestore data."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .. import state, theme


def _parse_day(iso: str):
    try:
        return datetime.fromisoformat(iso).date()
    except (ValueError, TypeError):
        return None


def _metric_cards(appointments, calls, customers) -> None:
    today = date.today().isoformat()
    week_ago = (date.today() - timedelta(days=7)).isoformat()

    appts_today = [a for a in appointments if a.get("date") == today and a.get("status") != "cancelled"]
    upcoming = [a for a in appointments if a.get("date", "") >= today and a.get("status") != "cancelled"]
    calls_today = [c for c in calls if c.get("date") == today]
    new_customers = [c for c in customers if c.get("created_at", "")[:10] >= week_ago]

    cols = st.columns(4)
    with cols[0]:
        theme.metric_card("Appointments today", len(appts_today),
                          f"{len(upcoming)} total upcoming")
    with cols[1]:
        theme.metric_card("Calls today", len(calls_today), f"{len(calls)} all time")
    with cols[2]:
        booked = [c for c in calls if c.get("outcome") == "booked"]
        rate = f"{round(100 * len(booked) / len(calls))}%" if calls else "—"
        theme.metric_card("Booking rate", rate, "calls that ended in a booking")
    with cols[3]:
        theme.metric_card("Customers", len(customers), f"+{len(new_customers)} this week")


def _calls_chart(calls: List[Dict[str, Any]]) -> None:
    days = [(date.today() - timedelta(days=13 - i)) for i in range(14)]
    counts = {d.isoformat(): 0 for d in days}
    for call in calls:
        key = call.get("date", "")
        if key in counts:
            counts[key] += 1
    frame = pd.DataFrame({"Day": list(counts.keys()), "Calls": list(counts.values())})
    fig = px.bar(frame, x="Day", y="Calls")
    fig.update_traces(marker_color="#4F46E5", marker_line_width=0)
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=230,
                      plot_bgcolor="white", paper_bgcolor="white",
                      xaxis=dict(showgrid=False, title=None),
                      yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=None))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _status_chart(appointments: List[Dict[str, Any]]) -> None:
    counts: Dict[str, int] = {}
    for appt in appointments:
        status = appt.get("status", "scheduled")
        counts[status] = counts.get(status, 0) + 1
    fig = go.Figure(go.Pie(
        labels=[k.title() for k in counts], values=list(counts.values()), hole=0.62,
        marker_colors=["#4F46E5", "#10B981", "#94A3B8", "#EF4444"]))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=230,
                      paper_bgcolor="white", showlegend=True,
                      legend=dict(orientation="h", y=-0.08))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render(cfg: Dict[str, Any]) -> None:
    theme.page_header(
        f"Good {_daypart()}, {state.current_user().get('display_name', 'there').split()[0]}",
        f"Here's what's happening at {cfg.get('business_name', 'your business')} today.",
    )

    appointments = state.load_appointments()
    calls = state.load_calls()
    customers = state.load_customers()

    _metric_cards(appointments, calls, customers)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if not appointments and not calls and not customers:
        theme.empty_state(
            "🛰️", "Waiting for your first call",
            "Your receptionist is trained. Head to the Simulator to place a test call — "
            "bookings, customers and call records will appear here in real time.",
        )
        if st.button("Open the Simulator", type="primary"):
            state.navigate("Simulator")
            st.rerun()
        return

    c1, c2 = st.columns([1.6, 1])
    with c1:
        with st.container(border=True):
            st.markdown("**Calls — last 14 days**")
            _calls_chart(calls)
    with c2:
        with st.container(border=True):
            st.markdown("**Appointments by status**")
            if appointments:
                _status_chart(appointments)
            else:
                st.caption("No appointments yet.")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    today = date.today().isoformat()
    todays = sorted([a for a in appointments if a.get("date") == today],
                    key=lambda a: a.get("time", ""))
    with c1:
        with st.container(border=True):
            st.markdown("**Today's appointments**")
            if not todays:
                st.caption("Nothing scheduled today.")
            else:
                frame = pd.DataFrame([{
                    "Time": a.get("time", ""),
                    "Customer": a.get("customer_name", ""),
                    "Service": a.get("service", ""),
                    "Status": a.get("status", "").title(),
                } for a in todays])
                st.dataframe(frame, use_container_width=True, hide_index=True)

    with c2:
        with st.container(border=True):
            st.markdown("**Recent calls**")
            recent = sorted(calls, key=lambda c: c.get("started_at", ""), reverse=True)[:6]
            if not recent:
                st.caption("No calls recorded yet.")
            else:
                frame = pd.DataFrame([{
                    "When": _nice_dt(c.get("started_at", "")),
                    "Caller": c.get("customer_name") or c.get("customer_phone") or "Unknown",
                    "Outcome": (c.get("outcome") or "info").title(),
                } for c in recent])
                st.dataframe(frame, use_container_width=True, hide_index=True)


def _daypart() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "morning"
    if hour < 18:
        return "afternoon"
    return "evening"


def _nice_dt(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso).strftime("%b %-d, %-I:%M %p")
    except (ValueError, TypeError):
        return iso
