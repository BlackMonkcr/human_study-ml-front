import os
from typing import Optional, Dict, Any
from datetime import datetime

import bcrypt
from pymongo import MongoClient
import streamlit as st


class AuthService:
    """Basic auth service for registering and logging in users with hashed passwords."""

    def __init__(self):
        self._client: Optional[MongoClient] = None
        self._db = None
        self._users = None
        self._responses = None
        self._connect()

    def _connect(self):
        mongodb_uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("MONGODB_DB", "ml-workshop")
        users_collection = os.getenv("USERS_COLLECTION", "users")
        responses_collection = os.getenv("RESPONSES_COLLECTION", "user_responses")

        if not mongodb_uri:
            raise RuntimeError("MONGODB_URI is not set")

        self._client = MongoClient(mongodb_uri)
        self._db = self._client[db_name]
        self._users = self._db[users_collection]
        self._responses = self._db[responses_collection]

        # Indexes for performance and uniqueness
        try:
            self._users.create_index("username", unique=True)
            self._users.create_index("email", unique=True, sparse=True)
        except Exception:
            # Ignore if already exists / insufficient privileges
            pass

    def _hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    def _check_password(self, password: str, hashed: bytes) -> bool:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed)
        except Exception:
            return False

    def register_user(self, username_or_email: str, password: str, gender: Optional[str], age: Optional[int]) -> Dict[str, Any]:
        """Create a user account. Returns dict with success, message, user."""
        username = username_or_email.strip().lower()
        email = username if "@" in username else None

        # Basic validation
        if not username or not password:
            return {"success": False, "message": "Usuario y contraseña requeridos"}

        existing = self._users.find_one({"$or": [{"username": username}, {"email": email}]}) if email else self._users.find_one({"username": username})
        if existing:
            return {"success": False, "message": "El usuario ya existe"}

        hashed = self._hash_password(password)
        user_doc = {
            "username": username,
            "email": email,
            "password_hash": hashed,
            "gender": gender,
            "age": age,
            "created_at": datetime.now(),
            "last_login_at": None,
            "is_active": True,
        }
        res = self._users.insert_one(user_doc)
        user_doc["_id"] = res.inserted_id
        return {"success": True, "message": "Registro exitoso", "user": user_doc}

    def login_user(self, username_or_email: str, password: str) -> Dict[str, Any]:
        identifier = username_or_email.strip().lower()
        query = {"$or": [{"username": identifier}, {"email": identifier}]}
        user = self._users.find_one(query)
        if not user:
            return {"success": False, "message": "Usuario no encontrado"}

        if not user.get("is_active", True):
            return {"success": False, "message": "Cuenta inactiva"}

        if not self._check_password(password, user["password_hash"]):
            return {"success": False, "message": "Credenciales inválidas"}

        self._users.update_one({"_id": user["_id"]}, {"$set": {"last_login_at": datetime.now()}})
        return {"success": True, "message": "Login exitoso", "user": user}

    def get_user_progress_song_ids(self, user_id: str):
        """Return set of song_ids already answered by this user_id."""
        try:
            docs = self._responses.find({"user_id": user_id}, {"song_id": 1})
            return {d.get("song_id") for d in docs}
        except Exception:
            return set()



def get_auth_service() -> AuthService:
    # Cache in session to reuse connection
    if "_auth_service" not in st.session_state:
        st.session_state._auth_service = AuthService()
    return st.session_state._auth_service
