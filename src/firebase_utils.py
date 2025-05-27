import firebase_admin
from firebase_admin import credentials, firestore
import os

def init_firebase():
    # Only initialize once
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.path.join(os.getcwd(), "firebase_config.json"))
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

# Example: Save a plan for a user
def save_plan(user_id, plan_data):
    db = init_firebase()
    doc_ref = db.collection("plans").document(user_id)
    doc_ref.set(plan_data)

# Example: Load a plan for a user
def load_plan(user_id):
    db = init_firebase()
    doc_ref = db.collection("plans").document(user_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None
