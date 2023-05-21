from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/comment/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    # path('<int:review_pk>/like', views.movie_like, name='like'),
    path('<int:actor_pk>/detail/', views.actor_detail, name='actor_detail'),
]