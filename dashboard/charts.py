import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
from backend.config import API_BASE


def fetch_violations(limit: int = 50, zone: str = None, violation: str = None) -> list:
    try:
        params = {"limit": limit}
        if zone and zone != "All":
            params["zone"] = zone
        if violation and violation != "All":
            params["violation"] = violation
        r = requests.get(f"{API_BASE}/violations", params=params, timeout=3)
        return r.json()
    except:
        return []




def show_charts(stats: dict):
    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown("<div class='section-header'>Violations by Zone</div>", unsafe_allow_html=True)
        if stats and stats.get("by_zone"):
            zone_df = pd.DataFrame(stats["by_zone"])
            fig = px.bar(
                zone_df.sort_values("count", ascending=True),
                x="count", y="zone", orientation="h",
                color="count",
                color_continuous_scale=["#E8C2C2", "#C25555", "#7A1B26"]
            )
            fig.update_layout(
                plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", font_color="#6B5F57",
                showlegend=False, coloraxis_showscale=False,
                margin=dict(l=0, r=0, t=12, b=0),
                xaxis=dict(gridcolor="#F0E8E2", title=""),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", title=""),
                height=240
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div class="empty-state">No zone data yet</div>', unsafe_allow_html=True)

    with chart2:
        st.markdown("<div class='section-header'>Violation Trend (Today)</div>", unsafe_allow_html=True)
        if stats and stats.get("hourly"):
            hourly_df = pd.DataFrame(stats["hourly"])
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=hourly_df["hour"], y=hourly_df["count"],
                fill="tozeroy",
                fillcolor="rgba(122,27,38,0.07)",
                line=dict(color="#7A1B26", width=2),
                mode="lines+markers",
                marker=dict(color="#7A1B26", size=5)
            ))
            fig2.update_layout(
                plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", font_color="#6B5F57",
                margin=dict(l=0, r=0, t=12, b=0),
                xaxis=dict(gridcolor="#F0E8E2", title=""),
                yaxis=dict(gridcolor="#F0E8E2", title=""),
                height=240, showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div class="empty-state">No hourly data yet</div>', unsafe_allow_html=True)


def show_incident_log(violations: list):
    alert_col, log_col = st.columns([1, 2])

    # ─────────────────────────────────────────────
    # Active Alerts
    # ─────────────────────────────────────────────
    with alert_col:
        st.markdown(
            "<div class='section-header'>Active Alerts</div>",
            unsafe_allow_html=True,
        )

        unacked = [v for v in violations if not v.get("acknowledged")][:6]

        if not unacked:
            st.markdown(
                "<div style='color:#2D8A4E;font-size:13px;padding:16px 0;font-weight:600'>✓ No active violations</div>",
                unsafe_allow_html=True,
            )

        for v in unacked:
            ts = datetime.fromisoformat(v["timestamp"])
            mins_ago = int((datetime.now() - ts).total_seconds() / 60)

            is_critical = "Hardhat" in v["violation"]
            badge = "badge-critical" if is_critical else "badge-warning"
            severity = "CRITICAL" if is_critical else "WARNING"
            border_color = "#D93B3B" if is_critical else "#E0B23D"

            st.markdown(
                f"""
                <div class="violation-card" style="border-left:4px solid {border_color}">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                        <span class="alert-badge {badge}">{severity}</span>
                        <span style="font-size:11px;color:#A89A8E">{mins_ago}m ago</span>
                    </div>
                    <div style="font-size:13px;font-weight:600;color:#1C1917;margin-bottom:2px">
                        {v['violation']}
                    </div>
                    <div style="font-size:12px;color:#6B5F57">
                        {v['zone']} · Conf: {v['confidence']:.0%}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ─────────────────────────────────────────────
    # Incident Log
    # ─────────────────────────────────────────────
    with log_col:
        st.markdown(
            "<div class='section-header'>Incident Log</div>",
            unsafe_allow_html=True,
        )

        if not violations:
            st.markdown(
                '<div class="empty-state">No violations logged yet</div>',
                unsafe_allow_html=True,
            )
            return

        header = st.columns([1.3, 1.4, 2.5, 1, 1.2, 1])

        header[0].markdown("**Time**")
        header[1].markdown("**Zone**")
        header[2].markdown("**Violation**")
        header[3].markdown("**Conf**")
        header[4].markdown("**Severity**")
        header[5].markdown("**Evidence**")

        for v in violations:

            cols = st.columns([1.3, 1.4, 2.5, 1, 1.2, 1])

            cols[0].write(pd.to_datetime(v["timestamp"]).strftime("%H:%M:%S"))
            cols[1].write(v["zone"])
            cols[2].write(v["violation"])
            cols[3].write(f"{v['confidence']:.0%}")
            cols[4].write(
                "CRITICAL" if "Hardhat" in v["violation"] else "WARNING"
            )

            if cols[5].button("View", key=f"snap_{v['id']}"):
                if v.get("snapshot"):
                    filename = v["snapshot"].split("/")[-1]
                    st.session_state.snapshot = (
                        f"{API_BASE}/snapshots/{filename}"
                    )

        if "snapshot" in st.session_state:
            st.markdown("---")
            st.subheader("Violation Snapshot")
            st.image(
                st.session_state.snapshot,
                use_container_width=True,
            )
        else:
            st.markdown('<div class="empty-state">No violations logged yet</div>', unsafe_allow_html=True)


def show_zone_overview(stats: dict):
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Zone Risk Overview</div>", unsafe_allow_html=True)

    all_zones = ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]
    zone_data = {z["zone"]: z["count"] for z in stats.get("by_zone", [])} if stats else {}

    zone_cols = st.columns(len(all_zones))
    for i, zone in enumerate(all_zones):
        count = zone_data.get(zone, 0)
        risk  = "HIGH" if count > 20 else "MED" if count > 10 else "LOW"
        color = "#D93B3B" if count > 20 else "#E0B23D" if count > 10 else "#2D8A4E"
        with zone_cols[i]:
            st.markdown(f"""
            <div class="zone-card">
                <div style="font-size:10px;color:#A89A8E;margin-bottom:8px;font-weight:700;letter-spacing:0.06em">{zone.upper()}</div>
                <div style="font-family:'Barlow Condensed',sans-serif;font-size:30px;font-weight:800;color:{color}">{count}</div>
                <div style="font-size:10px;color:{color};margin-top:4px;font-weight:700;letter-spacing:0.06em">{risk}</div>
            </div>""", unsafe_allow_html=True)


