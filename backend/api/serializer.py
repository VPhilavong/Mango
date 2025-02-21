from rest_framework import serializers
from spotify.models import SpotifyToken

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyToken
        fields = '__all__'
