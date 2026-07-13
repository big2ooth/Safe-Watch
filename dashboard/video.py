import streamlit as st
from backend.config import API_BASE


def show_video():
    st.markdown("<div class='section-header'>Live Feed</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#1C1917;border-radius:4px;padding:4px;border:2px solid #7A1B26">
        <img src="{API_BASE}/video_feed"
             style="width:100%;border-radius:2px;display:block"
             alt="Live Feed"/>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px;color:#A89A8E;margin-top:6px;font-family:'JetBrains Mono',monospace">
        STREAM: {API_BASE}/video_feed
    </div>
    """, unsafe_allow_html=True)