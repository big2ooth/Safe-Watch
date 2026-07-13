import streamlit as st
import time

st.set_page_config(
    page_title="SafeWatch — Safety Console",
    page_icon="🦺",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.styles import load_styles
from dashboard.login import show_login
from dashboard.sidebar import show_sidebar
from dashboard.metrics import show_header, show_metrics, fetch_stats
from dashboard.charts import (
    show_charts, show_incident_log, show_zone_overview,
    show_worker_scores, fetch_violations
)
from dashboard.video import show_video

# ── Styles ──────────────────────────────────────────────────────────────────
load_styles()

# ── Auth ────────────────────────────────────────────────────────────────────
if not show_login():
    st.stop()

# ── Sidebar ─────────────────────────────────────────────────────────────────
filters = show_sidebar()

# ── Fetch data ───────────────────────────────────────────────────────────────
stats      = fetch_stats()
api_online = stats is not None
violations = fetch_violations(
    limit=filters["limit"],
    zone=filters["zone"] if filters["zone"] != "All" else None,
    violation=filters["violation"] if filters["violation"] != "All" else None
)

# ── Header ───────────────────────────────────────────────────────────────────
show_header(api_online, stats)

# ── Metrics ──────────────────────────────────────────────────────────────────
show_metrics(stats)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Video + Charts ───────────────────────────────────────────────────────────
video_col, charts_col = st.columns([1, 1])

with video_col:
    show_video()

with charts_col:
    show_charts(stats)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Incident log + Active alerts ─────────────────────────────────────────────
show_incident_log(violations)

# ── Zone overview ────────────────────────────────────────────────────────────
show_zone_overview(stats)

# ── Worker scores ────────────────────────────────────────────────────────────
show_worker_scores()

# ── Auto refresh ─────────────────────────────────────────────────────────────
if filters.get("auto_refresh"):
    rate_map = {"10s": 10, "30s": 30, "60s": 60}
    time.sleep(rate_map[filters["refresh_rate"]])
    st.rerun()