import streamlit as st

def load_custom_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    :root {
        --bg: #ffffff;
        --bg2: #f8f9fa;
        --text: #262730;
        --muted: #666666;
        --primary: #667eea;
        --primary2: #764ba2;
        --border: #e9ecef;
        --card-shadow: rgba(0,0,0,0.08);
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #0e1117;
            --bg2: #161a23;
            --text: #e6e6e6;
            --muted: #c2c7cf;
            --primary: #8ea2ff;
            --primary2: #9a7dff;
            --border: #2b2f3a;
            --card-shadow: rgba(0,0,0,0.3);
        }
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

    /* Classification form styling */
    .classification-form {
        background: var(--bg);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid var(--border);
        margin-top: 1rem;
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
    """Render song information in a styled card"""
    st.markdown(f"""
    <div class="song-card">
    <h3 style="margin-top: 0; color: var(--text);">{song['title_songs_new']}</h3>
    <p style="margin: 0.5rem 0; color: var(--muted);"><strong>Artista:</strong> {song['artist']}</p>
    <p style="margin: 0.5rem 0; color: var(--muted);"><strong>Género:</strong> {song['genre']}</p>
    {f'<p style="margin: 0.5rem 0; color: var(--muted);"><strong>Año:</strong> {song["release_date"][:4]}</p>' if song.get('release_date') else ''}
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
