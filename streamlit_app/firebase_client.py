"""Firebase client using only public REST APIs.

- Auth:    Identity Toolkit (email/password, Google IDP, refresh, password reset)
- Data:    Cloud Firestore REST API, authorized with the signed-in user's ID token,
           so Firestore Security Rules apply per user.

No service account or Admin SDK required — only the Firebase *web* config values.
"""
from __future__ import annotations

import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

IDENTITY_URL = "https://identitytoolkit.googleapis.com/v1"
SECURE_TOKEN_URL = "https://securetoken.googleapis.com/v1"
FIRESTORE_URL = "https://firestore.googleapis.com/v1"
REQUEST_TIMEOUT = 20


class FirebaseError(Exception):
    """Raised for Firebase REST errors with a human-readable message."""

    def __init__(self, message: str, code: str = ""):
        super().__init__(message)
        self.code = code


def _friendly_auth_message(code: str) -> str:
    table = {
        "EMAIL_EXISTS": "An account already exists with this email.",
        "OPERATION_NOT_ALLOWED": "Email/password sign-in is not enabled in Firebase Console.",
        "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts. Please try again later.",
        "EMAIL_NOT_FOUND": "No account found with this email.",
        "INVALID_PASSWORD": "Incorrect password.",
        "INVALID_LOGIN_CREDENTIALS": "Incorrect email or password.",
        "USER_DISABLED": "This account has been disabled.",
        "INVALID_ID_TOKEN": "Your session expired. Please sign in again.",
        "TOKEN_EXPIRED": "Your session expired. Please sign in again.",
        "INVALID_EMAIL": "That email address looks invalid.",
        "WEAK_PASSWORD": "Password should be at least 6 characters.",
        "MISSING_PASSWORD": "Please enter a password.",
    }
    for key, msg in table.items():
        if key in code:
            return msg
    return code.replace("_", " ").capitalize() or "Authentication failed"


# ---------------------------------------------------------------------------
# Value encoding / decoding for Firestore documents
# ---------------------------------------------------------------------------

def _encode_value(value: Any) -> Dict[str, Any]:
    if value is None:
        return {"nullValue": None}
    if isinstance(value, bool):
        return {"booleanValue": value}
    if isinstance(value, int):
        return {"integerValue": str(value)}
    if isinstance(value, float):
        return {"doubleValue": value}
    if isinstance(value, str):
        return {"stringValue": value}
    if isinstance(value, datetime):
        return {"timestampValue": value.strftime("%Y-%m-%dT%H:%M:%SZ")}
    if isinstance(value, (list, tuple)):
        return {"arrayValue": {"values": [_encode_value(v) for v in value]}}
    if isinstance(value, dict):
        return {"mapValue": {"fields": {k: _encode_value(v) for k, v in value.items()}}}
    return {"stringValue": str(value)}


def _decode_value(data: Dict[str, Any]) -> Any:
    if "nullValue" in data:
        return None
    if "booleanValue" in data:
        return bool(data["booleanValue"])
    if "integerValue" in data:
        return int(data["integerValue"])
    if "doubleValue" in data:
        return float(data["doubleValue"])
    if "stringValue" in data:
        return data["stringValue"]
    if "timestampValue" in data:
        return data["timestampValue"]
    if "arrayValue" in data:
        return [_decode_value(v) for v in data.get("arrayValue", {}).get("values", [])]
    if "mapValue" in data:
        return {k: _decode_value(v) for k, v in data.get("mapValue", {}).get("fields", {}).items()}
    return None


def encode_fields(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {"fields": {k: _encode_value(v) for k, v in doc.items()}}


def decode_document(raw: Dict[str, Any]) -> Dict[str, Any]:
    doc = {k: _decode_value(v) for k, v in raw.get("fields", {}).items()}
    name = raw.get("name", "")
    if name and "id" not in doc:
        doc["id"] = name.rstrip("/").split("/")[-1]
    return doc


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class FirebaseClient:
    def __init__(self, api_key: str, project_id: str, app_url: str = "http://localhost:8501"):
        self.api_key = api_key
        self.project_id = project_id
        self.app_url = app_url.rstrip("/")
        self._fs_base = f"{FIRESTORE_URL}/projects/{project_id}/databases/(default)/documents"

    # ------------------------------ Auth ---------------------------------

    def _auth_post(self, path: str, payload: Dict[str, Any], base: str = IDENTITY_URL) -> Dict[str, Any]:
        resp = requests.post(
            f"{base}/{path}?key={self.api_key}", json=payload, timeout=REQUEST_TIMEOUT
        )
        data = resp.json() if resp.content else {}
        if resp.status_code != 200:
            code = data.get("error", {}).get("message", "UNKNOWN_ERROR")
            raise FirebaseError(_friendly_auth_message(code), code=code)
        return data

    def sign_up(self, email: str, password: str) -> Dict[str, Any]:
        return self._auth_post("accounts:signUp", {
            "email": email, "password": password, "returnSecureToken": True,
        })

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        return self._auth_post("accounts:signInWithPassword", {
            "email": email, "password": password, "returnSecureToken": True,
        })

    def sign_in_with_google_id_token(self, google_id_token: str) -> Dict[str, Any]:
        return self._auth_post("accounts:signInWithIdp", {
            "postBody": f"id_token={google_id_token}&providerId=google.com",
            "requestUri": self.app_url,
            "returnSecureToken": True,
            "returnIdpCredential": True,
        })

    def send_password_reset(self, email: str) -> None:
        self._auth_post("accounts:sendOobCode", {
            "requestType": "PASSWORD_RESET", "email": email,
        })

    def refresh_id_token(self, refresh_token: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{SECURE_TOKEN_URL}/token?key={self.api_key}",
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            timeout=REQUEST_TIMEOUT,
        )
        data = resp.json() if resp.content else {}
        if resp.status_code != 200:
            raise FirebaseError("Session expired. Please sign in again.", code="TOKEN_EXPIRED")
        return data

    @staticmethod
    def session_from_auth(auth: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize an Identity Toolkit response into our session dict."""
        return {
            "uid": auth.get("localId", ""),
            "email": auth.get("email", ""),
            "display_name": auth.get("displayName") or auth.get("email", "").split("@")[0],
            "photo_url": auth.get("photoUrl", ""),
            "id_token": auth.get("idToken", ""),
            "refresh_token": auth.get("refreshToken", ""),
            "token_expiry": time.time() + int(auth.get("expiresIn", "3600")),
        }

    # ---------------------------- Firestore ------------------------------

    def _headers(self, id_token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {id_token}", "Content-Type": "application/json"}

    def _fs_request(self, method: str, path: str, id_token: str,
                    params: Optional[Dict[str, Any]] = None,
                    body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = requests.request(
            method, f"{self._fs_base}/{path}", headers=self._headers(id_token),
            params=params, json=body, timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 404:
            return {}
        if resp.status_code != 200:
            detail = ""
            try:
                detail = resp.json().get("error", {}).get("message", "")
            except ValueError:
                detail = resp.text[:200]
            if resp.status_code in (401, 403):
                raise FirebaseError(
                    "Firestore denied the request. Publish the security rules from the setup "
                    f"screen and sign in again. ({detail})", code="PERMISSION_DENIED")
            raise FirebaseError(f"Firestore error {resp.status_code}: {detail}", code="FIRESTORE")
        return resp.json() if resp.content else {}

    def user_path(self, uid: str) -> str:
        return f"users/{uid}"

    def get_document(self, uid: str, collection: str, doc_id: str, id_token: str) -> Optional[Dict[str, Any]]:
        raw = self._fs_request("GET", f"{self.user_path(uid)}/{collection}/{doc_id}", id_token)
        if not raw or "fields" not in raw:
            return None
        return decode_document(raw)

    def list_documents(self, uid: str, collection: str, id_token: str,
                       page_size: int = 500) -> List[Dict[str, Any]]:
        raw = self._fs_request("GET", f"{self.user_path(uid)}/{collection}", id_token,
                               params={"pageSize": page_size})
        return [decode_document(d) for d in raw.get("documents", [])]

    def create_document(self, uid: str, collection: str, data: Dict[str, Any],
                        id_token: str, doc_id: Optional[str] = None) -> Dict[str, Any]:
        if doc_id is None:
            doc_id = uuid.uuid4().hex
        data = {**data, "id": doc_id}
        raw = self._fs_request(
            "POST", f"{self.user_path(uid)}/{collection}", id_token,
            params={"documentId": doc_id}, body=encode_fields(data))
        return decode_document(raw) if raw else data

    def set_document(self, uid: str, collection: str, doc_id: str,
                     data: Dict[str, Any], id_token: str) -> Dict[str, Any]:
        """Upsert with field merge (PATCH + updateMask)."""
        data = {**data, "id": doc_id}
        params = [("updateMask.fieldPaths", k) for k in data.keys()]
        raw = self._fs_request(
            "PATCH", f"{self.user_path(uid)}/{collection}/{doc_id}", id_token,
            params=params, body=encode_fields(data))
        if not raw:  # 404 -> create
            return self.create_document(uid, collection, data, id_token, doc_id=doc_id)
        return decode_document(raw)

    def delete_document(self, uid: str, collection: str, doc_id: str, id_token: str) -> None:
        self._fs_request("DELETE", f"{self.user_path(uid)}/{collection}/{doc_id}", id_token)

    def delete_collection(self, uid: str, collection: str, id_token: str) -> int:
        docs = self.list_documents(uid, collection, id_token)
        for d in docs:
            self.delete_document(uid, collection, d["id"], id_token)
        return len(docs)
