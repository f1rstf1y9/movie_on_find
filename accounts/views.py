from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from .forms import UserCreationForm, UserChangeForm
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.urls import reverse
import requests

# Create your views here.
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    return render(request, 'accounts/login.html')

def email_login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/email_login.html', context)

# 카카오 로그인
def kakao_login(request):
    app_key = 'f98c6a2b8ef11b33b283997a2f0caca9'
    redirect_uri = 'http://127.0.0.1:8000/accounts/kakao_login/callback'
    kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
    return redirect(f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}')

def find_user_by_kakao_id(login_kakao_id):
    User = get_user_model()
    try:
        current_user = User.objects.get(kakao_id=login_kakao_id)
        return current_user
    except User.DoesNotExist:
        return None

def kakao_login_callback(request):
    print(request.GET.get('code'))
    auth_code = request.GET.get('code')
    kakao_token_api = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': 'f98c6a2b8ef11b33b283997a2f0caca9',
        'redirection_uri': 'http://127.0.0.1:8000/accounts/kakao_login/callback',
        'code': auth_code,
    }

    token_response = requests.post(kakao_token_api, data=data)
    access_token = token_response.json().get('access_token')
    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
    
    login_kakao_id = user_info_response.json().get('id')
    current_user = find_user_by_kakao_id(login_kakao_id)
    if current_user:
        auth_login(request, current_user)
        return redirect('movies:index')
    else:
        request.session['user_info'] = user_info_response.json()
        return redirect('accounts:signup')

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        initial_data = {}
        if request.session.get('user_info'):
            user_info = request.session.get('user_info')
            initial_data['kakao_id'] = user_info.get('id', None)
            initial_data['email'] = user_info['kakao_account'].get('email', None)
            initial_data['nickname'] = user_info['properties'].get('nickname', None)
        else:
            initial_data['kakao_id'] = '0'
        form = UserCreationForm(initial=initial_data)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)

@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)

@require_POST
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('movies:index')

def profile(request, username):
    User = get_user_model()
    person = User.objects.get(email=username)
    total_watched_time = 0
    for movie in person.watched_movies.all():
        total_watched_time += movie.runtime
    context = {
        'person': person,
        'total_watched_time': total_watched_time,
    }
    return render(request, 'accounts/profile.html', context)

@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        User = get_user_model()
        person = User.objects.get(pk=user_pk)
        if person != request.user:
            if person.followers.filter(pk=request.user.pk).exists():
                person.followers.remove(request.user)
            else:
                person.followers.add(request.user)
        return redirect('accounts:profile', person.email)
    return redirect('accounts:login')

@require_POST
def list_follow(request, current_user, follow_user, category):
    if request.user.is_authenticated:
        User = get_user_model()
        follow = User.objects.get(pk=follow_user)
        if follow != request.user:
            if follow.followers.filter(pk=request.user.pk).exists():
                follow.followers.remove(request.user)
            else:
                follow.followers.add(request.user)
        if category == 1:
          return redirect('accounts:followers', current_user)
        else:
          return redirect('accounts:followings', current_user)
          
    return redirect('accounts:login')

@require_safe
def followings(request, username):
    User = get_user_model()
    person = User.objects.get(email=username)
    if request.user.is_authenticated:
        followings_list = person.followings.all()
        context = {
            'person' : person,
            'followings_list': followings_list,
        }
        return render(request, 'accounts/followings.html', context)

@require_safe
def followers(request, username):
    User = get_user_model()
    person = User.objects.get(email=username)
    if request.user.is_authenticated:
        followers_list = person.followers.all()
        context = {
            'person' : person,
            'followers_list': followers_list,
        }
        return render(request, 'accounts/followers.html', context)
    
def interest(request, username):
    User = get_user_model()
    person = User.objects.get(email=username)
    context = {
        'person' : person,
    }
    return render(request, 'accounts/interest.html', context)
    
def watching(request, username):
    User = get_user_model()
    person = User.objects.get(email=username)
    context = {
        'person' : person,
    }
    return render(request, 'accounts/watching.html', context)
    
def watched(request, username):
    User = get_user_model()
    person = User.objects.get(email=username)
    context = {
        'person' : person,
    }
    return render(request, 'accounts/watched.html', context)

def reviews(request, username):
    User = get_user_model()
    person = User.objects.get(email=username)
    context = {
        'person' : person,
    }
    return render(request, 'accounts/reviews.html', context)