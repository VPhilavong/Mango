from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.templatetags.static import static
from django.contrib import messages
from spotify.util import get_user_tokens, exchange_code_for_token, update_tokens, is_spotify_authenticated
import json
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse
import requests
#delete after debugging
import logging
import requests

# Configure logging (you can change the level to DEBUG for more details)
logging.basicConfig(level=logging.INFO)


from datetime import datetime

# Create your views here.
def login(request):
    return render(request, 'login.html')

def recently_played(request, limit = 20):
    access_token = get_user_tokens(request.session.session_key).access_token
    profile_picture_url = get_user_profile_picture_url(request)

    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': limit}

    # Get recently played tracks
    recently_played_response = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers, params=params)
    recently_played_tracks = recently_played_response.json() if recently_played_response.status_code == 200 else None

    # Get currently playing track
    currently_playing_response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers, params=params)
    currently_playing_track = currently_playing_response.json() if currently_playing_response.status_code == 200 else None

    context = {
        'recently_played_tracks': recently_played_tracks,
        'currently_playing_track': currently_playing_track,
        'profile_picture_url': profile_picture_url
    }

    return render(request, 'recently_played.html', context)

def top_tracks(request, limit=50):
    access_token = get_user_tokens(request.session.session_key).access_token

    time_range = request.GET.get('time_range', 'short_term')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': limit, 'time_range': time_range}
    response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)
    
    if response.status_code == 200:
        top_artists = response.json()
        return render(request, 'top_tracks.html', {'top_tracks': top_artists, 'time_range': time_range, 'profile_picture_url': get_user_profile_picture_url(request)})
    else:
        return render(request, 'top_tracks.html', {'error': 'Failed to retrieve top artists'})



def top_tracks(request, limit=50):
    try:
        # Fetch the access token
        access_token = get_user_tokens(request.session.session_key).access_token
        logging.info(f"Access Token: {access_token}")
        
        # Set parameters for the request
        time_range = request.GET.get('time_range', 'short_term')
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'limit': limit, 'time_range': time_range}
        
        logging.info(f"Making request with params: {params}")

        # Make the API request
        response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)

        # Debug the response details
        logging.info(f"Spotify API Response Code: {response.status_code}")
        logging.debug(f"Spotify API Response Body: {response.text}")

        # Check for a successful response
        if response.status_code == 200:
            top_tracks = response.json()
            logging.info(f"Top Tracks: {top_tracks}")
            return render(request, 'top_tracks.html', {'top_tracks': top_tracks, 'time_range': time_range})
        else:
            # Log an error message and display the error on the page
            logging.error(f"Failed to retrieve top tracks. Status Code: {response.status_code}")
            return render(request, 'top_tracks.html', {'error': 'Failed to retrieve top tracks', 'status_code': response.status_code})

    except Exception as e:
        # Log any exceptions
        logging.exception(f"An error occurred: {e}")
        return render(request, 'top_tracks.html', {'error': 'An unexpected error occurred'})


def top_artists(request, limit=50):
    access_token = get_user_tokens(request.session.session_key).access_token
    profile_picture_url = get_user_profile_picture_url(request)

    time_range = request.GET.get('time_range', 'short_term')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': limit, 'time_range': time_range}
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers, params=params)
    
    if response.status_code == 200:
        top_artists = response.json()
        return render(request, 'top_artists.html', {'top_artists': top_artists, 'time_range': time_range, 'profile_picture_url': get_user_profile_picture_url(request)})
    else:
        return render(request, 'top_artists.html', {'error': 'Failed to retrieve top artists'})
    
def top_genres(request):
    access_token = get_user_tokens(request.session.session_key).access_token
    profile_picture_url = get_user_profile_picture_url(request)

    timerange = request.GET.get('time_range', 'short_term')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'time_range': timerange}
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers, params=params)
    
    if response.status_code == 200:
        top_artists = response.json()
        genre_count = {}
        
        for artist in top_artists['items']:
            for genre in artist['genres']:
                if genre in genre_count:
                    genre_count[genre] += 1
                else:
                    genre_count[genre] = 1
        
        # Sort genres by count and take the top 10
        sorted_genres = sorted(genre_count.items(), key=lambda item: item[1], reverse=True)[:10]
        
        if len(sorted_genres) == 0:
            return render(request, 'top_genres.html', {'error': 'No genres found'})
        genres, counts = zip(*sorted_genres)
        
        fig, ax = plt.subplots()
        fig.set_facecolor('#FDFD96')
        ax.set_facecolor('#FDFD96')
        ax.pie(counts, labels=genres, autopct='%1.1f%%', startangle=90,)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = 'data:image/png;base64,' + urllib.parse.quote(string)
        
        print(sorted_genres)
        return render(request, 'top_genres.html', {'pie_chart': uri, 'time_range': timerange, 'top_genres': sorted_genres, 'profile_picture_url': get_user_profile_picture_url(request)})
    else:
         return render(request, 'top_genres.html', {'error': 'Failed to retrieve top genres'})

def get_user_profile_picture_url(request):
    access_token = get_user_tokens(request.session.session_key).access_token  # Ensure access token retrieval is correct
    if not access_token:
        return None

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data['images'][0]['url'] if user_data['images'] else static('images/default.png')
    else:
        print(f"Failed to retrieve user profile: {response.status_code} - {response.text}")
        return None

def logout(request):
    request.session.flush()
    return redirect('login')

def test(request):
    return HttpResponse('Test page')

def recommendations(request, limit=10):
    access_token = get_user_tokens(request.session.session_key).access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get selected songs from the form
    selected_songs = request.POST.getlist('selected_songs')
    
    # Create the recommendations request
    params = {
        'limit': limit,
        'seed_tracks': ','.join(selected_songs)  # Use selected songs for recommendations
    }
    
    response = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=params)

    if response.status_code == 200:
        recommendations = response.json()
        return render(request, 'recommendations.html', {'recommendations': recommendations['tracks']})
    else:
        return render(request, 'error.html', {'error': 'Failed to retrieve recommendations'})

def create_playlist(request):
    if request.method == 'POST':
        access_token = get_user_tokens(request.session.session_key).access_token

        if not access_token:
            return HttpResponse("Error: No access token available.", status=400)

        user_id = get_user_tokens(request.session.session_key).access_token
        if not user_id:
            return HttpResponse("Error: No user ID found.", status=400)

        playlist_name = "FUCK "
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'name': playlist_name,
            'description': 'Created via Spotify App',
            'public': False
        }
        response = requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists', headers=headers, json=data)

        if response.status_code == 201:
            playlist_id = response.json()['id']
            track_ids = request.POST.getlist('selected_tracks')
            if track_ids:
                success = add_tracks_to_playlist(access_token, playlist_id, track_ids)
                if not success:
                    return HttpResponse("Error: Failed to add tracks to playlist.", status=500)
            return redirect('success_page')  # Redirect to the success page
        else:
            error_message = response.json().get('error', 'Failed to create playlist')
            return HttpResponse(f"Error: {error_message}", status=response.status_code)

    return HttpResponse("Error: Invalid request method.", status=405)

def add_tracks_to_playlist(access_token, playlist_id, track_ids):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    data = {'uris': [f'spotify:track:{track_id}' for track_id in track_ids]}
    
    # Debugging information
    print(f"Add Tracks Request URL: {url}")
    print(f"Add Tracks Request Headers: {headers}")
    print(f"Add Tracks Request Data: {json.dumps(data)}")
    
    response = requests.post(url, headers=headers, json=data)
    
    # Debugging information
    print(f"Add Tracks Response Status Code: {response.status_code}")
    print(f"Add Tracks Response Body: {response.text}")
    
    if response.status_code == 201:
        return True
    else:
        return False

def success_page(request):
    # Retrieve playlist info from query parameters
    playlist_id = request.GET.get('playlist_id')
    playlist_name = request.GET.get('playlist_name')
    playlist_description = request.GET.get('playlist_description')

    # Optional: Retrieve playlist data from Spotify API if needed
    # playlist_data = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=headers).json()

    context = {
        'playlist_id': playlist_id,
        'playlist_name': playlist_name,
        'playlist_description': playlist_description
    }

    return render(request, 'success.html', context)
