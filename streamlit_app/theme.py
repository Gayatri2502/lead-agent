"""Visual system: professional theme CSS, sidebar navigation, and UI primitives."""
from __future__ import annotations

import html
from typing import Callable, Dict, List, Optional

import streamlit as st
from streamlit_option_menu import option_menu

from .config import APP_ICON, APP_NAME, APP_TAGLINE

# Palette
SIDEBAR_BG = "#0B1220"
SIDEBAR_BORDER = "#1E293B"
ACCENT = "#4F46E5"
ACCENT_SOFT = "#EEF2FF"
TEXT_PRIMARY = "#0F172A"
TEXT_MUTED = "#64748B"
CARD_BORDER = "#E2E8F0"
PAGE_BG = "#F6F7FB"

MAIN_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, .stButton button {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}
.stApp {{ background-color: {PAGE_BG}; }}
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}

.block-container {{
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG};
    border-right: 1px solid {SIDEBAR_BORDER};
    min-width: 264px !important;
    max-width: 264px !important;
}}
section[data-testid="stSidebar"] > div {{ padding-top: 0.5rem; }}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] span {{ color: #CBD5E1; }}
section[data-testid="stSidebar"] hr {{ border-color: {SIDEBAR_BORDER}; margin: 0.75rem 0; }}

.vd-brand {{
    display: flex; align-items: center; gap: 12px;
    padding: 14px 10px 18px 10px;
}}
.vd-brand-logo {{
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; box-shadow: 0 4px 14px rgba(99,102,241,0.35);
}}
.vd-brand-name {{ color: #F8FAFC; font-weight: 700; font-size: 16px; letter-spacing: -0.01em; }}
.vd-brand-sub {{ color: #64748B; font-size: 11.5px; font-weight: 500; margin-top: 1px; }}

.vd-section {{
    color: #475569; font-size: 10.5px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 10px 12px 6px 12px;
}}

.vd-user-card {{
    background: #111A2E; border: 1px solid {SIDEBAR_BORDER};
    border-radius: 12px; padding: 12px; display: flex; gap: 10px; align-items: center;
}}
.vd-avatar {{
    width: 38px; height: 38px; border-radius: 50%;
    background: linear-gradient(135deg, #818CF8, #4F46E5);
    color: white; font-weight: 700; font-size: 14px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}}
.vd-user-name {{ color: #F1F5F9; font-weight: 600; font-size: 13.5px; line-height: 1.2; }}
.vd-user-email {{ color: #64748B; font-size: 11.5px; word-break: break-all; line-height: 1.2; }}

/* ---------- Main content primitives ---------- */
.vd-page-title {{
    font-size: 26px; font-weight: 800; color: {TEXT_PRIMARY};
    letter-spacing: -0.02em; margin: 0;
}}
.vd-page-desc {{ color: {TEXT_MUTED}; font-size: 14px; margin-top: 4px; }}

.vd-card {{
    background: white; border: 1px solid {CARD_BORDER};
    border-radius: 14px; padding: 20px 22px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}}
.vd-metric {{
    background: white; border: 1px solid {CARD_BORDER}; border-radius: 14px;
    padding: 16px 18px; height: 100%;
}}
.vd-metric-label {{
    color: {TEXT_MUTED}; font-size: 11px; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
}}
.vd-metric-value {{ color: {TEXT_PRIMARY}; font-size: 28px; font-weight: 800; margin-top: 6px; letter-spacing: -0.02em; }}
.vd-metric-sub {{ color: {TEXT_MUTED}; font-size: 12px; margin-top: 2px; }}

.vd-chip {{
    display: inline-block; padding: 3px 10px; border-radius: 999px;
    font-size: 11.5px; font-weight: 600;
}}
.vd-chip-green {{ background: #ECFDF5; color: #047857; }}
.vd-chip-amber {{ background: #FFFBEB; color: #B45309; }}
.vd-chip-red   {{ background: #FEF2F2; color: #B91C1C; }}
.vd-chip-blue  {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
.vd-chip-gray  {{ background: #F1F5F9; color: #475569; }}

.vd-empty {{
    text-align: center; padding: 56px 24px; color: {TEXT_MUTED};
}}
.vd-empty-icon {{ font-size: 40px; margin-bottom: 10px; }}
.vd-empty-title {{ font-size: 16px; font-weight: 700; color: {TEXT_PRIMARY}; }}
.vd-empty-sub {{ font-size: 13.5px; margin-top: 4px; }}

/* Buttons */
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {{
    background-color: {ACCENT}; border-color: {ACCENT}; font-weight: 600;
}}
.stButton > button[kind="primary"]:hover {{ background-color: #4338CA; border-color: #4338CA; }}
.stButton > button, .stFormSubmitButton > button {{ border-radius: 10px; font-weight: 600; }}

/* Inputs */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div,
.stTextArea textarea, .stNumberInput input, .stDateInput input, .stTimeInput input {{
    border-radius: 10px !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 8px 8px 0 0; font-weight: 600; }}

div[data-testid="stMetric"] {{ display: none; }}
</style>
"""


def inject_theme() -> None:
    st.markdown(MAIN_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

NAV_ITEMS: Dict[str, Dict[str, str]] = {
    "Dashboard": {"icon": "grid-1x2-fill", "desc": "Business overview"},
    "Appointments": {"icon": "calendar3", "desc": "Schedule & bookings"},
    "Customers": {"icon": "people", "desc": "Customer records"},
    "Calls": {"icon": "telephone", "desc": "Call history & transcripts"},
    "AI Training": {"icon": "cpu", "desc": "Train the receptionist model"},
    "Simulator": {"icon": "chat-left-dots", "desc": "Test conversations"},
    "Settings": {"icon": "gear", "desc": "Business & integrations"},
}


def _initials(name: str, email: str) -> str:
    parts = (name or "").split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    if name:
        return name[:2].upper()
    return (email[:2] or "U").upper()


def render_brand(agent_name: Optional[str] = None, business: Optional[str] = None) -> None:
    sub = f"{agent_name} · {business}" if agent_name and business else APP_TAGLINE
    st.markdown(
        f"""<div class="vd-brand">
            <div class="vd-brand-logo">{APP_ICON}</div>
            <div>
                <div class="vd-brand-name">{APP_NAME}</div>
                <div class="vd-brand-sub">{html.escape(sub)}</div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def render_sidebar(user: Dict, current_page: str, onboarding_complete: bool,
                   agent_name: str = "", business: str = "") -> str:
    """Render navigation sidebar. Returns the selected page name."""
    with st.sidebar:
        render_brand(agent_name or None, business or None)

        if not onboarding_complete:
            st.markdown('<div class="vd-section">Setup</div>', unsafe_allow_html=True)
            selected = option_menu(
                menu_title=None,
                options=["Receptionist Setup"],
                icons=["magic"],
                default_index=0,
                key="nav_setup",
                styles=_menu_styles(),
            ) or "Receptionist Setup"
        else:
            st.markdown('<div class="vd-section">Menu</div>', unsafe_allow_html=True)
            pages = list(NAV_ITEMS.keys())
            default_idx = pages.index(current_page) if current_page in pages else 0
            selected = option_menu(
                menu_title=None,
                options=pages,
                icons=[NAV_ITEMS[p]["icon"] for p in pages],
                default_index=default_idx,
                key="nav_main",
                styles=_menu_styles(),
            ) or current_page or "Dashboard"

        st.markdown("<div style='flex-grow:1'></div>", unsafe_allow_html=True)
        st.markdown("---")

        esc = html.escape
        st.markdown(
            f"""<div class="vd-user-card">
                <div class="vd-avatar">{esc(_initials(user.get("display_name", ""), user.get("email", "")))}</div>
                <div style="min-width:0">
                    <div class="vd-user-name">{esc(user.get("display_name") or "User")}</div>
                    <div class="vd-user-email">{esc(user.get("email", ""))}</div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Sign out", key="btn_signout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    return selected


def _menu_styles() -> Dict:
    return {
        "container": {"padding": "0 6px", "background-color": "transparent"},
        "icon": {"color": "#64748B", "font-size": "15px"},
        "nav-link": {
            "color": "#94A3B8", "font-size": "13.5px", "font-weight": "500",
            "border-radius": "10px", "margin": "2px 0", "padding": "9px 12px",
            "--hover-color": "#131E33",
        },
        "nav-link-selected": {
            "background-color": "rgba(99,102,241,0.16)", "color": "#E0E7FF",
            "font-weight": "600",
        },
    }


# ---------------------------------------------------------------------------
# Main-area primitives
# ---------------------------------------------------------------------------

def page_header(title: str, desc: str = "") -> None:
    st.markdown(f'<h1 class="vd-page-title">{html.escape(title)}</h1>', unsafe_allow_html=True)
    if desc:
        st.markdown(f'<div class="vd-page-desc">{html.escape(desc)}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)


def metric_card(label: str, value, sub: str = "") -> None:
    st.markdown(
        f"""<div class="vd-metric">
            <div class="vd-metric-label">{html.escape(label)}</div>
            <div class="vd-metric-value">{html.escape(str(value))}</div>
            <div class="vd-metric-sub">{html.escape(sub)}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def empty_state(icon: str, title: str, sub: str = "") -> None:
    st.markdown(
        f"""<div class="vd-card"><div class="vd-empty">
            <div class="vd-empty-icon">{icon}</div>
            <div class="vd-empty-title">{html.escape(title)}</div>
            <div class="vd-empty-sub">{html.escape(sub)}</div>
        </div></div>""",
        unsafe_allow_html=True,
    )


def status_chip(text: str, kind: str = "gray") -> str:
    return f'<span class="vd-chip vd-chip-{kind}">{html.escape(text)}</span>'


_APPT_CHIP = {"scheduled": "blue", "confirmed": "green", "completed": "gray", "cancelled": "red"}
_CALL_CHIP = {"completed": "green", "booked": "green", "missed": "amber", "failed": "red", "info": "blue"}


def chip_for(kind: str, value: str) -> str:
    mapping = _APPT_CHIP if kind == "appointment" else _CALL_CHIP
    return status_chip(value.replace("_", " ").title(), mapping.get(value, "gray"))
