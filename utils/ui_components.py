import streamlit as st

def load_custom_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    :root {
        /* Force light palette */
        --bg: #ffffff;
        --bg2: #f8f9fa;
        --text: #1f2328;
        --muted: #525860;
        --primary: #667eea;
        --primary2: #764ba2;
        --border: #e3e5e8;
        --card-shadow: rgba(0,0,0,0.08);
    }

    .main > div { padding-top: 2rem; }

    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary2) 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }

    /* Song card styling */
    .song-card {
        background: var(--bg2);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary);
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px var(--card-shadow);
    }

    /* Compact song card styling */
    .song-card-compact {
        background: #f7f7fa;
        padding: 0.3rem 0.8rem 0.3rem 0.8rem;
        border-radius: 6px;
        border-left: 3px solid #a78bfa;
        margin-bottom: 0.3rem;
        font-size: 0.93rem;
        box-shadow: 0 1px 2px #eee;
    }
    .song-title-compact {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.05rem;
        margin-top: 0.05rem;
    }
    .song-artist-compact {
        font-size: 0.93rem;
        color: #555;
        margin-bottom: 0.05rem;
    }
    .song-meta-compact {
        font-size: 0.85rem;
        color: #888;
        margin-bottom: 0.05rem;
    }

    /* Classification form styling */
    .classification-form {
        background: var(--bg);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid var(--border);
        margin-top: 1rem;
    }
    /* Ensure high-contrast text inside forms */
    .stForm, .stForm p, .stForm label, .stForm span,
    .stForm h1, .stForm h2, .stForm h3, .stForm h4, .stForm h5, .stForm h6,
    .stForm .stMarkdown p {
        color: var(--text) !important;
    }
    .stForm em, .stForm small { color: var(--muted) !important; }
    /* Inputs */
    .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] { color: var(--text) !important; }

    /* Input borders (text/password/number) */
    div[data-baseweb="input"] {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-baseweb="input"]:hover { border-color: var(--primary) !important; }
    div[data-baseweb="input"]:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 0.2rem rgba(102,126,234,0.18) !important;
    }

    /* Select borders */
    div[data-baseweb="select"] > div {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-baseweb="select"]:hover > div { border-color: var(--primary) !important; }
    div[data-baseweb="select"]:focus-within > div {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 0.2rem rgba(102,126,234,0.18) !important;
    }

    /* Textarea border */
    .stTextArea textarea {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }

    /* Progress bar custom styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary2) 100%);
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #28a745, #20c997);
    }

    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(45deg, #6c757d, #495057);
    }

    /* Success message styling */
    .stSuccess {
        background: linear-gradient(45deg, #d4edda, #c3e6cb);
        border-left: 4px solid #28a745;
    }

    /* Info message styling */
    .stInfo {
        background: linear-gradient(45deg, #cce7ff, #b3d9ff);
        border-left: 4px solid #007bff;
    }

    /* Error message styling */
    .stError {
        background: linear-gradient(45deg, #f8d7da, #f5c6cb);
        border-left: 4px solid #dc3545;
    }

    /* Sidebar styling */
    .css-1d391kg, .stSidebarContent {
        background: linear-gradient(180deg, var(--bg2) 0%, var(--bg) 100%);
    }

    /* Radio button styling */
    .stRadio > div > label > div:first-child {
        border: 2px solid var(--primary);
    }

    .stRadio > div > label > div:first-child[data-checked="true"] {
        background: var(--primary);
    }

    /* Metric styling */
    .metric-container {
        background: var(--bg);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border);
        text-align: center;
    }

    /* Form styling */
    .stForm {
        background: var(--bg2);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid var(--border);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}

    /* Responsive design */
    @media (max-width: 768px) {
    .main > div { padding-left: 1rem; padding-right: 1rem; }

    .song-card { padding: 1rem; }

    .classification-form { padding: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

def render_song_info_card(song):
    """Render compact song information card"""
    st.markdown(f"""
    <style>
    .song-card-compact {{
        background: #f7f7fa;
        padding: 0.3rem 0.8rem 0.3rem 0.8rem;
        border-radius: 6px;
        border-left: 3px solid #a78bfa;
        margin-bottom: 0.3rem;
        font-size: 0.93rem;
        box-shadow: 0 1px 2px #eee;
    }}
    .song-title-compact {{
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.05rem;
        margin-top: 0.05rem;
    }}
    .song-artist-compact {{
        font-size: 0.93rem;
        color: #555;
        margin-bottom: 0.05rem;
    }}
    .song-meta-compact {{
        font-size: 0.85rem;
        color: #888;
        margin-bottom: 0.05rem;
    }}
    </style>
    <div class="song-card-compact">
        <div class="song-title-compact">{song['title_songs_new']}</div>
        <div class="song-artist-compact">{song['artist']}</div>
        {f'<div class="song-meta-compact">Año: {song["release_date"][:4]}</div>' if song.get('release_date') else ''}
    </div>
    """, unsafe_allow_html=True)

def render_completion_animation():
    """Render completion animation"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
        <h1 style="color: #28a745; margin-bottom: 1rem;">¡Estudio Completado!</h1>
        <p style="font-size: 1.2rem; color: #666;">Gracias por tu valiosa participación</p>
    </div>
    """, unsafe_allow_html=True)
