from rest_framework import serializers
from .models import Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Genre
        fields = ['id', 'tmdb_id', 'name', 'movie_count']
        read_only_fields = ['id']
    
    def get_movie_count(self, obj):
        return obj.movies.count()


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    poster_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'overview', 'release_date',
            'poster_path', 'backdrop_path', 'vote_average', 'vote_count',
            'genres', 'poster_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MovieListSerializer(serializers.ModelSerializer):
    """Simplified serializer for movie lists"""
    genres = serializers.StringRelatedField(many=True, read_only=True)
    poster_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'release_date',
            'poster_url', 'vote_average', 'vote_count', 'genres'
        ]
        read_only_fields = ['id']
