from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from movies.serializers import MovieListSerializer,MovieDetailSerializer,ActorList,ActorDetail,CommentCreateSerializer
from django.core import serializers
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST, require_safe, require_http_methods
import requests
import json
from .forms import CommentForm
from movies.models import Comment,Genre
from django.db import transaction



my_id='b4d8715368a27e1da703d584f643db18'
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
#     json.dump(get_Genre_data(),f,ensure_ascii=False,indent=2)

def get_top_rated_data():
    result=[]
    for page in range(1,31):
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
                    "like_users":[],
                    "wish_users":[]
                    },

            }
            result.append(movie_dict)
        # print(result)
    return result
# with open('movies/fixtures/movie.json','w',encoding="UTF-8") as f:
#     json.dump(get_top_rated_data(),f,ensure_ascii=False,indent=2)
# Create your views here.

def Genre_data():
    url='https://api.themoviedb.org/3/genre/movie/list?api_key='+my_id+'&language=ko'
    response=requests.get(url)
    data=response.json()
    return data


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
    # 'https://api.themoviedb.org/3/person/1158/movie_credits?language=en-US'
    url='https://api.themoviedb.org/3/person/'+str(actor_pk)+'/movie_credits?api_key='+my_id+'&language=ko'
    response=requests.get(url)
    # print(response.json())
    data=response.json()
    return [data]

@api_view(['GET'])
def index(request):
    movies_data=Movies_data()
    # print(movies_data)
    serializer=MovieListSerializer(movies_data,many=True)
    serialized_data = serializer.data
    # print(serialized_data)
    data=Genre_data()
    # print(data)
    # return Response(serializer.data,status=status.HTTP_201_CREATED)
    return render(request,'movies/index.html',{'resdatas':serialized_data,'datas':data})
    

@require_safe
# @login_required
def detail(request,movie_pk):
    movie_data=Movie_data(movie_pk)
    actor_data=Actor_data(movie_pk)
    # print(actor_data)
    serializer1=MovieDetailSerializer(movie_data,many=True)
    serialized_data1 = serializer1.data
    serializer2=ActorList(actor_data,many=True)
    # print(serializer2.data)
    serialized_data2 = serializer2.data
    comment_form = CommentForm()
    # print(serialized_data2[0]['name'])
    comments=Comment.objects.all()
    comment=Comment.objects.filter(movie=movie_pk)
    # print(comment)
    C=[]
    for i in comments:
        if int(i.movie)==movie_pk:
            C.append(i)

    return render(request, 'movies/detail.html',{'resdatas':serialized_data1[0],'datas':serialized_data2[0]['name'],'comment_form':comment_form,'comments':C,'comment':comment})

@login_required
def actor_detail(request,actor_pk):
    actor_data=Actor_Detail_data(actor_pk)
    serializer=ActorDetail(actor_data,many=True)
    # print(serializer2.data)
    serialized_data = serializer.data
    # print(serialized_data)
    # print(serialized_data)
    # print(serialized_data[0]['cast'])
    return render(request, 'movies/actordetail.html',{'resdatas':serialized_data[0]['cast']})
    # return 

@require_POST
def comment_create(request,movie_pk):
    if request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie_pk
            comment.user = request.user
            comment.save()
        return redirect('movies:detail', movie_pk)
    return redirect('accounts:login')



@require_POST
def comments_delete(request,comment_pk,movie_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)



