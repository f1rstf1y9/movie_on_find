from django.urls import path
from . import views


app_name = 'reviews'
urlpatterns = [
    path('<int:movie_pk>/create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:review_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:review_pk>/likes/', views.likes, name='likes'),path('<int:pk>', views.detail, name='detail'),
    path('<int:comment_pk>/comment_likes/', views.comment_likes, name='comment_likes'),path('<int:pk>', views.detail, name='detail'),
]