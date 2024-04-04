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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        genres_not_associated = Type.objects.exclude(id__in=instance.genres.all())
        genres_serializer = TypeSerializer(genres_not_associated, many=True)

        return Response({
            'game': serializer.data,
            'genres_not_associated': genres_serializer.data
        })

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

class AddGenreToGame(APIView):
  def post(self, request, game_id, genre_id):
    cat = Game.objects.get(id=game_id)
    type = Type.objects.get(id=genre_id)
    game.genres.add(genre)
    return Response({'message': f'Genre {type.genre} added to Game {game.title}'})


