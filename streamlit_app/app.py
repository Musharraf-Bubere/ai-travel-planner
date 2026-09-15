import html
from datetime import date

import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000/plan"


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "travel_plan": None,
    "request_data": None,
    "generation_error": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# PIPELINE CONFIGURATION
# ============================================================

PIPELINE_STEPS = [
    ("🔎", "Destination", "Destination research"),
    ("🏨", "Stay", "Accommodation research"),
    ("🎯", "Activities", "Activity research"),
    ("🌦️", "Weather", "Weather research"),
    ("🍴", "Food", "Restaurant research"),
    ("🗓️", "Itinerary", "Generate itinerary"),
    ("🔍", "Validation", "Validate itinerary"),
    ("🔄", "Refinement", "Repair if required"),
    ("✨", "Final Response", "Create final plan"),
]

PREFERENCE_OPTIONS = [
    "Beaches",
    "Food",
    "Relaxation",
    "Adventure",
    "Culture",
    "Nature",
    "Shopping",
    "Nightlife",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def esc(value) -> str:
    """Safely escape dynamic values before inserting them into HTML."""
    return html.escape(str(value))


def render_html(content: str) -> None:
    """Render trusted application HTML."""
    st.html(content.strip())


def safe_text(value, fallback: str = "Not available") -> str:
    if value is None:
        return fallback

    text = str(value).strip()

    return text if text else fallback


def format_budget(value) -> str:
    try:
        return f"₹{float(value):,.0f}"
    except (TypeError, ValueError):
        return "₹—"


def format_preferences(preferences: list[str]) -> str:
    if not preferences:
        return "No specific preferences"

    return " · ".join(
        preference.replace("_", " ").title()
        for preference in preferences
    )


def group_itinerary_by_day(itinerary: list[dict]) -> dict:
    days = {}

    for item in itinerary:
        day = item.get("day", 1)
        days.setdefault(day, []).append(item)

    return dict(sorted(days.items()))


def activity_icon(activity: str) -> str:
    text = activity.lower()

    if any(
        word in text
        for word in ["breakfast", "lunch", "dinner", "food", "restaurant"]
    ):
        return "🍴"

    if any(
        word in text
        for word in ["beach", "island", "water", "swim"]
    ):
        return "🏖️"

    if any(
        word in text
        for word in [
            "museum",
            "culture",
            "temple",
            "mosque",
            "church",
            "heritage",
        ]
    ):
        return "🏛️"

    if any(
        word in text
        for word in ["shopping", "mall", "market"]
    ):
        return "🛍️"

    if any(
        word in text
        for word in ["hotel", "check-in", "check in", "stay"]
    ):
        return "🏨"

    if any(
        word in text
        for word in ["relax", "spa", "leisure"]
    ):
        return "🧘"

    if any(
        word in text
        for word in ["night", "club", "bar", "evening"]
    ):
        return "🌙"

    if any(
        word in text
        for word in ["park", "garden", "nature", "waterfall"]
    ):
        return "🌿"

    return "📍"


def get_validation_summary(
    validation: dict,
    attempts: int,
) -> tuple[str, str, int]:
    is_valid = validation.get("is_valid", False)
    issues = validation.get("issues", [])

    if is_valid:
        return "Valid", "success", len(issues)

    return "Review", "warning", len(issues)


def get_pipeline_status(
    step_name: str,
    plan_exists: bool,
    validation: dict,
    validation_attempts: int,
    final_response_exists: bool = False,
) -> tuple[str, str, str]:
    """
    Return a visual status for the final state returned by the API.

    The sidebar does not pretend to receive live LangGraph events.
    It reflects what the completed API response actually contains.
    """
    if not plan_exists:
        return "○", "Waiting", "idle"

    is_valid = validation.get("is_valid", False)

    if step_name == "Validation":
        if is_valid:
            return (
                "✓",
                f"Passed · {validation_attempts} attempt(s)",
                "success",
            )

        return (
            "!",
            f"Review required · {validation_attempts} attempt(s)",
            "warning",
        )

    if step_name == "Refinement":
        if validation_attempts > 1:
            refinement_count = validation_attempts - 1

            if refinement_count == 1:
                return "↻", "Used once", "refined"

            return (
                "↻",
                f"Used {refinement_count} times",
                "refined",
            )

        return "→", "Not required", "skipped"

    if step_name == "Final Response":
        if final_response_exists:
            return "✓", "Ready", "success"

        return "—", "Not produced", "warning"

    return "✓", "Completed", "success"


def reset_plan() -> None:
    st.session_state["travel_plan"] = None
    st.session_state["request_data"] = None
    st.session_state["generation_error"] = None


def render_stat_card(
    icon: str,
    label: str,
    value: str,
    accent: str = "",
) -> None:
    render_html(
        f"""
        <div class="stat-card {accent}">
            <div class="stat-icon">{esc(icon)}</div>
            <div class="stat-content">
                <div class="stat-label">{esc(label)}</div>
                <div class="stat-value">{esc(value)}</div>
            </div>
        </div>
        """
    )


# ============================================================
# CUSTOM STYLING — CONSOLIDATED UI SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --bg: #080b12;
        --panel: #10151f;
        --panel-2: #151b27;
        --panel-3: #1b2230;
        --border: rgba(148, 163, 184, 0.20);
        --border-strong: rgba(148, 163, 184, 0.32);
        --text: #f8fafc;
        --text-soft: #d7dee9;
        --muted: #a5b1c2;
        --blue: #60a5fa;
        --green: #4ade80;
        --purple: #a78bfa;
        --gold: #fbbf24;
        --danger: #fb7185;
        --radius-lg: 24px;
        --radius-md: 16px;
        --radius-sm: 12px;
    }

    /* ---------- APP ---------- */
    html, body,
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 85% 0%, rgba(59,130,246,.09), transparent 27%),
            radial-gradient(circle at 5% 45%, rgba(124,58,237,.055), transparent 24%),
            var(--bg) !important;
        color: var(--text) !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 1520px !important;
        padding: 2.2rem 2.6rem 5rem !important;
    }

    /* ---------- BASE TYPOGRAPHY ---------- */
    h1, h2, h3, h4 {
        color: var(--text) !important;
        letter-spacing: -0.025em !important;
        font-weight: 800 !important;
    }

    h1 { font-size: 2.55rem !important; line-height: 1.1 !important; }
    h2 { font-size: 1.95rem !important; line-height: 1.2 !important; margin-top: 1.65rem !important; }
    h3 { font-size: 1.35rem !important; line-height: 1.25 !important; }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: var(--text-soft) !important;
        font-size: 1.05rem !important;
        line-height: 1.78 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
        font-size: .92rem !important;
        line-height: 1.6 !important;
    }

    /* ---------- SIDEBAR: NEVER FORCE ITS WIDTH ---------- */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #0d121a 0%, #080b11 100%) !important;
        border-right: 1px solid rgba(148,163,184,.16) !important;
    }

    /* Keep the expanded pipeline comfortably readable without
       interfering with Streamlit's collapsed-sidebar behavior. */
    section[data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 340px !important;
        max-width: 340px !important;
    }

    section[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 340px !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding: 1.15rem .95rem 1.5rem !important;
    }

    .sidebar-brand { padding: .35rem .2rem 1rem; }
    .sidebar-brand-title {
        color: #fff !important;
        font-size: 1.32rem !important;
        line-height: 1.3 !important;
        font-weight: 850 !important;
        margin-bottom: .35rem;
    }
    .sidebar-brand-subtitle {
        color: #b8c4d4 !important;
        font-size: .92rem !important;
        line-height: 1.6 !important;
    }

    .sidebar-status {
        display: flex;
        align-items: center;
        gap: .6rem;
        min-height: 46px;
        padding: .75rem .82rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(96,165,250,.20);
        border-radius: 12px;
        background: rgba(96,165,250,.055);
        color: #dbeafe !important;
        font-size: .91rem !important;
        line-height: 1.5 !important;
    }

    .sidebar-status-dot {
        width: 8px; height: 8px; border-radius: 50%; flex: 0 0 auto;
        background: #60a5fa;
        box-shadow: 0 0 10px rgba(96,165,250,.45);
    }
    .sidebar-status-dot.complete {
        background: #4ade80;
        box-shadow: 0 0 10px rgba(74,222,128,.45);
    }
    .sidebar-status-text { color: #dbe4f0 !important; }

    .pipeline-group {
        padding: .72rem;
        border: 1px solid rgba(148,163,184,.15);
        border-radius: 16px;
        background: rgba(255,255,255,.018);
    }
    .pipeline-group-label {
        color: #b9c5d5 !important;
        font-size: .78rem !important;
        font-weight: 850 !important;
        letter-spacing: .13em !important;
        text-transform: uppercase;
        margin: .15rem .1rem .65rem;
    }

    .pipeline-card {
        position: relative;
        -webkit-font-smoothing: antialiased;
        padding: 1rem .82rem;
        margin-bottom: .48rem;
        border: 1px solid rgba(148,163,184,.18);
        border-radius: 13px;
        background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.018));
        box-shadow: 0 5px 16px rgba(0,0,0,.12);
    }
    .pipeline-card.success {
        border-color: rgba(74,222,128,.28);
        background: linear-gradient(145deg, rgba(34,197,94,.055), rgba(255,255,255,.018));
    }
    .pipeline-card.warning { border-color: rgba(251,191,36,.34); }
    .pipeline-card.refined {
        border-color: rgba(192,132,252,.34);
        background: linear-gradient(145deg, rgba(168,85,247,.06), rgba(255,255,255,.018));
    }
    .pipeline-card.skipped { opacity: .58; }
    .pipeline-top { display:flex; align-items:center; gap:.55rem; }
    .pipeline-icon {
        width: 2rem; height: 2rem; flex: 0 0 auto;
        display:flex; align-items:center; justify-content:center;
        border-radius: 10px;
        background: rgba(255,255,255,.065);
        border: 1px solid rgba(255,255,255,.06);
        font-size: 1.18rem;
    }
    .pipeline-name {
        color: #f8fafc !important;
        font-size: 1.08rem !important;
        line-height: 1.3 !important;
        font-weight: 820 !important;
    }
    .pipeline-description {
        margin: .28rem 0 0 2.55rem;
        color: #cbd5e1 !important;
        font-size: .87rem !important;
        line-height: 1.55 !important;
    }
    .pipeline-status {
        margin: .34rem 0 0 2.55rem;
        color: #b9c5d5 !important;
        font-size: .86rem !important;
        line-height: 1.5 !important;
        font-weight: 720 !important;
    }
    .pipeline-status.success { color: #86efac !important; }
    .pipeline-status.warning { color: #fcd34d !important; }
    .pipeline-status.refined { color: #d8b4fe !important; }
    .pipeline-connector {
        height: .62rem;
        margin: -.02rem 0 -.02rem 1.62rem;
        border-left: 1px dashed rgba(148,163,184,.38);
    }
    .parallel-badge {
        margin: .62rem 0 .45rem;
        padding: .48rem .55rem;
        border: 1px solid rgba(96,165,250,.22);
        border-radius: 9px;
        background: rgba(59,130,246,.08);
        color: #bfdbfe !important;
        text-align:center;
        font-size: .75rem !important;
        font-weight: 750 !important;
    }
    .workflow-legend {
        margin-top: .85rem;
        padding: .72rem;
        border: 1px solid rgba(148,163,184,.13);
        border-radius: 12px;
        background: rgba(255,255,255,.016);
    }
    .workflow-legend-title {
        color:#cbd5e1 !important;
        font-size:.74rem !important;
        font-weight:800 !important;
        letter-spacing:.08em !important;
        text-transform:uppercase;
        margin-bottom:.38rem;
    }
    .workflow-legend-item {
        display:inline-block;
        margin:.12rem .12rem .12rem 0;
        padding:.28rem .42rem;
        border:1px solid rgba(148,163,184,.12);
        border-radius:999px;
        background:rgba(255,255,255,.025);
        color:#cbd5e1 !important;
        font-size:.73rem !important;
    }
    .sidebar-footer {
        padding-top:.75rem;
        margin-top:.8rem;
        border-top:1px solid rgba(148,163,184,.10);
        color:#8794a8 !important;
        font-size:.72rem !important;
        line-height:1.55 !important;
        text-align:center;
    }

    /* ---------- HERO ---------- */
    .hero {
        position:relative;
        overflow:hidden;
        min-height:270px;
        padding:2.7rem 2.75rem;
        margin-bottom:1.55rem;
        border:1px solid rgba(96,165,250,.24);
        border-radius:26px;
        background:
            radial-gradient(circle at 90% 5%, rgba(96,165,250,.18), transparent 30%),
            radial-gradient(circle at 10% 110%, rgba(167,139,250,.09), transparent 34%),
            linear-gradient(135deg, rgba(30,58,110,.52), rgba(18,24,38,.88));
        box-shadow:0 22px 55px rgba(0,0,0,.20), inset 0 1px 0 rgba(255,255,255,.04);
    }
    .hero-eyebrow {
        color:#bfdbfe !important;
        font-size:.70rem !important;
        font-weight:850 !important;
        letter-spacing:.18em !important;
        text-transform:uppercase;
        margin-bottom:.55rem;
    }
    .hero-title {
        color:#fff !important;
        font-size:3.45rem !important;
        line-height:1.04 !important;
        font-weight:900 !important;
        letter-spacing:-.045em !important;
        margin-bottom:.48rem;
    }
    .hero-subtitle {
        color:#e2e8f0 !important;
        font-size:1.28rem !important;
        line-height:1.4 !important;
        font-weight:760 !important;
        margin-bottom:.65rem;
    }
    .hero-description {
        max-width:1060px;
        color:#cbd5e1 !important;
        font-size:.96rem !important;
        line-height:1.75 !important;
    }
    .hero-pills { display:flex; flex-wrap:wrap; gap:.45rem; margin-top:1.05rem; }
    .hero-pill {
        padding:.42rem .66rem;
        border:1px solid rgba(148,163,184,.20);
        border-radius:999px;
        background:rgba(255,255,255,.055);
        color:#dbeafe !important;
        font-size:.72rem !important;
        font-weight:650 !important;
        backdrop-filter:blur(8px);
    }

    /* ---------- SECTION / FORM ---------- */
    .section-kicker {
        color:#94a3b8 !important;
        font-size:.70rem !important;
        font-weight:850 !important;
        letter-spacing:.16em !important;
        text-transform:uppercase;
        margin:.2rem 0 .15rem;
    }
    .section-description {
        color:#9aa8ba !important;
        font-size:.92rem !important;
        line-height:1.65 !important;
        margin-top:-.55rem;
        margin-bottom:.85rem;
    }
    .form-card {
        padding:1.25rem 1.25rem .9rem;
        border:1px solid rgba(148,163,184,.17);
        border-radius:20px;
        background:linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.014));
        box-shadow:0 18px 45px rgba(0,0,0,.13);
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stDateInput"] label,
    div[data-testid="stMultiSelect"] label {
        color:#e2e8f0 !important;
        font-size:1.05rem !important;
        font-weight:750 !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input {
        min-height:46px !important;
        border-radius:12px !important;
        border:1px solid rgba(148,163,184,.20) !important;
        background:#181e29 !important;
        color:#f8fafc !important;
        font-size:1.05rem !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stDateInput"] input:focus {
        border-color:rgba(96,165,250,.65) !important;
        box-shadow:0 0 0 3px rgba(96,165,250,.10) !important;
    }
    div[data-testid="stMultiSelect"] > div {
        min-height:46px !important;
        border-radius:12px !important;
        border:1px solid rgba(148,163,184,.20) !important;
        background:#181e29 !important;
    }
    div[data-testid="stMultiSelect"] span { font-size:.92rem !important; }
    .duration-preview {
        padding:.72rem .85rem;
        border:1px solid rgba(96,165,250,.18);
        border-radius:12px;
        background:rgba(59,130,246,.06);
        color:#bfdbfe !important;
        font-size:.82rem !important;
        line-height:1.55 !important;
    }
    .generate-hint {
        color:#8492a6 !important;
        text-align:center;
        font-size:.75rem !important;
        margin-top:.5rem;
    }

    div.stButton > button {
        min-height:2.8rem !important;
        border-radius:12px !important;
        font-size:.96rem !important;
        font-weight:760 !important;
        transition:transform .15s ease, box-shadow .15s ease;
    }
    div.stButton > button:hover {
        transform:translateY(-1px);
        box-shadow:0 10px 24px rgba(0,0,0,.20);
    }
    div.stButton > button[kind="primary"] {
        min-height:3.15rem !important;
        font-size:1.05rem !important;
        border:1px solid rgba(255,255,255,.14) !important;
        box-shadow:0 12px 28px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.14);
    }

    /* ---------- RESULT ---------- */
    .section-divider {
        height:1px;
        margin:1.75rem 0;
        background:linear-gradient(90deg, transparent, rgba(148,163,184,.18), transparent);
    }
    .result-kicker {
        color:#94a3b8 !important;
        font-size:.70rem !important;
        font-weight:850 !important;
        letter-spacing:.16em !important;
        text-transform:uppercase;
    }
    .result-title {
        color:#fff !important;
        font-size:2.85rem !important;
        line-height:1.08 !important;
        font-weight:900 !important;
    }
    .result-subtitle {
        color:#9aa8ba !important;
        font-size:.92rem !important;
        line-height:1.65 !important;
        margin-bottom:1rem;
    }
    .result-banner {
        display:flex; align-items:center; gap:.62rem;
        padding:.82rem .95rem;
        margin-bottom:.9rem;
        border:1px solid rgba(74,222,128,.20);
        border-radius:13px;
        background:rgba(34,197,94,.06);
        color:#bbf7d0 !important;
        font-size:.86rem !important;
        line-height:1.55 !important;
    }
    .result-banner.warning {
        border-color:rgba(251,191,36,.22);
        background:rgba(245,158,11,.065);
        color:#fef3c7 !important;
    }
    .snapshot-note {
        padding:.82rem .95rem;
        margin-bottom:1rem;
        border:1px solid rgba(148,163,184,.15);
        border-radius:13px;
        background:rgba(255,255,255,.018);
        color:#cbd5e1 !important;
        font-size:.84rem !important;
        line-height:1.65 !important;
    }
    .stat-card {
        display:flex; align-items:center; gap:.72rem;
        min-height:88px;
        padding:.9rem .95rem;
        border:1px solid rgba(148,163,184,.17);
        border-radius:16px;
        background:linear-gradient(145deg, rgba(255,255,255,.04), rgba(255,255,255,.016));
        box-shadow:0 8px 24px rgba(0,0,0,.09);
    }
    .stat-card.blue { border-color:rgba(96,165,250,.22); }
    .stat-card.green { border-color:rgba(74,222,128,.22); }
    .stat-card.purple { border-color:rgba(192,132,252,.22); }
    .stat-card.gold { border-color:rgba(251,191,36,.22); }
    .stat-icon {
        width:2.25rem; height:2.25rem; flex:0 0 auto;
        display:flex; align-items:center; justify-content:center;
        border-radius:10px; background:rgba(255,255,255,.065); font-size:1.05rem;
    }
    .stat-label { color:#9aa8ba !important; font-size:.73rem !important; font-weight:750 !important; text-transform:uppercase; letter-spacing:.06em; }
    .stat-value { color:#fff !important; font-size:1.08rem !important; font-weight:820 !important; margin-top:.12rem; }

    .content-card, .recommendation-card {
        height:100%;
        padding:1.15rem 1.18rem;
        border:1px solid rgba(148,163,184,.17);
        border-radius:17px;
        background:linear-gradient(145deg, rgba(255,255,255,.035), rgba(255,255,255,.014));
        box-shadow:0 8px 24px rgba(0,0,0,.08);
    }
    .content-card-title { color:#fff !important; font-size:1.10rem !important; font-weight:820 !important; margin-bottom:.4rem; }
    .content-card-text, .recommendation-text { color:#cbd5e1 !important; font-size:.96rem !important; line-height:1.75 !important; }
    .why-card { min-height:150px; }
    .why-icon { font-size:1.45rem; margin-bottom:.45rem; }
    .why-title { color:#fff !important; font-size:1.05rem !important; font-weight:820 !important; margin-bottom:.28rem; }
    .why-text { color:#b6c1d0 !important; font-size:.90rem !important; line-height:1.7 !important; }
    .recommendation-label { color:#aeb9c9 !important; font-size:.75rem !important; font-weight:850 !important; letter-spacing:.10em; text-transform:uppercase; margin-bottom:.42rem; }

    /* ---------- ITINERARY ---------- */
    .day-header {
        display:flex; align-items:center; justify-content:space-between; gap:1rem;
        padding:.82rem 0 .86rem;
        border-bottom:1px solid rgba(148,163,184,.14);
    }
    .day-title { color:#fff !important; font-size:1.42rem !important; font-weight:850 !important; }
    .day-count { color:#c4cfdd !important; font-size:.76rem !important; padding:.34rem .58rem; border:1px solid rgba(148,163,184,.14); border-radius:999px; background:rgba(255,255,255,.03); }
    .timeline-item {
        display:grid;
        grid-template-columns:112px minmax(0,1fr);
        gap:1.15rem;
        padding:1rem 0;
    }
    .timeline-item + .timeline-item { border-top:1px solid rgba(148,163,184,.09); }
    .timeline-time { color:#93c5fd !important; font-size:.84rem !important; font-weight:820 !important; letter-spacing:.04em; text-transform:uppercase; padding-top:.25rem; }
    .timeline-title { color:#fff !important; font-size:1.18rem !important; line-height:1.4 !important; font-weight:820 !important; margin-bottom:.25rem; }
    .timeline-location { color:#9aa8ba !important; font-size:.96rem !important; line-height:1.58 !important; margin-bottom:.35rem; }
    .timeline-description { color:#d3dbe7 !important; font-size:.94rem !important; line-height:1.75 !important; }

    /* ---------- TIPS / VALIDATION / EMPTY ---------- */
    .tip-card { display:flex; gap:.65rem; align-items:flex-start; padding:.9rem 1rem; margin-bottom:.5rem; border:1px solid rgba(96,165,250,.17); border-radius:13px; background:rgba(59,130,246,.06); color:#dbeafe !important; font-size:.94rem !important; line-height:1.75 !important; }
    .validation-hero { padding:1.15rem; border:1px solid rgba(74,222,128,.18); border-radius:17px; background:rgba(34,197,94,.045); }
    .validation-hero.warning { border-color:rgba(251,191,36,.20); background:rgba(245,158,11,.045); }
    .validation-title { color:#f8fafc !important; font-size:1.12rem !important; font-weight:830 !important; }
    .validation-subtitle { color:#aeb9c9 !important; font-size:.84rem !important; line-height:1.55 !important; margin-top:.2rem; }
    .validation-check { color:#bfeccf !important; font-size:.90rem !important; line-height:1.55 !important; padding:.38rem 0; }
    .validation-ok { color:#86efac !important; }
    .validation-issue { padding:.72rem .82rem; margin-top:.4rem; border:1px solid rgba(251,191,36,.18); border-radius:10px; background:rgba(245,158,11,.06); color:#fde68a !important; font-size:.82rem !important; line-height:1.6 !important; }
    .empty-state { padding:2.5rem 1.5rem; margin-top:.5rem; border:1px dashed rgba(148,163,184,.22); border-radius:22px; background:radial-gradient(circle at 50% 0%, rgba(96,165,250,.065), transparent 48%), rgba(255,255,255,.009); text-align:center; }
    .empty-state-icon { font-size:2.3rem; margin-bottom:.35rem; }
    .empty-state-title { color:#fff !important; font-size:1.55rem !important; font-weight:830 !important; margin-bottom:.35rem; }
    .empty-state-text { max-width:780px; margin:0 auto; color:#aeb9c9 !important; font-size:.94rem !important; line-height:1.75 !important; }
    .footer { color:#66758a !important; font-size:.70rem !important; text-align:center; padding-top:.95rem; }

    /* ---------- STREAMLIT NATIVE COMPONENTS ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] { border-radius:18px !important; border-color:rgba(148,163,184,.16) !important; background:rgba(255,255,255,.012) !important; }
    div[data-testid="stMetric"] { padding:.62rem .7rem; border-radius:11px; background:rgba(255,255,255,.025); border:1px solid rgba(148,163,184,.12); }
    div[data-testid="stMetricLabel"] { font-size:.72rem !important; color:#9aa8ba !important; }
    div[data-testid="stMetricValue"] { font-size:1.18rem !important; color:#f8fafc !important; }
    div[data-testid="stAlert"] { border-radius:13px !important; font-size:.94rem !important; }

    /* ---------- WORKFLOW STATE ---------- */
    .workflow-state {
        display:flex;
        align-items:center;
        gap:.85rem;
        padding:1rem 1.05rem;
        margin:.95rem 0 1.15rem;
        border-radius:16px;
        border:1px solid rgba(74,222,128,.20);
        background:linear-gradient(135deg, rgba(34,197,94,.075), rgba(255,255,255,.018));
    }
    .workflow-state.review {
        border-color:rgba(251,191,36,.24);
        background:linear-gradient(135deg, rgba(245,158,11,.075), rgba(255,255,255,.018));
    }
    .workflow-state-icon {
        width:2.25rem;
        height:2.25rem;
        flex:0 0 auto;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:11px;
        background:rgba(74,222,128,.11);
        color:#86efac;
        font-size:1.15rem;
        font-weight:900;
    }
    .workflow-state.review .workflow-state-icon {
        background:rgba(251,191,36,.11);
        color:#fcd34d;
    }
    .workflow-state-title {
        color:#f8fafc !important;
        font-size:1.05rem !important;
        line-height:1.35 !important;
        font-weight:850 !important;
    }
    .workflow-state-text {
        color:#aeb9c9 !important;
        font-size:.82rem !important;
        line-height:1.55 !important;
        margin-top:.15rem;
    }

    /* ---------- VALIDATION DETAILS ---------- */
    .validation-issues-heading {
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:.7rem;
        margin:.9rem 0 .55rem;
        color:#f8fafc;
        font-size:.88rem;
        font-weight:800;
    }
    .validation-issues-count {
        min-width:1.55rem;
        padding:.18rem .45rem;
        border-radius:999px;
        border:1px solid rgba(251,191,36,.22);
        background:rgba(245,158,11,.08);
        color:#fcd34d;
        text-align:center;
        font-size:.68rem;
    }
    .validation-issue {
        display:flex !important;
        align-items:flex-start;
        gap:.7rem;
        padding:.85rem .9rem !important;
        margin-top:.45rem !important;
        border-radius:11px !important;
        border:1px solid rgba(251,191,36,.16) !important;
        background:rgba(245,158,11,.045) !important;
        color:#f5e7b5 !important;
        font-size:.90rem !important;
        line-height:1.65 !important;
    }
    .validation-issue-icon {
        display:inline-flex;
        align-items:center;
        justify-content:center;
        width:1.25rem;
        height:1.25rem;
        flex:0 0 auto;
        border-radius:50%;
        background:rgba(251,191,36,.12);
        color:#fcd34d;
        font-size:.72rem;
        font-weight:900;
    }

    /* ---------- SIDEBAR STATE ---------- */
    .sidebar-status.review {
        border-color:rgba(251,191,36,.20) !important;
        background:linear-gradient(135deg, rgba(245,158,11,.06), rgba(255,255,255,.018)) !important;
    }
    .sidebar-status-dot.review {
        background:#fbbf24 !important;
        box-shadow:0 0 9px rgba(251,191,36,.35);
    }

    /* ---------- RESPONSIVE ---------- */
    @media (max-width: 1000px) {
        .block-container { padding-left:1.25rem !important; padding-right:1.25rem !important; }
        .hero { padding:2rem 1.7rem; }
        .hero-title { font-size:2.75rem !important; }
    }
    @media (max-width: 700px) {
        .block-container { padding:1.2rem .8rem 3rem !important; }
        .hero { padding:1.6rem 1.2rem; border-radius:20px; }
        .hero-title { font-size:2.25rem !important; }
        .hero-subtitle { font-size:1.05rem !important; }
        .hero-description { font-size:.90rem !important; }
        h2 { font-size:1.6rem !important; }
        .timeline-item { grid-template-columns:1fr; gap:.25rem; }
        .timeline-time { padding-top:0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR — AI PLANNING PIPELINE
# ============================================================

with st.sidebar:
    plan_exists = st.session_state["travel_plan"] is not None
    result = st.session_state["travel_plan"] or {}

    validation = result.get("validation", {})
    validation_attempts = result.get("validation_attempts", 0)
    final_response_exists = bool(result.get("final_response"))

    render_html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🧠 AI Planning Pipeline</div>
            <div class="sidebar-brand-subtitle">
                Multi-agent travel workflow orchestrated by LangGraph
            </div>
        </div>
        """
    )

    if plan_exists:
        if final_response_exists and validation.get("is_valid", False):
            sidebar_status_text = "Plan verified · final response ready"
            sidebar_status_class = "complete"
        elif final_response_exists:
            sidebar_status_text = "Plan generated · review recommended"
            sidebar_status_class = "review"
        else:
            sidebar_status_text = "Workflow finished · final plan unavailable"
            sidebar_status_class = "review"

        render_html(
            f"""
            <div class="sidebar-status {sidebar_status_class}">
                <span class="sidebar-status-dot {sidebar_status_class}"></span>
                <span class="sidebar-status-text">
                    {esc(sidebar_status_text)}
                </span>
            </div>
            """
        )
    else:
        render_html(
            """
            <div class="sidebar-status">
                <span class="sidebar-status-dot ready"></span>
                <span class="sidebar-status-text">
                    Ready for a new travel request
                </span>
            </div>
            """
        )

    render_html(
        '<div class="pipeline-group">'
        '<div class="pipeline-group-label">Workflow</div>'
    )

    sequential_names = {
        "Destination",
        "Itinerary",
        "Validation",
        "Refinement",
        "Final Response",
    }

    for index, (icon, name, description) in enumerate(PIPELINE_STEPS):
        if name not in sequential_names:
            continue

        status_icon, status_text, status_class = get_pipeline_status(
            name,
            plan_exists,
            validation,
            validation_attempts,
            final_response_exists,
        )

        display_icon = status_icon if plan_exists else icon

        render_html(
            f"""
            <div class="pipeline-card {status_class}">
                <div class="pipeline-top">
                    <div class="pipeline-icon">{esc(display_icon)}</div>
                    <div class="pipeline-name">{esc(name)}</div>
                </div>

                <div class="pipeline-description">
                    {esc(description)}
                </div>

                <div class="pipeline-status {status_class}">
                    {esc(status_text)}
                </div>
            </div>
            """
        )

        if name == "Destination":
            render_html(
                '<div class="parallel-badge">'
                '⚡ Parallel research stage'
                '</div>'
            )

            for (
                parallel_icon,
                parallel_name,
                parallel_description,
            ) in PIPELINE_STEPS:
                if parallel_name not in {
                    "Stay",
                    "Activities",
                    "Weather",
                }:
                    continue

                p_icon, p_status, p_class = get_pipeline_status(
                    parallel_name,
                    plan_exists,
                    validation,
                    validation_attempts,
                    final_response_exists,
                )

                render_html(
                    f"""
                    <div class="pipeline-card {p_class}">
                        <div class="pipeline-top">
                            <div class="pipeline-icon">
                                {esc(p_icon if plan_exists else parallel_icon)}
                            </div>

                            <div class="pipeline-name">
                                {esc(parallel_name)}
                            </div>
                        </div>

                        <div class="pipeline-description">
                            {esc(parallel_description)}
                        </div>

                        <div class="pipeline-status {p_class}">
                            {esc(p_status)}
                        </div>
                    </div>
                    """
                )

            render_html(
                '<div class="pipeline-connector"></div>'
            )

        elif name != "Final Response":
            render_html(
                '<div class="pipeline-connector"></div>'
            )

    render_html("</div>")

    render_html(
        """
        <div class="workflow-legend">
            <div class="workflow-legend-title">
                Workflow patterns
            </div>

            <span class="workflow-legend-item">→ Sequential</span>
            <span class="workflow-legend-item">⚡ Parallel</span>
            <span class="workflow-legend-item">🔀 Conditional</span>
            <span class="workflow-legend-item">↻ Iterative</span>
        </div>

        <div class="sidebar-footer">
            LangGraph Orchestrator<br>
            Research → Plan → Validate → Refine → Respond
        </div>
        """
    )


# ============================================================
# MAIN PAGE — HERO
# ============================================================

render_html(
    """
    <div class="hero">
        <div class="hero-eyebrow">Multi-Agent AI System</div>

        <div class="hero-title">✈️ AI Travel Planner</div>

        <div class="hero-subtitle">
            Personalized travel planning powered by intelligent agents
        </div>

        <div class="hero-description">
            Research destinations, discover accommodation and activities,
            analyze weather, build a day-by-day itinerary, validate the plan,
            and automatically refine it when required.
        </div>

        <div class="hero-pills">
            <span class="hero-pill">🧠 LangGraph</span>
            <span class="hero-pill">🔎 Real-time research</span>
            <span class="hero-pill">⚡ Parallel agents</span>
            <span class="hero-pill">🔍 Validation</span>
            <span class="hero-pill">🔄 Iterative refinement</span>
        </div>
    </div>
    """
)


# ============================================================
# TRIP CONFIGURATION
# ============================================================

render_html(
    '<div class="section-kicker">Trip configuration</div>'
)

st.header("🧳 Plan Your Trip")

st.markdown(
    '<div class="section-description">'
    'Tell the AI planner what kind of trip you want.'
    '</div>',
    unsafe_allow_html=True,
)

render_html('<div class="form-card">')

form_col1, form_col2 = st.columns([1.55, 1])

with form_col1:
    destination = st.text_input(
        "📍 Destination",
        placeholder="e.g. Goa, Mumbai, Dubai",
        help="Enter a city or destination for the travel research agents.",
    )

with form_col2:
    travelers = st.number_input(
        "👥 Travelers",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        help="Number of people travelling.",
    )

date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input(
        "📅 Start Date",
        value=date.today(),
    )

with date_col2:
    end_date = st.date_input(
        "📅 End Date",
        value=date.today(),
    )

budget_col1, budget_col2 = st.columns([1, 2])

with budget_col1:
    budget = st.number_input(
        "💰 Total Budget (₹)",
        min_value=1.0,
        value=30000.0,
        step=1000.0,
        help="Total planned budget for the trip.",
    )

with budget_col2:
    selected_preferences = st.multiselect(
        "❤️ Travel Preferences",
        PREFERENCE_OPTIONS,
        default=[
            "Beaches",
            "Food",
            "Relaxation",
        ],
        help="Choose the interests the itinerary should prioritize.",
    )

if end_date > start_date:
    duration_preview = (end_date - start_date).days

    render_html(
        f"""
        <div class="duration-preview">
            📅 <strong>{duration_preview} day trip</strong>
            &nbsp;·&nbsp;
            {esc(start_date.strftime("%d %b %Y"))}
            → {esc(end_date.strftime("%d %b %Y"))}
            &nbsp;·&nbsp;
            👥 {esc(travelers)} traveler(s)
            &nbsp;·&nbsp;
            💰 {esc(format_budget(budget))}
        </div>
        """
    )
elif end_date == start_date:
    render_html(
        """
        <div class="duration-preview">
            ⚠️ Select an end date after the start date.
        </div>
        """
    )
else:
    render_html(
        """
        <div class="duration-preview">
            ⚠️ End date cannot be before the start date.
        </div>
        """
    )

st.write("")

button_col1, button_col2, button_col3 = st.columns(
    [1, 2, 1]
)

with button_col2:
    generate_plan = st.button(
        "✨ Generate My Travel Plan",
        type="primary",
        use_container_width=True,
    )

render_html(
    """
    <div class="generate-hint">
        Your request will be processed through the multi-agent planning workflow.
    </div>
    """
)

render_html("</div>")


# ============================================================
# GENERATE TRAVEL PLAN
# ============================================================

if generate_plan:
    st.session_state["generation_error"] = None

    if not destination.strip():
        st.error("Please enter a destination.")
        st.stop()

    if end_date <= start_date:
        st.error("End date must be after the start date.")
        st.stop()

    duration = (end_date - start_date).days

    preferences = [
        preference.lower()
        for preference in selected_preferences
    ]

    payload = {
        "destination": destination.strip(),
        "travel_dates": (
            f"{start_date.isoformat()} "
            f"to {end_date.isoformat()}"
        ),
        "duration": duration,
        "travelers": travelers,
        "budget": budget,
        "preferences": preferences,
    }

    with st.status(
        "✨ Building your travel plan...",
        expanded=True,
    ) as status:
        st.write("🔎 Researching the destination")
        st.write("⚡ Running stay, activities, and weather agents in parallel")
        st.write("🍴 Researching restaurant options")
        st.write("🗓️ Generating the day-by-day itinerary")
        st.write("🔍 Validating geographic and research consistency")
        st.write("🔄 Refining the itinerary when required")
        st.write("✨ Preparing the final response")

        try:
            response = requests.post(
                API_URL,
                json=payload,
                timeout=300,
            )

            if response.status_code == 200:
                result = response.json()

                st.session_state["travel_plan"] = result
                st.session_state["request_data"] = payload

                status.update(
                    label="✅ Travel plan generated successfully!",
                    state="complete",
                    expanded=False,
                )

                st.rerun()

            error_detail = "Unknown API error."

            try:
                error_detail = response.json().get(
                    "detail",
                    error_detail,
                )
            except ValueError:
                if response.text:
                    error_detail = response.text

            st.session_state["generation_error"] = (
                f"API Error: {error_detail}"
            )

            status.update(
                label="❌ Travel planning failed",
                state="error",
                expanded=True,
            )

        except requests.exceptions.ConnectionError:
            st.session_state["generation_error"] = (
                "FastAPI is not running. Start it with: "
                "uvicorn src.api.main:app --reload"
            )

            status.update(
                label="❌ FastAPI connection failed",
                state="error",
                expanded=True,
            )

        except requests.exceptions.Timeout:
            st.session_state["generation_error"] = (
                "The AI planning workflow took too long to complete. "
                "Please try again."
            )

            status.update(
                label="⏱️ Request timed out",
                state="error",
                expanded=True,
            )

        except requests.exceptions.RequestException as exc:
            st.session_state["generation_error"] = (
                f"Request failed: {exc}"
            )

            status.update(
                label="❌ Request failed",
                state="error",
                expanded=True,
            )


if st.session_state["generation_error"]:
    st.error(st.session_state["generation_error"])


# ============================================================
# DISPLAY TRAVEL PLAN
# ============================================================

if st.session_state["travel_plan"] is not None:
    result = st.session_state["travel_plan"]
    request_data = st.session_state["request_data"] or {}

    final_response = result.get("final_response", {})
    validation = result.get("validation", {})
    final_response_exists = bool(final_response)
    validation_attempts = result.get(
        "validation_attempts",
        0,
    )

    destination_name = safe_text(
        final_response.get(
            "destination",
            request_data.get("destination"),
        ),
        "Unknown destination",
    )

    duration = request_data.get("duration", 0)
    travelers_count = request_data.get("travelers", 0)
    total_budget = request_data.get("budget", 0)

    preferences = request_data.get(
        "preferences",
        [],
    )

    preferences_text = format_preferences(
        preferences
    )

    travel_dates = request_data.get(
        "travel_dates",
        "Dates not specified",
    )

    (
        validation_status,
        validation_class,
        issues_count,
    ) = get_validation_summary(
        validation,
        validation_attempts,
    )

    # ========================================================
    # RESULT HEADER
    # ========================================================

    if final_response_exists and validation.get("is_valid", False):
        result_state_title = "Your verified travel plan"
        result_state_text = (
            "The itinerary passed semantic and deterministic validation "
            f"after {validation_attempts} attempt(s)."
        )
        result_state_class = "verified"
        result_state_icon = "✓"
    elif final_response_exists:
        result_state_title = "Your travel plan"
        result_state_text = (
            "A travel plan was generated, but the validator still "
            "identified issues that should be reviewed."
        )
        result_state_class = "review"
        result_state_icon = "!"
    else:
        result_state_title = "Planning completed with review required"
        result_state_text = (
            "The workflow reached its validation limit without producing "
            "a final validated response."
        )
        result_state_class = "review"
        result_state_icon = "!"

    render_html(
        f"""
        <div class="workflow-state {result_state_class}">
            <div class="workflow-state-icon">{esc(result_state_icon)}</div>
            <div>
                <div class="workflow-state-title">{esc(result_state_title)}</div>
                <div class="workflow-state-text">{esc(result_state_text)}</div>
            </div>
        </div>
        """
    )

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    render_html(
        """
        <div class="result-kicker">Generated result</div>

        <div class="result-title">
            🌍 Your Travel Plan
        </div>

        <div class="result-subtitle">
            A research-informed itinerary generated and checked
            by the multi-agent planning workflow.
        </div>
        """
    )

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        render_stat_card(
            "📍",
            "Destination",
            destination_name,
            "blue",
        )

    with stat_col2:
        render_stat_card(
            "📅",
            "Duration",
            f"{duration} Days",
            "purple",
        )

    with stat_col3:
        render_stat_card(
            "👥",
            "Travelers",
            str(travelers_count),
            "green",
        )

    with stat_col4:
        render_stat_card(
            "💰",
            "Budget",
            format_budget(total_budget),
            "gold",
        )

    render_html(
        f"""
        <div class="snapshot-note">
            <strong>❤️ Preferences:</strong>
            {esc(preferences_text)}
            &nbsp;&nbsp;•&nbsp;&nbsp;
            <strong>📅 Travel dates:</strong>
            {esc(travel_dates)}
        </div>
        """
    )

    if validation.get("is_valid", False):
        render_html(
            f"""
            <div class="result-banner">
                <span>✅</span>
                <span>
                    <strong>Plan verified.</strong>
                    The itinerary passed validation after
                    {esc(validation_attempts)} attempt(s).
                </span>
            </div>
            """
        )
    else:
        render_html(
            f"""
            <div class="result-banner warning">
                <span>⚠️</span>
                <span>
                    <strong>Plan requires review.</strong>
                    Validation completed after
                    {esc(validation_attempts)} attempt(s).
                </span>
            </div>
            """
        )

    # ========================================================
    # QUICK ACTIONS
    # ========================================================

    action_col1, action_col2, action_col3 = st.columns(
        [1, 1, 1]
    )

    with action_col1:
        if st.button(
            "↻ Plan Another Trip",
            use_container_width=True,
        ):
            reset_plan()
            st.rerun()

    with action_col2:
        if st.button(
            "⬆ Back to Configuration",
            use_container_width=True,
        ):
            st.markdown(
                '<script>window.scrollTo({top: 0, behavior: "smooth"});</script>',
                unsafe_allow_html=True,
            )

    with action_col3:
        st.caption("")


    # ========================================================
    # TRIP OVERVIEW
    # ========================================================

    trip_summary = final_response.get(
        "trip_summary",
        "",
    )

    if trip_summary:
        st.header("📝 Trip Overview")

        with st.container(border=True):
            st.write(
                safe_text(
                    trip_summary,
                    "Trip summary unavailable.",
                )
            )


    # ========================================================
    # WHY THIS PLAN
    # ========================================================

    st.header("🧠 Why This Plan?")

    why_col1, why_col2, why_col3 = st.columns(3)

    why_cards = [
        (
            why_col1,
            "🎯",
            "Preference-aware",
            "The itinerary uses the travel preferences supplied in your request.",
        ),
        (
            why_col2,
            "🌦️",
            "Research-informed",
            "Destination, accommodation, activities, weather, and restaurant research feed the planning workflow.",
        ),
        (
            why_col3,
            "🔍",
            "Validated",
            "The itinerary is checked for semantic, geographic, duplicate, and research-grounding issues.",
        ),
    ]

    for column, icon, title, text in why_cards:
        with column:
            render_html(
                f"""
                <div class="content-card why-card">
                    <div class="why-icon">{esc(icon)}</div>
                    <div class="why-title">{esc(title)}</div>
                    <div class="why-text">{esc(text)}</div>
                </div>
                """
            )


    # ========================================================
    # DAY-BY-DAY ITINERARY
    # ========================================================

    itinerary = final_response.get(
        "itinerary",
        [],
    )

    if itinerary:
        st.header("🗓️ Day-by-Day Itinerary")

        days = group_itinerary_by_day(
            itinerary
        )

        for day, day_items in days.items():
            with st.container(border=True):
                render_html(
                    f"""
                    <div class="day-header">
                        <div class="day-title">
                            🗺️ Day {esc(day)}
                        </div>

                        <div class="day-count">
                            {esc(len(day_items))} planned item(s)
                        </div>
                    </div>
                    """
                )

                for item in day_items:
                    time = safe_text(
                        item.get("time"),
                        "Time not specified",
                    )

                    activity = safe_text(
                        item.get("activity"),
                        "Activity",
                    )

                    location = safe_text(
                        item.get("location"),
                        "Location unavailable",
                    )

                    description = safe_text(
                        item.get("description"),
                        "",
                    )

                    icon = activity_icon(
                        activity
                    )

                    render_html(
                        f"""
                        <div class="timeline-item">
                            <div class="timeline-time">
                                {esc(time)}
                            </div>

                            <div class="timeline-main">
                                <div class="timeline-title">
                                    {esc(icon)} {esc(activity)}
                                </div>

                                <div class="timeline-location">
                                    📍 {esc(location)}
                                </div>

                                <div class="timeline-description">
                                    {esc(description)}
                                </div>
                            </div>
                        </div>
                        """
                    )

    else:
        st.info(
            "No itinerary items were returned by the final response."
        )


    # ========================================================
    # ACCOMMODATION + FOOD
    # ========================================================

    st.header("🏨 Accommodation & 🍴 Food")

    accommodation_col, food_col = st.columns(2)

    accommodation_summary = final_response.get(
        "accommodation_summary",
        "",
    )

    food_summary = final_response.get(
        "food_summary",
        "",
    )

    with accommodation_col:
        render_html(
            f"""
            <div class="recommendation-card">
                <div class="recommendation-label">
                    🏨 Accommodation
                </div>

                <div class="recommendation-text">
                    {esc(
                        safe_text(
                            accommodation_summary,
                            "Accommodation information unavailable.",
                        )
                    )}
                </div>
            </div>
            """
        )

    with food_col:
        render_html(
            f"""
            <div class="recommendation-card">
                <div class="recommendation-label">
                    🍴 Food recommendations
                </div>

                <div class="recommendation-text">
                    {esc(
                        safe_text(
                            food_summary,
                            "Food recommendations unavailable.",
                        )
                    )}
                </div>
            </div>
            """
        )


    # ========================================================
    # TRAVEL TIPS
    # ========================================================

    travel_tips = final_response.get(
        "travel_tips",
        [],
    )

    if travel_tips:
        st.header("💡 Travel Tips")

        for tip in travel_tips:
            render_html(
                f"""
                <div class="tip-card">
                    <span>💡</span>
                    <span>{esc(safe_text(tip))}</span>
                </div>
                """
            )


    # ========================================================
    # VALIDATION SUMMARY
    # ========================================================

    st.header("🛡️ Plan Verification")

    if validation.get("is_valid", False):
        render_html(
            f"""
            <div class="validation-hero">
                <div class="validation-title">
                    ✓ Itinerary verified successfully
                </div>

                <div class="validation-subtitle">
                    {esc(validation_attempts)} validation attempt(s)
                    · {esc(issues_count)} remaining issue(s)
                </div>
            </div>
            """
        )
    else:
        render_html(
            f"""
            <div class="validation-hero warning">
                <div class="validation-title">
                    ⚠ Itinerary requires review
                </div>

                <div class="validation-subtitle">
                    {esc(validation_attempts)} validation attempt(s)
                    · {esc(issues_count)} issue(s)
                </div>
            </div>
            """
        )

    with st.expander(
        "🔍 View validation details",
        expanded=False,
    ):
        detail_col1, detail_col2, detail_col3 = st.columns(3)

        with detail_col1:
            st.metric(
                "Attempts",
                validation_attempts,
            )

        with detail_col2:
            st.metric(
                "Status",
                validation_status,
            )

        with detail_col3:
            st.metric(
                "Issues",
                issues_count,
            )

        st.write("")

        checks = [
            "Semantic itinerary validation",
            "Geographic consistency checks",
            "Duplicate-place checks",
            "Research-grounding checks",
            "Activity and restaurant grounding",
            "Automatic refinement when required",
        ]

        for check in checks:
            render_html(
                f"""
                <div class="validation-check validation-ok">
                    ✓ {esc(check)}
                </div>
                """
            )

        issues = validation.get(
            "issues",
            [],
        )

        if issues:
            st.write("")
            render_html(
                f"""
                <div class="validation-issues-heading">
                    <span>Remaining issues</span>
                    <span class="validation-issues-count">{esc(len(issues))}</span>
                </div>
                """
            )

            for issue in issues:
                render_html(
                    f"""
                    <div class="validation-issue">
                        <span class="validation-issue-icon">!</span>
                        <span>{esc(safe_text(issue))}</span>
                    </div>
                    """
                )
        else:
            st.success(
                "No validation issues detected."
            )


# ============================================================
# EMPTY STATE
# ============================================================

else:
    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    render_html(
        """
        <div class="empty-state">
            <div class="empty-state-icon">🌴</div>

            <div class="empty-state-title">
                Ready to plan your next trip?
            </div>

            <div class="empty-state-text">
                Enter your destination, dates, travelers, budget, and
                preferences above. The multi-agent system will research,
                plan, validate, and refine your itinerary before presenting
                the final travel plan.
            </div>
        </div>
        """
    )

    st.write("")

    st.subheader("🤖 What happens behind the scenes?")

    feature_col1, feature_col2, feature_col3 = st.columns(3)

    feature_cards = [
        (
            feature_col1,
            "🔎",
            "AI Research",
            "Specialized agents research destination information, accommodation, activities, weather, and restaurants.",
        ),
        (
            feature_col2,
            "⚡",
            "Multi-Agent Planning",
            "LangGraph coordinates sequential, parallel, conditional, and iterative workflow patterns.",
        ),
        (
            feature_col3,
            "🛡️",
            "Validation & Refinement",
            "The generated itinerary is validated and automatically refined when the validator identifies problems.",
        ),
    ]

    for column, icon, title, text in feature_cards:
        with column:
            render_html(
                f"""
                <div class="content-card">
                    <div class="why-icon">{esc(icon)}</div>
                    <div class="content-card-title">
                        {esc(title)}
                    </div>
                    <div class="content-card-text">
                        {esc(text)}
                    </div>
                </div>
                """
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="section-divider"></div>',
    unsafe_allow_html=True,
)

render_html(
    """
    <div class="footer">
        ✈️ AI Travel Planner — Multi-Agent Travel Planning System
        &nbsp;•&nbsp; LangGraph
        &nbsp;•&nbsp; LangChain
        &nbsp;•&nbsp; FastAPI
        &nbsp;•&nbsp; Streamlit
    </div>
    """
)
