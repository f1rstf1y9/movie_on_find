from rest_framework import serializers
from movies.models import Movie,Actor
import requests

class ActorDetail(serializers.ModelSerializer):
    cast=serializers.SerializerMethodField()
    def get_cast(self,actor):
        return
    class Meta:
        model=Actor
        fields=('id','name','cast')
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
        fields=('id','name','profile_path',)

class MovieListSerializer(serializers.ModelSerializer):
    genre_ids = serializers.SerializerMethodField()

    def get_genre_ids(self, movie):
        # movie 객체로부터 장르 아이디 값을 가져와 반환
        return movie.get('genre_ids', [])
    class Meta:
        model = Movie
        fields = ('id','title', 'overview','vote_average','poster_path','genre_ids',)



class MovieDetailSerializer(serializers.ModelSerializer):
    genre_ids = serializers.SerializerMethodField()
    def get_genre_ids(self, movie):
        # movie 객체로부터 장르 아이디 값을 가져와 반환
        return movie.get('genres', [])
    class Meta:
        model = Movie
        fields = ('id','title', 'overview','vote_average','poster_path','genre_ids',)