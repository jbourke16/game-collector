from rest_framework import serializers
from .models import Game, Developer, Type

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    genres = TypeSerializer(many=True, read_only=True)
    class Meta:
        model = Game
        fields = '__all__'

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'
        read_only_fields = ('game',)

