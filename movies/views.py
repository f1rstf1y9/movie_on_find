from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib.auth.decorators import login_required
from movies.models import Movie,Actor
from movies.serializers import MovieListSerializer,MovieDetailSerializer,ActorList,ActorDetail
from django.core import serializers
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST, require_safe, require_http_methods
import requests
import json
from movies.models import Genre
from reviews.models import Review
from cards.models import Card
from django.db import transaction


# 장르데이터저장
my_id=''
def get_Genre_data():
    url='https://api.themoviedb.org/3/genre/movie/list?api_key='+my_id+'&language=ko'
    response=requests.get(url)
    raw_data=response.json()
    data=raw_data.get('genres')
    result=[]
    for i in data:
        genre_dict={
            "model":"movies.genre",
            "pk":i.get("id"),
            "fields":{"name":i.get("name")}
        }
        result.append(genre_dict)
    return result
# with open('movies/fixtures/genre.json','w',encoding="UTF-8") as f:
    json.dump(get_Genre_data(),f,ensure_ascii=False,indent=2)
# 영화데이터저장
def get_top_rated_data():
    result=[]
    for page in range(1,51):
        url='https://api.themoviedb.org/3/movie/top_rated?api_key='+my_id+'&language=ko&page='+str(page)
        raw_data=requests.get(url).json()
        data=raw_data.get('results')
        
        for i in data:
            movie_dict={
                "model":"movies.movie",
                "pk":i.get("id"),
                "fields":{
                    "title":i.get("title"),
                    "vote_average":i.get("vote_average"),
                    "overview":i.get("overview"),
                    "poster_path":i.get("poster_path"),
                    "genres":i.get("genre_ids"),
                    "interest":[],
                    "watched":[],
                    "watching":[],
                    },
            }
            result.append(movie_dict)
    return result
# with open('movies/fixtures/movie.json','w',encoding="UTF-8") as f:
#     json.dump(get_top_rated_data(),f,ensure_ascii=False,indent=2)
# Create your views here.

def data_sort():
    movie=Movie.objects.all()
    for i in movie:
        if i.overview=='':
            i.delete()

def Genre_data():
    url='https://api.themoviedb.org/3/genre/movie/list?api_key='+my_id+'&language=ko'
    response=requests.get(url).json()
    data=response.json()
    return data
def get_movie_video():
    movie=Movie.objects.all()
    for i in movie:
        url1='https://api.themoviedb.org/3/movie/'+str(i.pk)+'/videos?api_key='+my_id+'&language=ko'
        response1=requests.get(url1).json()
        data1=response1['results']
        if len(data1)==0:
            pass
        else:
            key=data1[0]['key']
            i.video=key
            i.save()


def Movies_data():
    url='https://api.themoviedb.org/3/movie/top_rated?api_key='+my_id+'&language=ko'
    response=requests.get(url)
    data=response.json()
    
    return data.get('results',[])
def Movie_data(movie_pk):
    url='https://api.themoviedb.org/3/movie/'+str(movie_pk)+'?api_key='+my_id+'&language=ko'
    response=requests.get(url)
    data=response.json()
    return [data]

def Actor_data(movie_pk):
    url='https://api.themoviedb.org/3/movie/'+str(movie_pk)+'/credits?api_key='+my_id+'&language=ko'
    response=requests.get(url)
    data=response.json()
    return [data]

def Actor_Detail_data(actor_pk):
    url='https://api.themoviedb.org/3/person/'+str(actor_pk)+'/movie_credits?api_key='+my_id+'&language=ko'
    response=requests.get(url)
    data=response.json()
    return [data]



@api_view(['GET'])
def index(request):
    # data_sort()
    # get_movie_video()
    movie=Movie.objects.all().order_by('-vote_average')[:10]
    genre=Genre.objects.values()
    serializer=MovieListSerializer(movie,many=True)
    serialized_data = serializer.data

    
    return render(request,'movies/index.html',{'resdatas':serialized_data,'datas':genre})

@require_safe
@login_required
def detail(request,movie_pk):
    movie=Movie.objects.get(pk=movie_pk)
    serializer1=MovieDetailSerializer(movie)
    serialized_data1 = serializer1.data
    genre=Genre.objects.values()
    raw_data=Review.objects.filter(movie_id=movie_pk)
    reviews=raw_data
    cards=Card.objects.filter(movie_id=movie_pk)
    # movie.video=get_movie_video(movie_pk)
    # movie.save()
    context={
        'resdatas':serialized_data1,
        'datas':genre,
        'reviews':reviews,
        'cards':cards
    }
    return render(request, 'movies/detail.html',context)

# @login_required
# def actor_detail(request,actor_pk):
#     actor_data=Actor_Detail_data(actor_pk)
#     serializer=ActorDetail(actor_data,many=True)
#     serialized_data = serializer.data
#     return render(request, 'movies/actordetail.html',{'resdatas':serialized_data[0]['cast']})

@api_view(['GET'])
def search(request):
    movies=Movie.objects.all()
    content = request.GET.get('content')
    print(content)
    for i in movies:
        if i.title==content:
            context={
                'ID':i.id
            }
            return JsonResponse(context)

