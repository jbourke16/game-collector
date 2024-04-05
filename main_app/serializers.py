from rest_framework import serializers
from .models import Game, Developer, Type
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    genres = TypeSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Game
        fields = '__all__'

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'
        read_only_fields = ('game',)

