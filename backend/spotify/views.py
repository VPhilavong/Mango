import base64
import requests
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from urllib.parse import urlencode
import random, string
import os
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# login endpoint

@api_view(['GET'])
def login(request):
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    scope = ['user-top-read',
              'user-library-read',
              'user-read-recently-played',
              'user-read-currently-playing',
              'playlist-modify-public',
              ]
    print(REDIRECT_URI)
    auth_url = "https://accounts.spotify.com/authorize?" + urlencode({
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': ' '.join(scope),
        'redirect_uri': REDIRECT_URI,
        'state': state
    })
    return redirect(auth_url)


@api_view(['GET'])
def callback(request):
    """
    Handles the Spotify authentication callback, exchanges the authorization code for an access token.
    """
    code = request.GET.get('code')
    state = request.GET.get('state')

    if state is None:
        return redirect('/#' + urlencode({'error': 'state_mismatch'}))

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        },
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        }
    }

    response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])

    if response.status_code == 200:
        return Response(response.json())  # Return the access token and other data
    else:
        return Response({'error': 'invalid_token'}, status=response.status_code)