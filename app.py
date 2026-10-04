"""
AI Voice Receptionist — production Streamlit application.

Flow:  Firebase setup → sign in (email/password or Google) → design your
receptionist (persona form) → dashboard, bookings, customers, calls, training
and a live simulator. All data lives in the user's own Firebase project.

Run:  streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

from streamlit_app import state, theme
from streamlit_app.auth import handle_oauth_callback, render_auth_page
from streamlit_app.config import APP_ICON, APP_NAME, load_firebase_config
from streamlit_app.setup_screen import render_setup_screen

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)
theme.inject_theme()


def main() -> None:
    # 0) Google OAuth return URL carries ?code&state — complete sign-in first.
    if handle_oauth_callback():
        return

    # 1) Firebase must be connected before anything else works.
    if not load_firebase_config():
        st.session_state.pop("nav_pending", None)
        render_setup_screen()
        return

    # 2) Authentication gate.
    user = state.current_user()
    if not user:
        auth_col = st.columns([1])[0]  # keep sidebar collapsed for auth
        st.markdown('<style>section[data-testid="stSidebar"]{display:none}</style>',
                    unsafe_allow_html=True)
        render_auth_page()
        return

    # 3) Load the receptionist profile from Firestore.
    agent_cfg = state.load_agent_config()
    onboarding_complete = bool(agent_cfg and agent_cfg.get("onboarding_complete"))

    # 4) Sidebar + routing.
    requested = state.get_current_page()
    page = theme.render_sidebar(
        user, requested, onboarding_complete,
        agent_name=(agent_cfg or {}).get("agent_name", ""),
        business=(agent_cfg or {}).get("business_name", ""),
    )
    state.navigate(page)

    if not onboarding_complete or page == "Receptionist Setup":
        from streamlit_app.onboarding import render_onboarding
        render_onboarding(agent_cfg if onboarding_complete else None)
        return

    from streamlit_app.pages import (appointments, calls, customers, dashboard,
                                     settings, simulator, training)

    routes = {
        "Dashboard": dashboard.render,
        "Appointments": appointments.render,
        "Customers": customers.render,
        "Calls": calls.render,
        "AI Training": training.render,
        "Simulator": simulator.render,
        "Settings": settings.render,
    }
    render_fn = routes.get(page, dashboard.render)
    try:
        render_fn(agent_cfg)
    except Exception as exc:  # surfaced instead of a red traceback wall
        st.error(f"Something went wrong on this page: {exc}")


main()
