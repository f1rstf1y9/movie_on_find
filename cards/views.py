from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from cards.models import Card,Comment
from movies.models import Movie
from django import forms
from cards.forms import CardForm,CommentForm
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
        if request.method == 'POST':
            form = CardForm(request.POST)
            movie = Movie.objects.get(pk=movie_pk)
            if form.is_valid():
                print(1)
                card = form.save(commit=False)
                card.user = request.user
                card.movie = movie
                card.movie_posterpath = movie.poster_path
                card.save()
                return redirect('cards:detail', card.pk)
        else:
            print(2)
            form = CardForm()
        return render(request, 'cards/create.html', {'pk':movie_pk,'form': form})
    return redirect('accounts:login')

@require_safe
def detail(request, pk):
    card = Card.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = card.comment_set.all()
    likes=len(card.like_users.all())
    movie=Movie.objects.get(pk=card.movie_id)
    L=[]
    for i in comments:
        c=Comment.objects.get(pk=i.id)
        data = {
            'pk':i.id,
            'user':c.user,
            'content' :c.content,
            'like_users':c.like_users.all(),
    }
        L.append(data)
    context = {
        'card': card,
        'comment_form': comment_form,
        'comments': L,
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
            form = CardForm(request.POST, instance=card)
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
def comments_create(request, pk):
    if request.user.is_authenticated:
        card = Card.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.card = card
            comment.user = request.user
            comment.save()
        return redirect('cards:detail', card.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, card_pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('cards:detail', card_pk)


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

@require_POST
def comment_likes(request, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if comment.user_id==request.user.pk:
            pass
        else:
            if comment.like_users.filter(pk=request.user.pk).exists():
                comment.like_users.remove(request.user)
                is_commentliked = False
                commentlikes=comment.like_users.all()
            else:
                comment.like_users.add(request.user)
                is_commentliked = True
                commentlikes=comment.like_users.all()
            context = {
                'is_commentliked': is_commentliked,
                'commentlikes':len(commentlikes),
            }
            return JsonResponse(context)
    return redirect('accounts:login')