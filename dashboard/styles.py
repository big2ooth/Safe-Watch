import streamlit as st


def load_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        .stApp { background-color: #FAF7F4; color: #1C1917; }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E8DFD8; }
        [data-testid="stSidebar"] h3 { font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 22px; color: #7A1B26 !important; }
        [data-testid="stSidebar"] hr { border-color: #E8DFD8; }
        [data-testid="stSidebar"] label { color: #6B5F57 !important; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div { background-color: #FAF7F4 !important; border: 1px solid #E8DFD8 !important; border-radius: 4px; }
        [data-testid="stSidebar"] caption, [data-testid="stSidebar"] .stCaption { color: #A89A8E !important; }

        /* ── Header band ── */
        .sw-header { background: #7A1B26; margin: -1rem -4rem 28px -4rem; padding: 20px 4rem 18px 4rem; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #1C1917; }
        .sw-header .brand { font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 26px; color: #FFFFFF; letter-spacing: 0.02em; text-transform: uppercase; line-height: 1; }
        .sw-header .brand span { color: #E0B23D; }
        .sw-header .sub { font-size: 10px; color: #E8C9C9; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 3px; }
        .sw-header .live-row { color: #F2E0E0; font-size: 11px; font-family: 'JetBrains Mono', monospace; text-align: right; }

        /* ── Metric cards ── */
        .metric-card { background: #FFFFFF; border: 1px solid #E8DFD8; border-radius: 4px; padding: 20px 22px; position: relative; overflow: hidden; }
        .metric-card::before { content: ''; position: absolute; top: 0; left: 0; width: 5px; height: 100%; }
        .metric-card.danger::before  { background: #D93B3B; }
        .metric-card.warning::before { background: #E0B23D; }
        .metric-card.safe::before    { background: #2D8A4E; }
        .metric-card.brand::before   { background: #7A1B26; }
        .metric-label { font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #A89A8E; margin-bottom: 10px; }
        .metric-value { font-family: 'Barlow Condensed', sans-serif; font-size: 42px; font-weight: 800; color: #1C1917; line-height: 1; }
        .metric-sub { font-size: 11px; color: #A89A8E; margin-top: 8px; }

        /* ── Badges ── */
        .alert-badge { display: inline-block; padding: 3px 10px; font-size: 10px; font-weight: 700; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.04em; border-radius: 2px; }
        .badge-critical { background: #D93B3B; color: #FFFFFF; }
        .badge-warning  { background: #E0B23D; color: #1C1917; }
        .badge-safe     { background: #2D8A4E; color: #FFFFFF; }

        /* ── Section headers ── */
        .section-header { font-family: 'Barlow Condensed', sans-serif; font-size: 16px; font-weight: 700; letter-spacing: 0.03em; text-transform: uppercase; color: #1C1917; border-bottom: 3px solid #7A1B26; padding-bottom: 8px; margin-bottom: 18px; display: inline-block; }

        /* ── Live dot ── */
        .live-dot { display: inline-block; width: 8px; height: 8px; background: #E0B23D; border-radius: 50%; margin-right: 6px; animation: blink 1.4s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

        /* ── Cards ── */
        .zone-card { background: #FFFFFF; border: 1px solid #E8DFD8; border-top: 3px solid #7A1B26; border-radius: 4px; padding: 16px; text-align: center; }
        .empty-state { background: #FFFFFF; border: 1px dashed #D9CDC3; border-radius: 4px; padding: 32px; text-align: center; color: #A89A8E; font-size: 13px; }
        .violation-card { background: #FFFFFF; border: 1px solid #E8DFD8; border-radius: 4px; padding: 12px 14px; margin-bottom: 8px; }
        .role-badge { display: inline-block; padding: 2px 8px; background: #7A1B26; color: #FFFFFF; border-radius: 2px; font-size: 10px; font-weight: 700; letter-spacing: 0.06em; font-family: 'JetBrains Mono', monospace; }

        

        /* ── Login ── */
        .login-brand { font-family: 'Barlow Condensed', sans-serif; font-size: 40px; font-weight: 800; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.02em; text-align: center; margin-bottom: 6px; }
        .login-brand span { color: #E0B23D; }
        .login-tagline { font-size: 11px; color: rgba(255,255,255,0.55); text-align: center; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 36px; }
        .login-footer { font-size: 11px; color: rgba(255,255,255,0.35); text-align: center; margin-top: 20px; letter-spacing: 0.04em; }
        /* SIDEBAR VISIBILITY BUG */
        #MainMenu, footer,{ visibility: hidden;} header[data-testid="stHeader"]{background: transparent; }
        .block-container { padding-top: 1rem; padding-bottom: 3rem; max-width: 100%; }
    </style>
    """, unsafe_allow_html=True)