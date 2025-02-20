from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from requests import post
import requests
import urllib.parse

# Constants
CLIENT_ID = settings.SPOTIFY_CLIENT_ID
CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET
REDIRECT_URI = settings.SPOTIFY_REDIRECT_URI
BASE_URL = "https://api.spotify.com/v1/me/"

def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    return None

def update_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        if tokens.expires_in <= timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False

def refresh_spotify_token(session_id):
    tokens = get_user_tokens(session_id)
    if not tokens:
        return

    refresh_token = tokens.refresh_token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    if response.get('access_token'):
        access_token = response['access_token']
        token_type = response['token_type']
        expires_in = response['expires_in']
        update_tokens(session_id, access_token, token_type, expires_in, refresh_token)
    else:
        # Handle errors (e.g., logging, user notification)
        print('Failed to refresh token:', response)

def get_authorization_url(client_id, redirect_uri):
    base_url = 'https://accounts.spotify.com/authorize'
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': 'playlist-modify-public playlist-modify-private user-top-read',  # Include user-top-read
        'redirect_uri': redirect_uri,
        'show_dialog': 'true'  # Force Spotify to show the login dialog
    }
    # Return the full authorization URL
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def exchange_code_for_token(code):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()