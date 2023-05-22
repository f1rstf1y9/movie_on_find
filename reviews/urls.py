from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('<int:review_pk>/', views.review, name='review'),
]