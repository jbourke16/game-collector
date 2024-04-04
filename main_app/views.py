from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Game, Developer, Type
from .serializers import GameSerializer, DeveloperSerializer, TypeSerializer

# Create your views here.
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the game-collector api home route!'}
        return Response(content)
    
class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'id'

class DeveloperListCreate(generics.ListCreateAPIView):
    serializer_class = DeveloperSerializer

    def get_queryset(self):
        game_id = self.kwargs('game_id')
        return Developer.objects.filter(game_id=game_id)
    
    def perform_create(self, serializer):
        game_id = self.kwargs('game_id')
        game = Game.objects.get(id=game_id)
        serializer.save(game=game)

class DeveloperDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        game_id = self.kwargs['game_id']
        return Developer.objects.filter(game_id=game_id)
    
class TypeList(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    lookup_field = 'id'

