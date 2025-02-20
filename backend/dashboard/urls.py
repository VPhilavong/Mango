from django.urls import path
from . import views
from spotify.views import auth_url, spotify_callback, logout, spotify_callback
urlpatterns = [
    path('spotify/login/', auth_url, name='spotify_login'),
    path('spotify/callback/', spotify_callback, name='spotify_callback'),
    path('spotify/logout/', logout, name='spotify_logout'),
    path('top_artists/', views.top_artists, name='top_artists'),
    path('top_tracks/', views.top_tracks, name='top_tracks'),
    path('top_genres/', views.top_genres, name='top_genres'),
    path('recently_played/', views.recently_played, name='recently_played'),
    path('top_genres/', views.recommendations, name='recommendations'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('success/', views.success_page, name='success_page'),
    path('logout/', views.logout, name='logout'),
    path('', views.login, name='login'),
]