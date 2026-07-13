import streamlit as st
import hashlib
from backend.database import get_user


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def show_login() -> bool:
    """Returns True if user is logged in, False otherwise."""

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    if st.session_state.logged_in:
        return True

    # ── Login page styles ──
    st.markdown("""
    <style>
        .stApp { background-color: #7A1B26 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="login-brand">Safe<span>Watch</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-tagline">Construction Site Safety Monitor</div>', unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        with st.container(border=True):
            st.markdown("<div style='font-family:Barlow Condensed,sans-serif;font-size:20px;font-weight:700;color:#1C1917;margin-bottom:12px'>Sign In</div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter username", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Enter password", label_visibility="collapsed")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

            if st.button("Sign In →", type="primary", use_container_width=True):
                if username and password:
                    user = get_user(username, hash_password(password))
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both fields")

    st.markdown('<div class="login-footer">SafeWatch v2.0 · Powered by YOLOv8</div>', unsafe_allow_html=True)
    return False