from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from movies.serializers import MovieListSerializer,MovieDetailSerializer,ActorList,ActorDetail
from django.core import serializers
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.views.decorators.http import require_POST, require_safe, require_http_methods
import requests

my_id='b4d8715368a27e1da703d584f643db18'


# Create your views here.

def Genre_data():
    url='https://api.themoviedb.org/3/genre/movie/list?api_key='+my_id
    response=requests.get(url)
    data=response.json()
    return data


def Movies_data():
    url='https://api.themoviedb.org/3/movie/top_rated?api_key='+my_id
    response=requests.get(url)
    data=response.json()
    
    return data.get('results',[])
def Movie_data(movie_pk):
    url='https://api.themoviedb.org/3/movie/'+str(movie_pk)+'?api_key='+my_id
    response=requests.get(url)
    data=response.json()
    return [data]

def Actor_data(movie_pk):
    url='https://api.themoviedb.org/3/movie/'+str(movie_pk)+'/credits?api_key='+my_id
    response=requests.get(url)
    data=response.json()
    return [data]

def Actor_Detail_data(actor_pk):
    # 'https://api.themoviedb.org/3/person/1158/movie_credits?language=en-US'
    url='https://api.themoviedb.org/3/person/'+str(actor_pk)+'/movie_credits?api_key='+my_id
    response=requests.get(url)
    print(response.json())
    data=response.json()
    return [data]

@require_safe
def index(request):
    movies_data=Movies_data()
    # print(movies_data)
    serializer=MovieListSerializer(movies_data,many=True)
    serialized_data = serializer.data
    # print(serialized_data)
    data=Genre_data()
    return render(request,'movies/index.html',{'resdatas':serialized_data,'datas':data})
    

@require_safe
@login_required
def detail(request,movie_pk):
    movie_data=Movie_data(movie_pk)
    actor_data=Actor_data(movie_pk)
    # print(actor_data)
    serializer1=MovieDetailSerializer(movie_data,many=True)
    serialized_data1 = serializer1.data
    serializer2=ActorList(actor_data,many=True)
    # print(serializer2.data)
    serialized_data2 = serializer2.data
    # print(serialized_data2[0]['name'])
    return render(request, 'movies/detail.html',{'resdatas':serialized_data1[0],'datas':serialized_data2[0]['name']})

@require_safe
@login_required
def actor_detail(request,actor_pk):
    actor_data=Actor_Detail_data(actor_pk)
    serializer=ActorDetail(actor_data,many=True)
    # print(serializer2.data)
    # serialized_data = serializer.data
    # print(serialized_data2[0]['name'])
    return
    # return render(request, 'movies/detail.html',{'resdatas':serialized_data})

