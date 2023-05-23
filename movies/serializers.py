from rest_framework import serializers
from movies.models import Movie,Actor,Genre
import requests

class ActorDetail(serializers.ModelSerializer):
    cast=serializers.SerializerMethodField()
    def get_cast(self,actor):
        L=[]
        for i in actor.get('cast'):
            L.append({'id':i['id'],'title':i['title'],'poster_path':i['poster_path']})
        return [{'title':item['title'],'id':item['id'],'poster_path':item['poster_path']} for item in L]
    class Meta:
        model=Actor
        fields=('id','cast')
class ActorList(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    def get_name(self, actor):
        L=[]
        for i in actor.get('cast'):
            if i['known_for_department'] == 'Acting':
                # print(i['profile_path'])
                L.append({'id':i['id'],'name':i['name'],'profile_path':i['profile_path']})
        return [{'name':item['name'],'id':item['id'],'profile_path':item['profile_path']} for item in L]
    class Meta:
        model=Actor
        fields=('id','name')

class MovieListSerializer(serializers.ModelSerializer):
    genre_ids = serializers.SerializerMethodField()
    def get_genre_ids(self, movie):
        # Movie 모델의 genres 필드로부터 genre_ids 값을 추출
        return list(movie.genres.values_list('id', flat=True))
    class Meta:
        model = Movie
        fields = ('id','title', 'overview','vote_average','poster_path','genre_ids',)
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


# class CommentCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=Comment
#         fields='__all__'
#         read_only_fields = ('movie','user')