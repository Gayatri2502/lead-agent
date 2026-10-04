"""Settings: account, receptionist profile, integrations, data management."""
from __future__ import annotations

import os
from typing import Any, Dict

import streamlit as st

from .. import state, theme
from ..config import FIREBASE_CONFIG_PATH, load_firebase_config, save_firebase_config
from ..ml.train import load_model, model_path


def render(cfg: Dict[str, Any]) -> None:
    user = state.current_user()
    theme.page_header("Settings", "Account, receptionist profile, integrations and data controls.")

    tab_profile, tab_integrations, tab_data = st.tabs(
        ["Profile & receptionist", "Integrations", "Data management"])

    # ------------------------------------------------------------------ tab 1
    with tab_profile:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**Account**")
                st.markdown(f"**{user.get('display_name') or 'User'}**")
                st.caption(user.get("email", ""))
                st.caption(f"UID: `{user.get('uid','')}`")
        with c2:
            with st.container(border=True):
                st.markdown("**Receptionist profile**")
                st.markdown(f"**{cfg.get('agent_name','')}** — {cfg.get('role','')}")
                st.caption(f"{cfg.get('business_name','')} · {cfg.get('tone','')} tone · "
                           f"voice `{cfg.get('voice','')}`")
                if st.button("Edit receptionist setup", use_container_width=True):
                    state.navigate("Receptionist Setup")
                    st.rerun()

    # ------------------------------------------------------------------ tab 2
    with tab_integrations:
        fb_cfg = load_firebase_config() or {}
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**Firebase**")
                st.markdown(theme.status_chip("Connected", "green"), unsafe_allow_html=True)
                st.caption(f"Project: `{fb_cfg.get('project_id','')}`")
                google_ok = bool(fb_cfg.get("google_client_id") and fb_cfg.get("google_client_secret"))
                st.caption("Google sign-in: " + ("enabled" if google_ok else "not configured"))
        with c2:
            with st.container(border=True):
                st.markdown("**Receptionist model**")
                trained = load_model(user["uid"]) is not None
                st.markdown(theme.status_chip("Trained" if trained else "Not trained",
                                              "green" if trained else "amber"),
                            unsafe_allow_html=True)
                if trained:
                    try:
                        size_kb = os.path.getsize(model_path(user["uid"])) // 1024
                        st.caption(f"Local model artifact: {size_kb} KB")
                    except OSError:
                        pass

        with st.container(border=True):
            st.markdown("**Telephony (production calling)**")
            st.caption(
                "Live phone calls run through the FastAPI backend (Twilio/Vapi webhooks) in "
                "`backend/`. The agent profile and system prompt in Firebase are what the "
                "backend consumes. Configure Twilio credentials in `backend/.env` to go live.")

        with st.expander("Update Firebase connection / enable Google sign-in"):
            st.caption("Find these in Firebase Console → Project settings → Your apps → Web app. "
                       "Google sign-in additionally needs an OAuth 2.0 **Web** client from "
                       "Google Cloud Console with the app URL as an authorized redirect URI.")
            with st.form("firebase_update"):
                api_key = st.text_input("Web API key", value=fb_cfg.get("api_key", ""))
                project_id = st.text_input("Project ID", value=fb_cfg.get("project_id", ""))
                app_url = st.text_input("App URL (OAuth redirect)",
                                        value=fb_cfg.get("app_url", "http://localhost:8501"))
                gid = st.text_input("Google OAuth client ID (optional)",
                                    value=fb_cfg.get("google_client_id", ""))
                gsecret = st.text_input("Google OAuth client secret (optional)",
                                        value=fb_cfg.get("google_client_secret", ""),
                                        type="password")
                if st.form_submit_button("Save Firebase settings", use_container_width=True):
                    save_firebase_config({
                        "api_key": api_key.strip(), "project_id": project_id.strip(),
                        "app_url": app_url.strip(),
                        "google_client_id": gid.strip(),
                        "google_client_secret": gsecret.strip(),
                    })
                    st.success("Saved. Sign-in changes apply on your next sign-in.")

    # ------------------------------------------------------------------ tab 3
    with tab_data:
        with st.container(border=True):
            st.markdown("**Clear collected data**")
            st.caption("Deletes documents from your Firebase workspace. This cannot be undone.")
            for label, collection in [("Calls", "calls"), ("Appointments", "appointments"),
                                      ("Customers", "customers"), ("Training history", "trainings")]:
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"{label}")
                key = f"confirm_clear_{collection}"
                if st.session_state.get(key):
                    if c2.button("Confirm?", key=f"btn_{key}", type="primary",
                                 use_container_width=True):
                        fb = state.get_firebase()
                        n = fb.delete_collection(user["uid"], collection, state._token())
                        state.invalidate_cache()
                        st.session_state.pop(key, None)
                        st.success(f"Deleted {n} {label.lower()} records.")
                        st.rerun()
                else:
                    if c2.button("Clear", key=f"btn_clear_{collection}", use_container_width=True):
                        st.session_state[key] = True
                        st.rerun()
