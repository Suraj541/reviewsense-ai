import firebase_admin
from firebase_admin import auth, credentials
import os

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL")
})

firebase_admin.initialize_app(cred)

def verify_token(token: str):
    try:
        return auth.verify_id_token(token)
    except Exception as e:
        raise ValueError(f"Authentication failed: {str(e)}")