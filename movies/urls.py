from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('genre_sort/<int:genre_pk>/', views.genre_sort, name='genre_sort'),
    path('sort/<int:pk>/', views.sort, name='sort'),
    path('<int:movie_pk>/interest/', views.interest, name='interest'),path('', views.index, name='index'),
    path('<int:movie_pk>/watching/', views.watching, name='watching'),path('', views.index, name='index'),
    path('<int:movie_pk>/watched/', views.watched, name='watched'),path('', views.index, name='index'),
]