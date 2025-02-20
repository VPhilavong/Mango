from django.shortcuts import render, redirect
from django.conf import settings
from requests import Request, post
from .util import update_tokens, get_user_tokens
from django.contrib.auth import logout as auth_logout
import os
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Create your views here.
def auth_url(request):
    scopes = 'user-top-read user-library-read user-read-recently-played, user-read-currently-playing, playlist-modify-public playlist-modify-private'
    url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID
        }).prepare().url
    return redirect(url)

def spotify_callback(request):
    code = request.GET.get('code')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    
    if expires_in is None:
        expires_in = 3600
    
    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('recently_played')

def logout(request):
    # Clear specific session keys
    keys_to_clear = ['access_token', 'token_type', 'expires_in', 'refresh_token']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]
    
    # Use Django's built-in logout function to clear the session
    auth_logout(request)
    
    # Ensure the session is flushed
    request.session.flush()
    
    # Render the custom logout page
    return render(request, 'logout.html')