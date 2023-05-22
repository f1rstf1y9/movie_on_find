from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.urls import reverse
import requests

# Create your views here.
def review(request, review_pk):
    return render(request, 'reviews/index.html')