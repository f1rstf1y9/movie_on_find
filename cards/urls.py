from django.urls import path
from . import views

app_name = 'cards'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    # path('<int:pk>/create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:card_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:card_pk>/likes/', views.likes, name='likes'),path('', views.index, name='index'),
    path('<int:comment_pk>/comment_likes/', views.comment_likes, name='comment_likes'),path('', views.index, name='index'),
]