import streamlit as st
import requests
from datetime import datetime
from backend.config import API_BASE


def show_header(api_online: bool, stats: dict):
    if not api_online:
        status_label, status_color = "API OFFLINE", "#E0B23D"
    elif stats and stats.get("unacknowledged", 0) > 0:
        status_label, status_color = "VIOLATIONS DETECTED", "#FFFFFF"
    else:
        status_label, status_color = "ALL CLEAR", "#FFFFFF"

    st.markdown(f"""
    <div class="sw-header">
        <div>
            <div class="brand">Safe<span>Watch</span></div>
            <div class="sub">Construction Site Safety Monitor</div>
        </div>
        <div>
            <div style="color:{status_color};font-weight:700;font-size:12px;letter-spacing:0.06em;font-family:'JetBrains Mono',monospace;text-align:right">
                <span class="live-dot"></span>{status_label}
            </div>
            <div class="live-row">{datetime.now().strftime('%d %b %Y, %H:%M:%S')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_metrics(stats: dict):
    unacked     = stats.get("unacknowledged", 0) if stats else 0
    today_count = stats.get("today", 0) if stats else 0
    no_hardhat  = stats.get("no_hardhat", 0) if stats else 0
    no_vest     = stats.get("no_vest", 0) if stats else 0

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-card danger">
            <div class="metric-label">Active Violations</div>
            <div class="metric-value">{unacked}</div>
            <div class="metric-sub">Unacknowledged alerts</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card brand">
            <div class="metric-label">Today's Incidents</div>
            <div class="metric-value">{today_count}</div>
            <div class="metric-sub">Since midnight</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card warning">
            <div class="metric-label">No Hardhat</div>
            <div class="metric-value">{no_hardhat}</div>
            <div class="metric-sub">Helmet violations</div>
        </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card warning">
            <div class="metric-label">No Safety Vest</div>
            <div class="metric-value">{no_vest}</div>
            <div class="metric-sub">Vest violations</div>
        </div>""", unsafe_allow_html=True)


def fetch_stats() -> dict:
    try:
        r = requests.get(f"{API_BASE}/violations/stats", timeout=3)
        return r.json()
    except:
        return None