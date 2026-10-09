
import os
import firebase_admin
from firebase_admin import credentials, firestore

KEY_PATH = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

if os.path.exists(KEY_PATH):
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    print("⚠️ Warning: 'serviceAccountKey.json' not found in backend directory. Firebase db initialized as None.")
    db = None

