from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    # path('<int:actor_pk>/detail/', views.actor_detail, name='actor_detail'),
]