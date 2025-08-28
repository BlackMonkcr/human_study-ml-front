import streamlit as st
import uuid
import json
from datetime import datetime, timedelta

class SessionManager:
    """Manage user session state and persistence"""

    @staticmethod
    def initialize_session():
        """Initialize all session state variables"""

        # User identification
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None  # Set after auth

        # Auth state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False

        if 'account' not in st.session_state:
            st.session_state.account = None

        # User information collection
        if 'user_info_collected' not in st.session_state:
            st.session_state.user_info_collected = False

        if 'user_gender' not in st.session_state:
            st.session_state.user_gender = None

        if 'user_age' not in st.session_state:
            st.session_state.user_age = None

        # Navigation and progress
        if 'current_song_index' not in st.session_state:
            st.session_state.current_song_index = 0

        if 'completed_songs' not in st.session_state:
            st.session_state.completed_songs = set()

        if 'skipped_songs' not in st.session_state:
            st.session_state.skipped_songs = set()

        # Study data
        if 'songs_data' not in st.session_state:
            st.session_state.songs_data = []

        if 'song_id_to_index' not in st.session_state:
            st.session_state.song_id_to_index = {}

        # Session metadata
        if 'session_start_time' not in st.session_state:
            st.session_state.session_start_time = datetime.now()

        if 'last_activity_time' not in st.session_state:
            st.session_state.last_activity_time = datetime.now()

        # Study completion
        if 'study_completed' not in st.session_state:
            st.session_state.study_completed = False

        if 'progress_synced' not in st.session_state:
            st.session_state.progress_synced = False

    @staticmethod
    def update_activity():
        """Update last activity timestamp"""
        st.session_state.last_activity_time = datetime.now()

    @staticmethod
    def get_session_duration():
        """Get current session duration in seconds"""
        if 'session_start_time' not in st.session_state:
            return 0

        duration = datetime.now() - st.session_state.session_start_time
        return duration.total_seconds()

    @staticmethod
    def mark_song_completed(song_index, action='completed'):
        """Mark a song as completed or skipped"""
        if action == 'completed':
            st.session_state.completed_songs.add(song_index)
            # Remove from skipped if it was there
            st.session_state.skipped_songs.discard(song_index)
        elif action == 'skipped':
            st.session_state.skipped_songs.add(song_index)
            # Don't remove from completed in case user wants to revisit

    @staticmethod
    def get_progress_stats():
        """Get progress statistics"""
        total_songs = len(st.session_state.songs_data)
        completed = len(st.session_state.completed_songs)
        skipped = len(st.session_state.skipped_songs)
        remaining = total_songs - completed - skipped

        return {
            'total': total_songs,
            'completed': completed,
            'skipped': skipped,
            'remaining': remaining,
            'progress_percentage': (completed / total_songs * 100) if total_songs > 0 else 0
        }

    @staticmethod
    def get_next_song_index():
        """Get the next song that hasn't been completed or skipped"""
        total_songs = len(st.session_state.songs_data)

        # Start from current index + 1 and look forward
        for i in range(st.session_state.current_song_index + 1, total_songs):
            if i not in st.session_state.completed_songs and i not in st.session_state.skipped_songs:
                return i

        # If no forward songs found, look backward
        for i in range(0, st.session_state.current_song_index):
            if i not in st.session_state.completed_songs and i not in st.session_state.skipped_songs:
                return i

        # All songs completed or skipped
        return None

    @staticmethod
    def navigate_to_song(song_index):
        """Navigate to a specific song"""
        total_songs = len(st.session_state.songs_data)
        if 0 <= song_index < total_songs:
            st.session_state.current_song_index = song_index
            SessionManager.update_activity()
            return True
        return False

    @staticmethod
    def reset_session():
        """Reset the entire session"""
        keys_to_keep = ['songs_data']  # Keep loaded songs data
        keys = list(st.session_state.keys())
        for key in keys:
            if key not in keys_to_keep:
                del st.session_state[key]
        SessionManager.initialize_session()

    @staticmethod
    def is_session_expired(timeout_minutes=30):
        """Check if session has expired due to inactivity"""
        if 'last_activity_time' not in st.session_state:
            return False

        time_since_activity = datetime.now() - st.session_state.last_activity_time
        return time_since_activity > timedelta(minutes=timeout_minutes)

    @staticmethod
    def get_user_data():
        """Get user data for saving to database"""
        return {
            'user_id': st.session_state.user_id,
            'gender': st.session_state.user_gender,
            'age': st.session_state.user_age
        }

    @staticmethod
    def set_authenticated_user(user_doc):
        """Set account info after login/register."""
        st.session_state.authenticated = True
        st.session_state.account = {
            'id': str(user_doc.get('_id')),
            'username': user_doc.get('username'),
            'email': user_doc.get('email'),
        }
        st.session_state.user_id = st.session_state.account['id']
        # Load profile data
        st.session_state.user_gender = user_doc.get('gender')
        st.session_state.user_age = user_doc.get('age')
        st.session_state.user_info_collected = bool(st.session_state.user_gender is not None and st.session_state.user_age is not None)
        SessionManager.update_activity()

    @staticmethod
    def logout():
        """Log out the current user but keep loaded songs."""
        keys_to_keep = ['songs_data', 'song_id_to_index']
        keys = list(st.session_state.keys())
        for key in keys:
            if key not in keys_to_keep:
                del st.session_state[key]
        SessionManager.initialize_session()

    @staticmethod
    def set_song_id_map(songs):
        st.session_state.song_id_to_index = {str(song['_id']): idx for idx, song in enumerate(songs)}

    @staticmethod
    def sync_progress_from_db(responses):
        """Mark completed/skipped based on past responses."""
        for resp in responses:
            song_id = resp.get('song_id')
            status = resp.get('status') or 'completed'
            idx = st.session_state.song_id_to_index.get(song_id)
            if idx is None:
                continue
            if status == 'skipped':
                st.session_state.skipped_songs.add(idx)
            else:
                st.session_state.completed_songs.add(idx)
        st.session_state.progress_synced = True

    @staticmethod
    def save_local_progress():
        """Save progress to browser's local storage (via session state)"""
        # This is automatically handled by Streamlit's session state
        # but we can implement additional local storage if needed
        pass

    @staticmethod
    def check_study_completion():
        """Check if the study is completed and update status"""
        total_songs = len(st.session_state.songs_data)
        completed_songs = len(st.session_state.completed_songs)

        if total_songs > 0 and completed_songs >= total_songs:
            st.session_state.study_completed = True
            return True

        return False

# Utility functions for session management
def require_user_info():
    """Decorator function to require user info before proceeding"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not st.session_state.user_info_collected:
                st.warning("⚠️ Por favor, completa tu información personal antes de continuar.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator
