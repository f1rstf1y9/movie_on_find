from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from movies.serializers import MovieListSerializer,MovieDetailSerializer
from django.core import serializers
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST, require_safe, require_http_methods
import requests
import json
from card_collections.models import Card_collection
from movies.models import Genre
from reviews.models import Review
from cards.models import Card
from accounts.models import User
from django.db import transaction
from movies.forms import Searchform
from django.template.defaulttags import register

@register.filter(name='split')
def split(value, key): 
    return value.split(key)[0]

my_id='4d159f322795f49ab1e9bb06b61577fb'
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
                    "original_title":i.get("original_title"),
                    "vote_average":i.get("vote_average"),
                    "popularity":i.get("popularity"),
                    "overview":i.get("overview"),
                    "poster_path":i.get("poster_path"),
                    "backdrop_path":i.get("backdrop_path"),
                    "release_date":i.get("release_date"),
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
def data_sort():
    movie=Movie.objects.all()
    for i in movie:
        if i.overview=='':
            i.delete()

def recommend(id):
    genre=Genre.objects.filter(like_users=id).values()
    G=[]
    for i in genre:
        G.append(i['name'])
    print(G)
    return set(G)
@api_view(['GET'])
def index(request):
    # get_top_rated_data()
    # data_sort()
    # get_movie_video()
    movie=Movie.objects.all().order_by('-vote_average')[:10]
    genre=Genre.objects.values()
    serializer=MovieListSerializer(movie,many=True)
    serialized_data = serializer.data
    if request.user.is_authenticated:
        rec=recommend(request.user.id)
        rec_movie=Movie.objects.all()
        L=[]
        for i in rec_movie:
            D=[]
            for j in i.genres.all().values():
                D.append(j['name'])
            a=set.intersection(set(D),rec)
            if abs(len(rec)-len(a))<2:
                L.append(i)
    else:
        L = []

    collections=Card_collection.objects.all()
    return render(request,'movies/index.html',{'resdatas':serialized_data,'datas':genre,'collections':collections,'rec':L})

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
    context={
        'resdatas':serialized_data1,
        'datas':genre,
        'reviews':reviews,
        'cards':cards
    }
    return render(request, 'movies/detail.html',context)

def genre_sort(request,genre_pk):
    print(type(genre_pk))
    # 모험
    if genre_pk==12:
        movie=Movie.objects.filter(genres=genre_pk)
    # 판타지
    elif genre_pk==14:
        movie=Movie.objects.filter(genres=genre_pk)
    # 애니메이션
    elif genre_pk==16:
        movie=Movie.objects.filter(genres=genre_pk)
    # 드라마
    elif genre_pk==18:
        movie=Movie.objects.filter(genres=genre_pk)
    # 공포
    elif genre_pk==27:
        movie=Movie.objects.filter(genres=genre_pk)
    # 액션
    elif genre_pk==28:
        movie=Movie.objects.filter(genres=genre_pk)
    # 코미디
    elif genre_pk==35:
        movie=Movie.objects.filter(genres=genre_pk)
    # 역사
    elif genre_pk==36:
        movie=Movie.objects.filter(genres=genre_pk)
    # 서부
    elif genre_pk==37:
        movie=Movie.objects.filter(genres=genre_pk)
    # 스릴러
    elif genre_pk==53:
        movie=Movie.objects.filter(genres=genre_pk)
    # 범죄
    elif genre_pk==80:
        movie=Movie.objects.filter(genres=genre_pk)
    # 다큐멘터리
    elif genre_pk==99:
        movie=Movie.objects.filter(genres=genre_pk)
    # SF
    elif genre_pk==878:
        movie=Movie.objects.filter(genres=genre_pk)
    # 미스터리
    elif genre_pk==9648:
        movie=Movie.objects.filter(genres=genre_pk)
    # 음악
    elif genre_pk==10402:
        movie=Movie.objects.filter(genres=genre_pk)
    # 로맨스
    elif genre_pk==10749:
        movie=Movie.objects.filter(genres=genre_pk)
    # 가족
    elif genre_pk==10751:
        movie=Movie.objects.filter(genres=genre_pk)
    # 전쟁
    elif genre_pk==10752:
        movie=Movie.objects.filter(genres=genre_pk)
    # TV 영화
    elif genre_pk==10770:
        movie=Movie.objects.filter(genres=genre_pk)
    genre=Genre.objects.values()
    serializer=MovieListSerializer(movie,many=True)
    serialized_data = serializer.data
    return render(request,'movies/sort.html',{'resdatas':serialized_data,'datas':genre})

def sort(request,pk):
    # 평점순
    if pk==1:
        movie=Movie.objects.all().order_by('-vote_average')
    #인기도순
    elif pk==2:
        movie=Movie.objects.all().order_by('-popularity')
    #개봉일순
    elif pk==3:
        movie=Movie.objects.all().order_by('-release_date')
    genre=Genre.objects.values()
    serializer=MovieListSerializer(movie,many=True)
    serialized_data = serializer.data
    return render(request,'movies/sort.html',{'resdatas':serialized_data,'datas':genre})


@api_view(['GET'])
def search(request):
    form =Searchform(request.GET)
    movies=Movie.objects.all()
    blind={'ans':False}
    if form.is_valid():
        keyword=form.cleaned_data.get('keyword')
        if keyword:
            blind={'ans':True}
            movies=movies.filter(title__icontains=keyword)
    context={
        'form':form,
        'movies':movies,
        'blind':blind
    }
    return render(request,'movies/search.html',context)

@require_POST
def watching(request, card_pk):
    if request.user.is_authenticated:
        card = Card.objects.get(pk=card_pk)
        if card.user_id==request.user.pk:
            pass
        else:
            if card.like_users.filter(pk=request.user.pk).exists():
                card.like_users.remove(request.user)
                is_liked = False
                likes=card.like_users.all()
            else:
                card.like_users.add(request.user)
                is_liked = True
                likes=card.like_users.all()
            context = {
                'is_liked': is_liked,
                'likes':len(likes),
            }
            return JsonResponse(context)
    return redirect('accounts:login')

@require_POST
def watched(request, card_pk):
    if request.user.is_authenticated:
        card = Card.objects.get(pk=card_pk)
        if card.user_id==request.user.pk:
            pass
        else:
            if card.like_users.filter(pk=request.user.pk).exists():
                card.like_users.remove(request.user)
                is_liked = False
                likes=card.like_users.all()
            else:
                card.like_users.add(request.user)
                is_liked = True
                likes=card.like_users.all()
            context = {
                'is_liked': is_liked,
                'likes':len(likes),
            }
            return JsonResponse(context)
    return redirect('accounts:login')

@require_POST
def interest(request, card_pk):
    if request.user.is_authenticated:
        card = Card.objects.get(pk=card_pk)
        if card.user_id==request.user.pk:
            pass
        else:
            if card.like_users.filter(pk=request.user.pk).exists():
                card.like_users.remove(request.user)
                is_liked = False
                likes=card.like_users.all()
            else:
                card.like_users.add(request.user)
                is_liked = True
                likes=card.like_users.all()
            context = {
                'is_liked': is_liked,
                'likes':len(likes),
            }
            return JsonResponse(context)
    return redirect('accounts:login')