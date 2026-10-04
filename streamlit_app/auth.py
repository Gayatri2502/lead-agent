"""Authentication screens: email/password and Google sign-in through Firebase."""
from __future__ import annotations

import html
from typing import Any, Dict, Optional, Set

import requests
import streamlit as st

from . import state
from .config import APP_ICON, APP_NAME, APP_TAGLINE, load_firebase_config
from .firebase_client import FirebaseError

_GOOGLE_SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email",
                  "https://www.googleapis.com/auth/userinfo.profile"]

# Server-side store of in-flight OAuth states (single Streamlit process).
_PENDING_OAUTH_STATES: Set[str] = set()


def _google_flow():
    """Build a google-auth-oauthlib Flow from saved config, if Google OAuth is set up."""
    from google_auth_oauthlib.flow import Flow

    cfg = load_firebase_config() or {}
    client_id, client_secret = cfg.get("google_client_id"), cfg.get("google_client_secret")
    if not client_id or not client_secret:
        return None
    app_url = cfg.get("app_url", "http://localhost:8501").rstrip("/")
    return Flow.from_client_config(
        {"web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [app_url],
        }},
        scopes=_GOOGLE_SCOPES,
        redirect_uri=app_url,
    )


def google_oauth_url() -> Optional[str]:
    flow = _google_flow()
    if not flow:
        return None
    auth_url, oauth_state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="select_account")
    _PENDING_OAUTH_STATES.add(oauth_state)
    return auth_url


def handle_oauth_callback() -> bool:
    """If the URL carries a Google OAuth code, complete the Firebase sign-in. True if handled."""
    params = st.query_params
    code, oauth_state = params.get("code"), params.get("state")
    if not code or not oauth_state:
        return False
    st.query_params.clear()
    if oauth_state not in _PENDING_OAUTH_STATES:
        st.error("Sign-in session expired or was started elsewhere. Please try again.")
        return True
    _PENDING_OAUTH_STATES.discard(oauth_state)

    flow = _google_flow()
    fb = state.get_firebase()
    if not flow or not fb:
        st.error("Google sign-in is not configured.")
        return True
    try:
        flow.fetch_token(code=code)
        id_token = getattr(flow.credentials, "id_token", None)
        if not id_token:  # pragma: no cover - depends on google response
            id_token = getattr(flow.credentials, "_id_token", None)
        auth = fb.sign_in_with_google_id_token(id_token)
        state.set_user(fb.session_from_auth(auth))
        st.rerun()
    except (FirebaseError, requests.RequestException, ValueError) as exc:
        st.error(f"Google sign-in failed: {exc}")
    return True


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

def render_auth_page() -> None:
    """Centered, professional sign-in screen."""
    st.markdown("<div style='height:6vh'></div>", unsafe_allow_html=True)
    col = st.columns([1, 1.15, 1])[1]

    with col:
        st.markdown(
            f"""<div style="text-align:center; margin-bottom: 26px;">
                <div style="width:64px;height:64px;border-radius:18px;margin:0 auto 14px;
                    background:linear-gradient(135deg,#6366F1,#4338CA);display:flex;
                    align-items:center;justify-content:center;font-size:32px;
                    box-shadow:0 10px 30px rgba(99,102,241,.35);">{APP_ICON}</div>
                <div style="font-size:24px;font-weight:800;color:#0F172A;letter-spacing:-0.02em;">{APP_NAME}</div>
                <div style="color:#64748B;font-size:14px;margin-top:4px;">{html.escape(APP_TAGLINE)}</div>
            </div>""",
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            google_url = None
            google_err = None
            try:
                google_url = google_oauth_url()
            except Exception as exc:  # invalid client config shouldn't block email auth
                google_err = str(exc)

            tab_signin, tab_signup = st.tabs(["Sign in", "Create account"])
            with tab_signin:
                _sign_in_form()
            with tab_signup:
                _sign_up_form()

            st.markdown(
                "<div style='display:flex;align-items:center;gap:12px;color:#94A3B8;"
                "font-size:12px;margin:14px 0 12px;'>"
                "<div style='flex:1;height:1px;background:#E2E8F0'></div>OR"
                "<div style='flex:1;height:1px;background:#E2E8F0'></div></div>",
                unsafe_allow_html=True,
            )
            if google_url:
                st.link_button("🔵  Continue with Google", google_url, use_container_width=True)
            elif google_err:
                st.caption(f"Google sign-in misconfigured: {google_err}")
            else:
                st.button("🔵  Continue with Google", use_container_width=True, disabled=True,
                          help="Add your Google OAuth Client ID & Secret in the Firebase setup screen to enable this.")

        st.markdown(
            "<div style='text-align:center;color:#94A3B8;font-size:12px;margin-top:18px;'>"
            "Secured by Firebase Authentication</div>",
            unsafe_allow_html=True,
        )


def _sign_in_form() -> None:
    with st.form("sign_in_form"):
        email = st.text_input("Email", placeholder="you@business.com", autocomplete="email")
        password = st.text_input("Password", type="password", autocomplete="current-password")
        submitted = st.form_submit_button("Sign in", use_container_width=True, type="primary")
    if submitted:
        if not email or not password:
            st.warning("Enter your email and password.")
        else:
            _do_auth(email.strip(), password, mode="sign_in")

    with st.expander("Forgot your password?"):
        with st.form("reset_form"):
            reset_email = st.text_input("Account email", key="reset_email")
            reset_submitted = st.form_submit_button("Send reset link", use_container_width=True)
        if reset_submitted:
            fb = state.get_firebase()
            try:
                fb.send_password_reset(reset_email.strip())
                st.success("Password reset email sent. Check your inbox.")
            except FirebaseError as exc:
                st.error(str(exc))


def _sign_up_form() -> None:
    with st.form("sign_up_form"):
        name = st.text_input("Your name", placeholder="Ava Carter")
        email = st.text_input("Work email", placeholder="you@business.com", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password",
                                 help="Minimum 6 characters.", autocomplete="new-password")
        password2 = st.text_input("Confirm password", type="password", key="signup_password2",
                                  autocomplete="new-password")
        submitted = st.form_submit_button("Create account", use_container_width=True, type="primary")
    if submitted:
        if not name.strip() or not email.strip() or not password:
            st.warning("Please fill in all fields.")
        elif password != password2:
            st.warning("Passwords do not match.")
        else:
            _do_auth(email.strip(), password, mode="sign_up", display_name=name.strip())


def _do_auth(email: str, password: str, mode: str, display_name: str = "") -> None:
    fb = state.get_firebase()
    try:
        auth = fb.sign_up(email, password) if mode == "sign_up" else fb.sign_in(email, password)
        user = fb.session_from_auth(auth)
        if display_name:
            user["display_name"] = display_name
        state.set_user(user)
        st.rerun()
    except (FirebaseError, requests.RequestException) as exc:
        st.error(str(exc))
