from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/review', views.index, name='review'),
    path('<int:review_pk>/comment', views.index, name='comment'),
    path('<int:actor_pk>/detail/', views.actor_detail, name='actor_detail'),
]