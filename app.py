import streamlit as st
import os
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Import custom utilities
from utils.database import (
    get_filtered_songs,
    save_user_classification,
    check_database_health,
    get_user_progress
)
from utils.session_manager import SessionManager
from utils.auth import get_auth_service
from utils.ui_components import (
    load_custom_css,
    render_song_info_card,
    render_completion_animation
)

import streamlit as st
import os
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Import custom utilities
from utils.database import (
    get_filtered_songs,
    save_user_classification,
    check_database_health,
    get_user_progress
)
from utils.session_manager import SessionManager
from utils.ui_components import (
    load_custom_css,
    render_song_info_card,
    render_completion_animation
)

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Estudio de Clasificación Musical",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load custom CSS
    load_custom_css()

def render_header():
    """Render application header compacto"""
    st.markdown("""
    <style>
    .main-header h1 {
        font-size: 1.7rem;
        margin-bottom: 0.2rem;
        margin-top: 0.5rem;
    }
    .main-header p {
        font-size: 1rem;
        margin-bottom: 0.2rem;
    }
    </style>
    <div class="main-header">
        <h1>🎵 Estudio de Clasificación Musical</h1>
        <p>Ayúdanos a clasificar el contenido de canciones en español</p>
    </div>
    """, unsafe_allow_html=True)

def render_user_info_form():
    """Render user information collection form"""
    st.markdown("### 📝 Información del Participante")
    st.markdown("Por favor, proporciona la siguiente información antes de comenzar:")

    with st.form("user_info_form"):
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox(
                "Género:",
                ["Seleccionar...", "Masculino", "Femenino", "Otro", "Prefiero no decir"],
                key="gender_select"
            )

        with col2:
            age = st.number_input(
                "Edad:",
                min_value=13,
                max_value=100,
                value=25,
                key="age_input"
            )

        # Terms and conditions
        st.markdown("---")
        terms_accepted = st.checkbox(
            "Acepto participar en este estudio de investigación y entiendo que mis respuestas serán utilizadas para fines académicos.",
            key="terms_checkbox"
        )
        submitted = st.form_submit_button("✅ Guardar perfil", use_container_width=True)

        if submitted:
            if gender != "Seleccionar..." and terms_accepted:
                st.session_state.user_gender = gender
                st.session_state.user_age = age
                st.session_state.user_info_collected = True
                # Persist to user profile if logged in
                if st.session_state.get('authenticated'):
                    try:
                        auth = get_auth_service()
                        auth._users.update_one(
                            {"_id": __import__('bson').objectid.ObjectId(st.session_state.account['id'])},
                            {"$set": {"gender": gender, "age": int(age)}}
                        )
                    except Exception:
                        pass
                st.rerun()
            else:
                if gender == "Seleccionar...":
                    st.error("Por favor, selecciona tu género para continuar.")
                if not terms_accepted:
                    st.error("Por favor, acepta los términos para continuar.")

def render_progress_indicator(current_index, total_songs):
    """Render progress indicator"""
    progress_stats = SessionManager.get_progress_stats()
    progress = progress_stats['completed'] / total_songs if total_songs > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Completadas", f"{progress_stats['completed']}/{total_songs}")

    with col2:
        st.metric("Omitidas", progress_stats['skipped'])

    with col3:
        st.metric("Progreso", f"{progress_stats['progress_percentage']:.1f}%")

    st.progress(progress, text=f"Canción {current_index + 1} de {total_songs}")

def render_audio_player(song):
    """Render solo el reproductor de YouTube usando id_yt"""
    st.subheader("🎧 Reproducir Canción")

    if song.get('id_yt'):
        youtube_embed = f'''
        <iframe width="100%" height="315"
            src="https://www.youtube.com/embed/{song['id_yt']}"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
        '''
        st.components.v1.html(youtube_embed, height=315)
    else:
        st.warning("⚠️ Video de YouTube no disponible para esta canción")

def render_classification_form(song, song_index):
    """Render classification form"""
    st.subheader("📊 Clasificación")

    with st.form(f"classification_form_{song_index}"):
        # Explicit content classification
        st.markdown("**¿Esta canción contiene contenido explícito?**")
        st.caption("Considera lenguaje fuerte, violencia, referencias a drogas, etc.")
        explicit_content = st.radio(
            "Contenido explícito:",
            ["No", "Sí", "No estoy seguro/a"],
            key=f"explicit_{song_index}",
            horizontal=True
        )

        # Sexual content classification
        st.markdown("**¿Esta canción contiene contenido sexual?**")
        st.caption("Considera referencias sexuales explícitas, insinuaciones, etc.")
        sexual_content = st.radio(
            "Contenido sexual:",
            ["No", "Sí", "No estoy seguro/a"],
            key=f"sexual_{song_index}",
            horizontal=True
        )

        # Confidence level
        confidence_level = st.select_slider(
            "¿Qué tan seguro/a estás de tu clasificación?",
            options=["Muy inseguro", "Inseguro", "Neutral", "Seguro", "Muy seguro"],
            value="Neutral",
            key=f"confidence_{song_index}"
        )

        # Additional comments
        comments = st.text_area(
            "Comentarios adicionales (opcional):",
            placeholder="Cualquier observación sobre la canción...",
            key=f"comments_{song_index}",
            max_chars=500
        )

        # Form buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            submit_button = st.form_submit_button(
                "✅ Enviar Clasificación",
                use_container_width=True,
                type="primary"
            )

        with col2:
            skip_button = st.form_submit_button(
                "⏭️ Omitir Canción",
                use_container_width=True
            )

        with col3:
            if song_index > 0:
                prev_button = st.form_submit_button(
                    "⬅️ Anterior",
                    use_container_width=True
                )
            else:
                prev_button = False

        return submit_button, skip_button, prev_button, {
            'explicit_content': explicit_content,
            'sexual_content': sexual_content,
            'confidence_level': confidence_level,
            'comments': comments,
            'song_index': song_index
        }

def handle_classification_submission(song, classification_data):
    """Handle the submission of a classification"""
    user_data = SessionManager.get_user_data()

    # Add session duration
    classification_data['session_duration'] = SessionManager.get_session_duration()

    success = save_user_classification(user_data, song, classification_data)

    if success:
        SessionManager.mark_song_completed(classification_data['song_index'], 'completed')
        SessionManager.update_activity()
        st.success("✅ Clasificación guardada exitosamente!")
        time.sleep(1)  # Brief pause for user feedback
        return True
    else:
        st.error("❌ Error al guardar la clasificación. Inténtalo de nuevo.")
        return False

def render_song_classification(song, song_index, total_songs):
    """Render complete song classification interface"""
    # Progress indicator
    render_progress_indicator(song_index, total_songs)

    # Song information y reproductor juntos
    col1, col2 = st.columns([6, 1])
    
    with col1:
        render_song_info_card(song)
        render_audio_player(song)  

    with col2:
        # Song metadata
        st.markdown("**Información adicional:**")
        if song.get('popularity'):
            st.metric("Popularidad Spotify", f"{song['popularity']}/100")

        if song.get('duration_ms'):
            duration_sec = song['duration_ms'] / 1000
            minutes = int(duration_sec // 60)
            seconds = int(duration_sec % 60)
            st.metric("Duración", f"{minutes}:{seconds:02d}")

        if song.get('release_date'):
            year = song['release_date'][:4]
            st.metric("Año", year)

    st.markdown("---")
    st.subheader("📊 Clasificación")

    # Checkbox FUERA del formulario
    show_more = st.checkbox(
        "Mostrar más preguntas",
        value=True,
        key=f"show_more_{song_index}"
    )

    with st.form(f"classification_form_{song_index}"):
        # Primera pregunta
        st.markdown("**¿Esta canción contiene contenido explícito?**")
        st.caption("Considera lenguaje fuerte, violencia, referencias a drogas, etc.")
        explicit_content = st.radio(
            "Contenido explícito:",
            ["No", "Sí", "No estoy seguro/a"],
            key=f"explicit_{song_index}",
            horizontal=True
        )

        # Si el usuario quiere, muestra el resto
        if show_more:
            st.markdown("**¿Esta canción contiene contenido sexual?**")
            st.caption("Considera referencias sexuales explícitas, insinuaciones, etc.")
            sexual_content = st.radio(
                "Contenido sexual:",
                ["No", "Sí", "No estoy seguro/a"],
                key=f"sexual_{song_index}",
                horizontal=True
            )

            confidence_level = st.select_slider(
                "¿Qué tan seguro/a estás de tu clasificación?",
                options=["Muy inseguro", "Inseguro", "Neutral", "Seguro", "Muy seguro"],
                value="Neutral",
                key=f"confidence_{song_index}"
            )

            comments = st.text_area(
                "Comentarios adicionales (opcional):",
                placeholder="Cualquier observación sobre la canción...",
                key=f"comments_{song_index}",
                max_chars=500
            )
        else:
            sexual_content = None
            confidence_level = None
            comments = ""

        # Form buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            submit_button = st.form_submit_button(
                "✅ Enviar Clasificación",
                use_container_width=True,
                type="primary"
            )

        with col2:
            skip_button = st.form_submit_button(
                "⏭️ Omitir Canción",
                use_container_width=True
            )

        with col3:
            if song_index > 0:
                prev_button = st.form_submit_button(
                    "⬅️ Anterior",
                    use_container_width=True
                )
            else:
                prev_button = False

        classification_data = {
            'explicit_content': explicit_content,
            'sexual_content': sexual_content,
            'confidence_level': confidence_level,
            'comments': comments,
            'song_index': song_index
        }

    # Manejo de botones igual que antes...
    # ... (resto del código de manejo de botones)

    if submit_button:
        # Guardar clasificación normal
        classification_data['status'] = 'completed'
        save_user_classification(SessionManager.get_user_data(), song, classification_data)
        SessionManager.mark_song_completed(song_index, 'completed')
        SessionManager.update_activity()
        st.success("✅ Clasificación guardada exitosamente!")
        time.sleep(1)
        next_song_index = SessionManager.get_next_song_index()
        if next_song_index is not None:
            SessionManager.navigate_to_song(next_song_index)
        else:
            st.session_state.study_completed = True
        st.rerun()

    elif skip_button:
        # Guardar como omitida
        classification_data['status'] = 'skipped'
        classification_data['explicit_content'] = None
        classification_data['sexual_content'] = None
        classification_data['confidence_level'] = None
        classification_data['comments'] = 'skipped'
        save_user_classification(SessionManager.get_user_data(), song, classification_data)
        SessionManager.mark_song_completed(song_index, 'skipped')
        SessionManager.update_activity()
        st.info("⏭️ Canción omitida")
        time.sleep(1)
        next_song_index = SessionManager.get_next_song_index()
        if next_song_index is not None:
            SessionManager.navigate_to_song(next_song_index)
        else:
            st.session_state.study_completed = True
        st.rerun()

    elif prev_button:
        # Ir a la canción anterior
        prev_index = song_index - 1
        if prev_index >= 0:
            SessionManager.navigate_to_song(prev_index)
            st.rerun()

def render_sidebar(songs):
    """Render application sidebar"""
    with st.sidebar:
        st.markdown("### 👤 Cuenta")
        if st.session_state.authenticated:
            st.write(f"**Usuario:** {st.session_state.account.get('username')}")
            st.write(f"**ID:** `{st.session_state.user_id[:8]}...`")
            st.write(f"**Género:** {st.session_state.user_gender}")
            st.write(f"**Edad:** {st.session_state.user_age}")
            if st.button("🚪 Cerrar sesión", use_container_width=True):
                SessionManager.logout()
                st.rerun()
        else:
            st.info("Inicia sesión o regístrate para guardar tu progreso.")

        st.markdown("---")

        # Progress summary
        progress_stats = SessionManager.get_progress_stats()
        st.markdown("### 📊 Progreso")
        st.write(f"**Completadas:** {progress_stats['completed']}")
        st.write(f"**Omitidas:** {progress_stats['skipped']}")
        st.write(f"**Restantes:** {progress_stats['remaining']}")

        # Progress bar
        if progress_stats['total'] > 0:
            progress = progress_stats['completed'] / progress_stats['total']
            st.progress(progress)

        st.markdown("---")

        # Song navigation
        st.markdown("### 🎵 Navegación")
        song_options = []
        for i, song in enumerate(songs):
            status = ""
            if i in st.session_state.completed_songs:
                status = "✅ "
            elif i in st.session_state.skipped_songs:
                status = "⏭️ "

            title = song['title_songs_new']
            if len(title) > 25:
                title = title[:25] + "..."

            song_options.append(f"{status}{i+1}. {title}")

        selected_index = st.selectbox(
            "Ir a canción:",
            range(len(songs)),
            index=st.session_state.current_song_index,
            format_func=lambda x: song_options[x]
        )

        if selected_index != st.session_state.current_song_index:
            SessionManager.navigate_to_song(selected_index)
            st.rerun()

        st.markdown("---")

        # Session info
        duration = SessionManager.get_session_duration()
        st.markdown("### ⏱️ Sesión")
        st.write(f"**Duración:** {duration/60:.1f} min")

        # Reset button
        if st.button("🔄 Reiniciar Estudio", use_container_width=True):
            SessionManager.reset_session()
            st.rerun()

def render_auth_panel():
    st.markdown("### 🔐 Acceso")
    auth = get_auth_service()
    tabs = st.tabs(["Iniciar sesión", "Registrarme"])

    with tabs[0]:
        with st.form("login_form"):
            identifier = st.text_input("Usuario o correo")
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Ingresar")
            if submit:
                res = auth.login_user(identifier, password)
                if res.get("success"):
                    SessionManager.set_authenticated_user(res["user"])
                    st.success("Bienvenido/a")
                    st.rerun()
                else:
                    st.error(res.get("message"))

    with tabs[1]:
        with st.form("register_form"):
            identifier = st.text_input("Usuario o correo")
            password = st.text_input("Contraseña", type="password")
            col1, col2 = st.columns(2)
            with col1:
                gender = st.selectbox("Género", ["Seleccionar...", "Masculino", "Femenino", "Otro", "Prefiero no decir"])
            with col2:
                age = st.number_input("Edad", min_value=13, max_value=100, value=25)
            submit = st.form_submit_button("Crear cuenta")
            if submit:
                g = None if gender == "Seleccionar..." else gender
                res = auth.register_user(identifier, password, g, int(age))
                if res.get("success"):
                    SessionManager.set_authenticated_user(res["user"])
                    st.success("Cuenta creada")
                    st.rerun()
                else:
                    st.error(res.get("message"))

def render_completion_screen():
    """Render study completion screen"""
    render_completion_animation()

    progress_stats = SessionManager.get_progress_stats()
    duration = SessionManager.get_session_duration()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Canciones Completadas", progress_stats['completed'])

    with col2:
        st.metric("Canciones Omitidas", progress_stats['skipped'])

    with col3:
        st.metric("Tiempo Total", f"{duration/60:.1f} min")

    st.markdown("---")

    st.markdown("""
    ### 🙏 ¡Gracias por tu participación!

    Tu contribución es muy valiosa para mejorar la clasificación automática
    de contenido musical. Los datos que proporcionaste ayudarán a desarrollar
    mejores sistemas de detección de contenido explícito en la música.

    **Código de participante:** `{}`

    Puedes cerrar esta página o reiniciar el estudio si deseas participar nuevamente.
    """.format(st.session_state.user_id))

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Participar Nuevamente", use_container_width=True):
            SessionManager.reset_session()
            st.rerun()

    with col2:
        st.markdown("[📊 Conoce más sobre el proyecto](#)", unsafe_allow_html=True)

def main():
    """Main application function"""
    # Configure page
    configure_page()

    # Initialize session
    SessionManager.initialize_session()

    # Render header
    render_header()

    # Check database health
    if not check_database_health():
        st.error("❌ No se puede conectar a la base de datos. Verifica la configuración.")
        st.stop()

    # Load songs if not already loaded
    if not st.session_state.songs_data:
        with st.spinner("Cargando canciones del estudio..."):
            st.session_state.songs_data = get_filtered_songs()
            SessionManager.set_song_id_map(st.session_state.songs_data)

    songs = st.session_state.songs_data

    if not songs:
        st.error("❌ No se encontraron canciones para el estudio.")
        st.stop()

    # Auth first if not logged in
    if not st.session_state.authenticated:
        render_auth_panel()
        return

    # Sync previous progress once per session
    if not st.session_state.progress_synced:
        # pull previous responses and mark completed
        prev_ids = get_user_progress(st.session_state.user_id)
        SessionManager.sync_progress_from_db([{ 'song_id': sid } for sid in prev_ids])

    # Collect user information (if missing in profile)
    if not st.session_state.user_info_collected:
        render_user_info_form()
        return

    # Check if study is completed
    if SessionManager.check_study_completion() or st.session_state.study_completed:
        render_completion_screen()
        return

    # Render sidebar
    render_sidebar(songs)

    # Render current song classification
    current_song = songs[st.session_state.current_song_index]
    render_song_classification(
        current_song,
        st.session_state.current_song_index,
        len(songs)
    )

if __name__ == "__main__":
    main()
