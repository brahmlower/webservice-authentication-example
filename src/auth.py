
from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(google_client_id, user_token):
        id_info = id_token.verify_oauth2_token(user_token, requests.Request(), google_client_id)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None
        return id_info
