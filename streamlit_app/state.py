"""Session state, routing, and cached Firestore data access."""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import streamlit as st

from .config import APP_URL_DEFAULT, load_firebase_config
from .firebase_client import FirebaseClient, FirebaseError

SESSION_USER = "auth_user"
SESSION_PAGE = "current_page"


def get_firebase() -> Optional[FirebaseClient]:
    cfg = load_firebase_config()
    if not cfg:
        return None
    return FirebaseClient(
        api_key=cfg["api_key"],
        project_id=cfg["project_id"],
        app_url=cfg.get("app_url", APP_URL_DEFAULT),
    )


def current_user() -> Optional[Dict[str, Any]]:
    return st.session_state.get(SESSION_USER)


def set_user(user: Dict[str, Any]) -> None:
    st.session_state[SESSION_USER] = user


def sign_out() -> None:
    st.cache_data.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def navigate(page: str) -> None:
    st.session_state[SESSION_PAGE] = page


def get_current_page() -> str:
    return st.session_state.get(SESSION_PAGE, "Dashboard")


def ensure_fresh_token() -> Optional[str]:
    """Return a valid ID token, refreshing silently when possible."""
    user = current_user()
    fb = get_firebase()
    if not user or not fb:
        return None
    if time.time() < user.get("token_expiry", 0) - 120:
        return user["id_token"]
    try:
        data = fb.refresh_id_token(user["refresh_token"])
        user["id_token"] = data["id_token"]
        user["refresh_token"] = data.get("refresh_token", user["refresh_token"])
        user["token_expiry"] = time.time() + int(data.get("expires_in", "3600"))
        set_user(user)
        return user["id_token"]
    except FirebaseError:
        return None


# ---------------------------------------------------------------------------
# Cached Firestore accessors (cleared after every write)
# ---------------------------------------------------------------------------

@st.cache_data(ttl=60, show_spinner=False)
def _cached_get(uid: str, collection: str, doc_id: str, token: str) -> Optional[Dict[str, Any]]:
    fb = get_firebase()
    return fb.get_document(uid, collection, doc_id, token) if fb else None


@st.cache_data(ttl=60, show_spinner=False)
def _cached_list(uid: str, collection: str, token: str) -> List[Dict[str, Any]]:
    fb = get_firebase()
    return fb.list_documents(uid, collection, token) if fb else []


def _token() -> str:
    token = ensure_fresh_token()
    if not token:
        sign_out()
        st.rerun()
    return token


def load_agent_config() -> Optional[Dict[str, Any]]:
    user = current_user()
    if not user:
        return None
    try:
        return _cached_get(user["uid"], "agentConfig", "config", _token())
    except FirebaseError as exc:
        st.error(str(exc))
        return None


def load_customers() -> List[Dict[str, Any]]:
    user = current_user()
    return _cached_list(user["uid"], "customers", _token()) if user else []


def load_appointments() -> List[Dict[str, Any]]:
    user = current_user()
    return _cached_list(user["uid"], "appointments", _token()) if user else []


def load_calls() -> List[Dict[str, Any]]:
    user = current_user()
    return _cached_list(user["uid"], "calls", _token()) if user else []


def load_trainings() -> List[Dict[str, Any]]:
    user = current_user()
    runs = _cached_list(user["uid"], "trainings", _token()) if user else []
    return sorted(runs, key=lambda r: r.get("trained_at", ""), reverse=True)


def invalidate_cache() -> None:
    st.cache_data.clear()


def save_agent_config(cfg: Dict[str, Any]) -> None:
    user, fb = current_user(), get_firebase()
    fb.set_document(user["uid"], "agentConfig", "config", cfg, _token())
    invalidate_cache()


def upsert(collection: str, doc_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    user, fb = current_user(), get_firebase()
    doc = fb.set_document(user["uid"], collection, doc_id, data, _token())
    invalidate_cache()
    return doc


def insert(collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
    user, fb = current_user(), get_firebase()
    doc = fb.create_document(user["uid"], collection, data, _token())
    invalidate_cache()
    return doc


def delete(collection: str, doc_id: str) -> None:
    user, fb = current_user(), get_firebase()
    fb.delete_document(user["uid"], collection, doc_id, _token())
    invalidate_cache()
