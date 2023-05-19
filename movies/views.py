from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
@require_safe
def index(request):
    # movies = Movie.objects.all()
    # context = {
    #     'movies': movies,
    # }
    return render(request, 'movies/index.html')