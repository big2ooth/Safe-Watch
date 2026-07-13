import streamlit as st
import sqlite3
from backend.config import API_BASE, DB_PATH


def show_sidebar() -> dict:
    """Renders sidebar, returns filter state as dict."""

    filters = {}

    with st.sidebar:
        st.markdown("### SafeWatch")

        user = st.session_state.user
        st.markdown(f"""
        <div style="background:#FAF7F4;border:1px solid #E8DFD8;border-radius:4px;padding:10px 12px;margin-bottom:16px">
            <div style="font-size:13px;font-weight:600;color:#1C1917">{user['full_name']}</div>
            <div style="margin-top:4px"><span class="role-badge">{user['role'].upper()}</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Filters**")

        try:
            import requests
            zones = ["All"] + requests.get(f"{API_BASE}/zones", timeout=2).json()
        except:
            zones = ["All"]

        filters["zone"]      = st.selectbox("Zone", zones)
        filters["violation"] = st.selectbox("Violation Type", ["All", "No Hardhat", "No Safety Vest"])
        filters["limit"]     = st.slider("Max Records", 10, 200, 30)

        st.markdown("---")
        st.markdown("**Auto-refresh**")
        filters["auto_refresh"]  = st.toggle("Enable", value=False)
        filters["refresh_rate"]  = st.selectbox("Interval", ["10s", "30s", "60s"])

        st.markdown("---")

        if user["role"] == "admin":
            if st.button("🗑 Clear DB", type="secondary", use_container_width=True):
                conn = sqlite3.connect(DB_PATH)
                conn.execute("DELETE FROM violations")
                conn.commit()
                conn.close()
                st.success("DB cleared")
                st.rerun()

        if st.button("Sign Out", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

        st.caption("Model: YOLOv8n  |  Backend: FastAPI")
        st.caption(f"API: {API_BASE}")

    return filters