from rest_framework.response import Response
from rest_framework.decorators import api_view
from spotify.models import SpotifyToken
from .serializer import ItemSerializer
from spotify.views import *
import spotify.util as spotify


@api_view(['GET'])
def getData(request):
    items = SpotifyToken.objects.all()
    serializer = ItemSerializer(items, many = True)
    return Response(serializer.data)


# Get top tracks
@api_view(['GET'])
def top_tracks(request):
    access_token = spotify.get_user_tokens(request.session.session_key).access_token
    time_range = request.GET.get('time_range', 'short_term')
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': 50, 'time_range': time_range}
    try:
        response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)
        return Response(response.json())
    except Exception as e:
        return Response({'error': 'Failed to retrieve top artists'})