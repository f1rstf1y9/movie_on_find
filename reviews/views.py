from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from reviews.models import Review,Comment
from movies.models import Movie
from cards.models import Card
from django import forms
from reviews.forms import ReviewForm,CommentForm
from django.http import JsonResponse
# Create your views here.
# @require_safe
# def index(request):
#     cards=Card.objects.all()
#     poster=[]
#     for i in cards:
#         m=Movie.objects.get(id=i.movie_id).poster_path
#         data = {
#             'pk':i.id,
#             'user':i.user,
#             'title':i.title,
#             'content' :i.content,
#             'like_users':i.like_users,
#             'movie':i.movie,
#             'created_at' :i.created_at, 
#             'updated_at' :i.updated_at,
#             'poster_path' :m
#     }
#         poster.append(data)
#     return render(request,'cards/index.html',{'poster':poster})

@login_required
@require_http_methods(['GET', 'POST'])
def create(request, movie_pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            movie = Movie.objects.get(pk=movie_pk)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.movie = movie
                review.save()
                return redirect('movies:detail', movie_pk)
        else:
            form = ReviewForm()
        return render(request, 'reviews/create.html', {'pk':movie_pk,'form': form})
    return redirect('accounts:login')

@require_safe
def detail(request, pk):
    review = Review.objects.get(pk=pk)
    movie=Movie.objects.get(pk=review.movie_id)
    comment_form = CommentForm()
    comments = review.comment_set.all()
    movie=Movie.objects.get(pk=review.movie_id)
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
        'review': review,
        'movie':movie,
        'comment_form': comment_form,
        'comments': L,
        'movie':movie
    }
    return render(request, 'reviews/detail.html', context)

@require_POST
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            n=review.movie_id
            review.delete()
            return redirect('movies:detail',n)

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('reviews:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
    else:
        return redirect('reviews:detail', review.pk)
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'reviews/update.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        review = Review.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
        return redirect('reviews:detail', review.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('reviews:detail', review_pk)

@require_POST
def likes(request, review_pk):
    if request.user.is_authenticated:
        review = Review.objects.get(pk=review_pk)
        if review.user_id==request.user.pk:
            pass
        else:
            if review.like_users.filter(pk=request.user.pk).exists():
                review.like_users.remove(request.user)
                is_liked = False
                likes=review.like_users.all()
            else:
                review.like_users.add(request.user)
                is_liked = True
                likes=review.like_users.all()
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
