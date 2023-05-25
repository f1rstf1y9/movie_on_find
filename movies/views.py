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
from django.db.models import FloatField
from django.db.models.functions import Cast


@register.filter(name='split')
def split(value, key): 
    if value:
        return value.split(key)[0]
    return ''

my_id='f0ee4eefc21a888bf1229e2d951df4e6'
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
                    "runtime": i.get("runtime"),
                    "interest":[],
                    "watched":[],
                    "watching":[],
                    },
            }
            result.append(movie_dict)
    return result
# with open('movies/fixtures/movie.json','w',encoding="UTF-8") as f:
#     json.dump(get_top_rated_data(),f,ensure_ascii=False,indent=2)


# get_object_or_404, get_list_or_404(Movie)
def get_movie_video():
    movie=Movie.objects.all()
    for i in movie:
        url='https://api.themoviedb.org/3/movie/'+str(i.pk)+'/videos?api_key='+my_id+'&language=ko'
        response=requests.get(url).json()
        data=response['results']
        if len(data)==0:
            pass
        else:
            key=data[0]['key']
            i.video=key
            i.save()

def get_movie_runtime():
    movie=Movie.objects.all()
    for i in movie:
        url1='https://api.themoviedb.org/3/movie/'+str(i.pk)+'?api_key='+my_id+'&language=ko'
        response1=requests.get(url1).json()
        data1=response1['runtime']
        i.runtime=data1
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
    return set(G)

@api_view(['GET'])
def index(request):
    # data_sort()
    # get_movie_video()
    # get_movie_runtime()
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
            if len(a)>=2 and len(a)!=0:
                L.append(i)
    else:
        L = []
    L.sort(key=lambda x: x.vote_average, reverse=True)
    collections=Card_collection.objects.all().order_by('updated_at')[:10]
    cards=Card.objects.all().order_by('created_at')[:10]
    return render(request,'movies/index.html',{'resdatas':serialized_data,'datas':genre,'collections':collections,'cards':cards,'rec':L})

@api_view(['GET'])
@login_required
def my_reco(request,num):
    if request.user.is_authenticated:
        rec=recommend(request.user.id)
        rec_movie=Movie.objects.all()
        L=[]
        for i in rec_movie:
            D=[]
            for j in i.genres.all().values():
                D.append(j['name'])
            # a=set.intersection(set(D),rec)
            a=set(D)&rec
            if len(a)>=2 and len(a)!=0:
                L.append(i)
    else:
        L = []
    A=[]
    L.sort(key=lambda x: x.vote_average, reverse=True)
    for i in range(1,len(L)//6+2):
        A.append(i)
    genre=Genre.objects.values()
    return render(request,'movies/myreco.html',{'resdatas':L[6*(num-1):6*num],'datas':genre,'total':A})

@require_safe
@login_required
@api_view(['GET'])
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

@api_view(['GET'])
def sort(request,pk,num):
    # 평점순
    if pk==1:
        print(pk)
        movie=Movie.objects.all().order_by('-vote_average')[5*(num-1):5*num]
    #인기도순
    elif pk==2:
        print(pk)
        movie=Movie.objects.all().order_by(Cast('popularity', FloatField()).desc())[5*(num-1):5*num]
    #개봉일순
    elif pk==3:
        print(pk)
        movie=Movie.objects.all().order_by('-release_date')[5*(num-1):5*num]
    genre=Genre.objects.values()
    serializer=MovieListSerializer(movie,many=True)
    serialized_data = serializer.data
    movie1=Movie.objects.all()
    A=[]
    for i in range(1,len(movie1)//20+2):
        A.append(i)
    G=1
    return render(request,'movies/sort.html',{'resdatas':serialized_data,'datas':genre,'total':A,'pk':pk,'G':G})

@api_view(['GET'])
def genre_sort(request,genre_pk,n,m):
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
    A=[]
    for i in range(1,len(movie)//20+2):
        A.append(i)
    genre=Genre.objects.values()
    if m==1:
        serializer=MovieListSerializer(movie.order_by('-vote_average')[5*(n-1):5*n],many=True)
    elif m==2:
        serializer=MovieListSerializer(movie.order_by(Cast('popularity', FloatField()).desc())[5*(n-1):5*n],many=True)
    elif m==3:
        serializer=MovieListSerializer(movie.order_by('-release_date')[5*(n-1):5*n],many=True)
    serialized_data = serializer.data
    # print(serialized_data)
    return render(request,'movies/sort.html',{'resdatas':serialized_data,'datas':genre,'total':A,'pk':n,'genre_id':genre_pk,'m':m})


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

@api_view(['POST'])
def watching(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if movie.watching==request.user.pk:
            pass
        else:
            if movie.watching.filter(pk=request.user.pk).exists():
                movie.watching.remove(request.user)
                is_watching = False
            else:
                movie.watching.add(request.user)
                is_watching = True
            context = {
                'is_watching': is_watching,
            }
            return JsonResponse(context)
    return redirect('accounts:login')

@api_view(['POST'])
def watched(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if movie.watched==request.user.pk:
            pass
        else:
            if movie.watched.filter(pk=request.user.pk).exists():
                movie.watched.remove(request.user)
                is_watched = False
            else:
                movie.watched.add(request.user)
                is_watched = True
            context = {
                'is_watched': is_watched,
            }
            return JsonResponse(context)
    return redirect('accounts:login')

@api_view(['POST'])
def interest(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if movie.interest==request.user.pk:
            pass
        else:
            if movie.interest.filter(pk=request.user.pk).exists():
                movie.interest.remove(request.user)
                is_interest = False
            else:
                movie.interest.add(request.user)
                is_interest = True
            context = {
                'is_interest': is_interest,
            }
            return JsonResponse(context)
    return redirect('accounts:login')