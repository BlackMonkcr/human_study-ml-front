import os
from pymongo import MongoClient
import streamlit as st
from datetime import datetime
import random 

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def connect(self):
        """Establish MongoDB connection"""
        if self.client is None:
            try:
                mongodb_uri = os.getenv('MONGODB_URI')
                if not mongodb_uri:
                    raise ValueError("MongoDB URI not found in environment variables")

                self.client = MongoClient(mongodb_uri)
                self.db = self.client[os.getenv('MONGODB_DB', 'ml-workshop')]

                # Test connection
                self.client.admin.command('ping')
                return True
            except Exception as e:
                st.error(f"Database connection error: {str(e)}")
                return False
        return True

    def get_database(self):
        """Get database instance"""
        if self.connect():
            return self.db
        return None

def get_filtered_songs():
    """Get songs filtered for human study, favoring those with fewer responses"""
    db = DatabaseConnection().get_database()
    if db is None:
        return []

    try:
        songs_collection = db[os.getenv('SONGS_COLLECTION', 'songs_lang')]
        responses_collection = db[os.getenv('RESPONSES_COLLECTION', 'user_responses')]

        filter_criteria = {
            "spotify_found": True,
            "is_human_study": True
        }
        songs = list(songs_collection.find(filter_criteria))

        pipeline = [
            {"$group": {"_id": "$song_id", "count": {"$sum": 1}}}
        ]
        response_counts = {doc["_id"]: doc["count"] for doc in responses_collection.aggregate(pipeline)}

        for song in songs:
            song_id = str(song["_id"])
            count = response_counts.get(song_id, 0)
            song["_weight"] = 1 / (count + 1)

        weighted_songs = sorted(
            songs,
            key=lambda s: random.random() * (1 / s["_weight"])  
        )

        return weighted_songs

    except Exception as e:
        st.error(f"Error fetching songs: {str(e)}")
        return []

def save_user_classification(user_data, song_data, classification_data):
    """Save user classification to database. Upsert to avoid duplicate entries per user+song."""
    db = DatabaseConnection().get_database()
    if db is None:
        return False

    try:
        collection = db[os.getenv('RESPONSES_COLLECTION', 'user_responses')]
        response_document = {
            # User information
            'user_id': user_data['user_id'],
            'user_gender': user_data['gender'],
            'user_age': user_data['age'],

            # Song information
            'song_id': str(song_data['_id']),
            'spotify_id': song_data.get('spotify_id'),
            'artist': song_data['artist'],
            'title': song_data['title_songs_new'],
            'genre': song_data.get('genre'),
            'release_date': song_data.get('release_date'),
            'popularity': song_data.get('popularity'),

            # Classification data
            'explicit_content': classification_data['explicit_content'],
            'sexual_content': classification_data['sexual_content'],
            'children_suitability': classification_data['children_suitability'],
            'comments': classification_data.get('comments', ''),
            'confidence_level': classification_data.get('confidence_level'),

            # Metadata
            'timestamp': datetime.now(),
            'song_index': classification_data['song_index'],
            'session_duration_seconds': classification_data.get('session_duration'),
            'classification_source': 'human_study_frontend'
    }

        # Add status (completed/skipped)
        response_document['status'] = classification_data.get('status', 'completed')

        # Upsert by unique key (user_id + song_id)
        filter_doc = {
            'user_id': response_document['user_id'],
            'song_id': response_document['song_id']
        }
        update_doc = {
            '$set': response_document,
            '$setOnInsert': {'created_at': datetime.now()},
            '$currentDate': {'updated_at': True}
        }
        result = collection.update_one(filter_doc, update_doc, upsert=True)
        return result.acknowledged

    except Exception as e:
        st.error(f"Error saving classification: {str(e)}")
        return False

def get_user_progress(user_id):
    """Get user's classification progress"""
    db = DatabaseConnection().get_database()
    if db is None:
        return []

    try:
        collection = db[os.getenv('RESPONSES_COLLECTION', 'user_responses')]
        classified_songs = list(collection.find(
            {'user_id': user_id},
            {'song_id': 1, 'song_index': 1}
        ))

        return [song['song_id'] for song in classified_songs]

    except Exception as e:
        st.error(f"Error fetching user progress: {str(e)}")
        return []

def check_database_health():
    """Check if database is accessible and collections exist"""
    db = DatabaseConnection().get_database()
    if db is None:
        return False

    try:
        # Check if songs collection exists and has data
        songs_collection = db[os.getenv('SONGS_COLLECTION', 'songs_lang')]
        songs_count = songs_collection.count_documents({
            "spotify_found": True,
            "is_human_study": True
        })

        if songs_count == 0:
            st.warning("⚠️ No songs found with the required criteria (spotify_found: true, is_human_study: true)")
            return False

        st.success(f"✅ Database connected successfully. Found {songs_count} songs for the study.")
        return True

    except Exception as e:
        st.error(f"Database health check failed: {str(e)}")
        return False
