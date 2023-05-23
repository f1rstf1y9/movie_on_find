from django.urls import path
from . import views

app_name = 'card_collections'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:card_collection_pk>/likes/', views.likes, name='likes'),path('<int:pk>', views.detail, name='detail'),
]