from rest_framework.response import Response
from rest_framework.decorators import api_view
from spotify.models import SpotifyToken
from .serializer import ItemSerializer
from spotify.views import *

"""
@api_view(['GET'])
def getData(request):
    items = SpotifyToken.objects.all()
    serializer = ItemSerializer(items, many = True)
    return Response(serializer.data)
"""
