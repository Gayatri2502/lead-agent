"""First-run screen: connect the app to the user's Firebase project."""
from __future__ import annotations

import streamlit as st

from .config import APP_ICON, APP_NAME, APP_TAGLINE, save_firebase_config

FIRESTORE_RULES = """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid}/{doc=**} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}"""


def render_setup_screen() -> None:
    st.markdown("<div style='height:4vh'></div>", unsafe_allow_html=True)
    col = st.columns([1, 1.5, 1])[1]
    with col:
        st.markdown(
            f"""<div style="text-align:center;margin-bottom:20px;">
                <div style="width:60px;height:60px;border-radius:16px;margin:0 auto 12px;
                    background:linear-gradient(135deg,#6366F1,#4338CA);display:flex;
                    align-items:center;justify-content:center;font-size:28px;">{APP_ICON}</div>
                <div style="font-size:22px;font-weight:800;color:#0F172A;">Connect Firebase</div>
                <div style="color:#64748B;font-size:13.5px;">{APP_NAME} stores everything in your own
                Firebase project — auth, database, training reports.</div>
            </div>""",
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown("**1 · Create / open your Firebase project**")
            st.caption("Go to [console.firebase.google.com](https://console.firebase.google.com) → "
                       "create a project → add a **Web app**. Copy the `apiKey` and `projectId`.")
            st.markdown("**2 · Enable services**")
            st.caption("Authentication → enable **Email/Password** (and **Google** for one-click "
                       "sign-in). Firestore Database → create in production mode.")
            st.markdown("**3 · Secure Firestore**")
            st.caption("Firestore → Rules → paste and publish:")
            st.code(FIRESTORE_RULES, language="javascript")

        with st.container(border=True):
            with st.form("firebase_setup_form"):
                api_key = st.text_input("Web API key", placeholder="AIzaSy…")
                project_id = st.text_input("Project ID", placeholder="my-receptionist-app")
                app_url = st.text_input("App URL", value="http://localhost:8501",
                                        help="Used as the Google OAuth redirect. Must match an "
                                             "authorized redirect URI on your Google OAuth client.")
                st.caption("Optional — only needed for the “Continue with Google” button. Create an "
                           "OAuth 2.0 **Web application** client in Google Cloud Console with the "
                           "App URL above as an authorized redirect URI.")
                gid = st.text_input("Google OAuth client ID (optional)")
                gsecret = st.text_input("Google OAuth client secret (optional)", type="password")
                submitted = st.form_submit_button("Connect", use_container_width=True,
                                                  type="primary")

        if submitted:
            if not api_key.strip() or not project_id.strip():
                st.error("Web API key and Project ID are required.")
            else:
                save_firebase_config({
                    "api_key": api_key.strip(),
                    "project_id": project_id.strip(),
                    "app_url": app_url.strip(),
                    "google_client_id": gid.strip(),
                    "google_client_secret": gsecret.strip(),
                })
                st.success("Firebase connected. Reloading…")
                st.rerun()
