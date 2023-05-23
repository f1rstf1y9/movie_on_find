from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from cards.models import Card
from movies.models import Movie
from django import forms
from cards.forms import CardForm
from django.http import JsonResponse
# Create your views here.
@require_safe
def index(request):
    cards=Card.objects.all()
    poster=[]
    for i in cards:
        m=Movie.objects.get(id=i.movie_id).poster_path
        data = {
            'pk':i.id,
            'user':i.user,
            'title':i.title,
            'content' :i.content,
            'like_users':i.like_users,
            'movie':i.movie,
            'created_at' :i.created_at, 
            'updated_at' :i.updated_at,
            'poster_path' :m
    }
        poster.append(data)
    return render(request,'cards/index.html',{'poster':poster})

@login_required
@require_http_methods(['GET', 'POST'])
def create(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if request.method == 'POST':
            form = CardForm(request.POST, request.FILES)
            
            if form.is_valid():
                card = form.save(commit=False)
                card.user = request.user
                card.movie = movie
                card.save()
                return redirect('cards:detail', card.pk)
        else:
            form = CardForm()
        return render(request, 'cards/create.html', {'movie':movie,'form': form})
    return redirect('accounts:login')

@require_safe
def detail(request, pk):
    card = Card.objects.get(pk=pk)
    likes=len(card.like_users.all())
    movie=Movie.objects.get(pk=card.movie_id)
    context = {
        'card': card,
        'likes':likes,
        'movie':movie
    }
    return render(request, 'cards/detail.html', context)

@require_POST
def delete(request, pk):
    card = Card.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user == card.user:
            card.delete()
            return redirect('cards:index')

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    card = Card.objects.get(pk=pk)
    if request.user == card.user:
        if request.method == 'POST':
            form = CardForm(request.POST, request.FILES, instance=card)
            if form.is_valid():
                form.save()
                return redirect('cards:detail', card.pk)
        else:
            form = CardForm(instance=card)
    else:
        return redirect('cards:index')
    context = {
        'form': form,
        'card': card,
    }
    return render(request, 'cards/update.html', context)

@require_POST
def likes(request, card_pk):
    if request.user.is_authenticated:
        card = Card.objects.get(pk=card_pk)
        if card.user_id==request.user.pk:
            pass
        else:
            if card.like_users.filter(pk=request.user.pk).exists():
                card.like_users.remove(request.user)
                is_liked = False
                likes=card.like_users.all()
            else:
                card.like_users.add(request.user)
                is_liked = True
                likes=card.like_users.all()
            context = {
                'is_liked': is_liked,
                'likes':len(likes),
            }
            return JsonResponse(context)
    return redirect('accounts:login')