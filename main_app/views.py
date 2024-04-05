from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from .models import Game, Developer, Type
from .serializers import GameSerializer, DeveloperSerializer, TypeSerializer, UserSerializer

# Create your views here.

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the game-collector api home route!'}
        return Response(content)
    
class GameList(generics.ListCreateAPIView):
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
       user = self.request.user
       return Game.objects.filter(user=user)
    
    def perform_create(self, serializer):
       serializer.save(user=self.request.user)

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    lookup_field = 'id'

    def get_queryset(self):
       user = self.request.user
       return Game.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        genres_not_associated = Type.objects.exclude(id__in=instance.genres.all())
        genres_serializer = TypeSerializer(genres_not_associated, many=True)

        return Response({
            'game': serializer.data,
            'genres_not_associated': genres_serializer.data
        })
    
    def perform_update(self, serializer):
       game = self.get_object()
       if game.user != self.request.user:
          raise PermissionDenied({'message': 'You do not have permission to edit this game.'})
       serializer.save()

    def perform_destroy(self, instance):
       if instance.user != self.request.user:
          raise PermissionDenied({'message': 'You do not have permission to delete this game'})
       instance.delete()

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
