from django.urls import path
from .views import *
from spotify.views import auth_url, spotify_callback, logout
urlpatterns = [
    path('spotify/login/', auth_url, name='spotify_login'),
    path('spotify/callback/', spotify_callback, name='spotify_callback'),
    path('spotify/logout/', logout, name='spotify_logout'),
    path('top_artists/', top_artists, name='top_artists'),
    path('top_tracks/', top_tracks, name='top_tracks'),
    path('top_genres/', top_genres, name='top_genres'),
    path('recently_played/', recently_played, name='recently_played'),
    path('logout/', logout, name='logout'),
    path('', login, name='login'),
]