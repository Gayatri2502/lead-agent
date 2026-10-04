"""Calls: real call records with transcripts, written by the simulator/telephony."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from .. import state, theme


def _fmt_duration(seconds: int) -> str:
    seconds = int(seconds or 0)
    return f"{seconds // 60}m {seconds % 60:02d}s"


def _nice_dt(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso).strftime("%a %b %-d, %-I:%M %p")
    except (ValueError, TypeError):
        return iso


def render(cfg: Dict[str, Any]) -> None:
    theme.page_header("Calls", "Every conversation the receptionist handled, with full transcripts.")

    calls: List[Dict[str, Any]] = sorted(
        state.load_calls(), key=lambda c: c.get("started_at", ""), reverse=True)

    if not calls:
        theme.empty_state("📞", "No calls yet",
                          "Use the Simulator to place your first test call — transcripts and "
                          "outcomes are stored here automatically.")
        return

    f1, f2 = st.columns([2, 1])
    query = f1.text_input("Search calls", placeholder="Name, phone or transcript text…",
                          label_visibility="collapsed")
    outcome = f2.selectbox("Outcome", ["All", "Booked", "Cancelled", "Info", "Escalated"])

    filtered = []
    for c in calls:
        if outcome != "All" and (c.get("outcome") or "info") != outcome.lower():
            continue
        if query:
            hay = " ".join([
                c.get("customer_name", ""), c.get("customer_phone", ""),
                " ".join(t.get("text", "") for t in c.get("transcript", [])),
            ]).lower()
            if query.lower() not in hay:
                continue
        filtered.append(c)

    if not filtered:
        st.caption("No calls match those filters.")
        return

    frame = pd.DataFrame([{
        "When": _nice_dt(c.get("started_at", "")),
        "Caller": c.get("customer_name") or "Unknown",
        "Phone": c.get("customer_phone", ""),
        "Duration": _fmt_duration(c.get("duration_sec", 0)),
        "Intents": ", ".join(dict.fromkeys(c.get("intents", [])))[:40],
        "Outcome": (c.get("outcome") or "info").title(),
        "Source": (c.get("source") or "phone").title(),
    } for c in filtered])
    st.dataframe(frame, use_container_width=True, hide_index=True)

    labels = {c["id"]: f"{_nice_dt(c.get('started_at',''))} — "
              f"{c.get('customer_name') or c.get('customer_phone') or 'Unknown caller'}"
              for c in filtered}
    selected_id = st.selectbox("Open call", list(labels.keys()),
                               format_func=lambda i: labels[i])
    call = next((c for c in filtered if c["id"] == selected_id), None)
    if not call:
        return

    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"**Outcome**\n\n{(call.get('outcome') or 'info').title()}")
        c2.markdown(f"**Duration**\n\n{_fmt_duration(call.get('duration_sec', 0))}")
        c3.markdown(f"**Direction**\n\n{(call.get('direction') or 'inbound').title()}")
        c4.markdown(f"**Source**\n\n{(call.get('source') or 'phone').title()}")

        st.markdown("**Transcript**")
        for turn in call.get("transcript", []):
            speaker = "🤖" if turn.get("speaker") == "agent" else "🧑"
            who = "Receptionist" if turn.get("speaker") == "agent" else (call.get("customer_name") or "Caller")
            st.markdown(
                f"<div style='margin:6px 0;padding:10px 14px;border-radius:10px;"
                f"background:{'#EEF2FF' if turn.get('speaker')=='agent' else '#F8FAFC'};"
                f"border:1px solid #E2E8F0;font-size:13.5px;'>"
                f"<b>{speaker} {who}</b> <span style='color:#94A3B8;font-size:11px;'>"
                f"{turn.get('time','')}</span><br/>{turn.get('text','')}</div>",
                unsafe_allow_html=True)

    if st.button("Delete call record", key=f"del_call_{call['id']}"):
        state.delete("calls", call["id"])
        st.rerun()
