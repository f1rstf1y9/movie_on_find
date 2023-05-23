from rest_framework import serializers
from movies.models import Movie,Genre
import requests

class MovieListSerializer(serializers.ModelSerializer):
    genre_ids = serializers.SerializerMethodField()

    def get_genre_ids(self, movie):
        # Movie 모델의 genres 필드로부터 genre_ids 값을 추출
        return list(movie.genres.values_list('id', flat=True))
    class Meta:
        model = Movie
        fields = ('id','title', 'overview','vote_average','poster_path','genre_ids','popularity','release_date')

class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieDetailSerializer(serializers.ModelSerializer):
    genre_ids = serializers.SerializerMethodField()

    def get_genre_ids(self, movie):
        # Movie 모델의 genres 필드로부터 genre_ids 값을 추출
        return list(movie.genres.all().values_list('id', flat=True))

    class Meta:
        model = Movie
        fields = ('id','title', 'overview','vote_average','poster_path','genre_ids',)