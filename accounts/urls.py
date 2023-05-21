from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('password/', views.change_password, name='change_password'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/followers', views.followers, name='followers'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('email_login', views.email_login, name="email_login"),
    path('kakao_login', views.kakao_login, name="kakao_login"),
    path('kakao_login/callback', views.kakao_login_callback, name="kakao_login_callback"),
]