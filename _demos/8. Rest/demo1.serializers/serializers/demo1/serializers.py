from .models import Movie
from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=100)
    
    def create(self, validated_data):
        print("create a new instance")

    def update(self, instance, validated_data):
        print("update the instance with the new data")


class MovieModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description']


