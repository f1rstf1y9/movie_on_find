from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from card_collections.models import Card_collection
from movies.models import Movie
from cards.models import Card
from django import forms
from card_collections.forms import CollectionForm
from django.http import JsonResponse
# Create your views here.
@require_safe
def index(request):
    card_collections=Card_collection.objects.all()
    return render(request,'card_collections/index.html',{'card_collections':card_collections})


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.user.is_authenticated:
        my_cards=Card.objects.filter(user=request.user)
        if request.method == 'POST':
            form = CollectionForm(request.POST,user=request.user)
            if form.is_valid():
                card_collections = form.save(commit=False)
                card_collections.user = request.user
                card_collections.save()
                form.save_m2m()
                return redirect('card_collections:detail', card_collections.pk)
        else:
            form =CollectionForm(user=request.user)
        return render(request, 'card_collections/create.html', {'form': form,'my_cards': my_cards})
    return redirect('accounts:login')

@require_safe
def detail(request, pk):
    card_collection = Card_collection.objects.get(pk=pk)
    context = {
        'card_collection': card_collection,
    }
    return render(request, 'card_collections/detail.html', context)

@require_POST
def delete(request, pk):
    card_collection = Card_collection.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user == card_collection.user:
            card_collection.delete()
            return redirect('card_collections:index')

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    card_collection = Card_collection.objects.get(pk=pk)
    if request.user == card_collection.user:
        if request.method == 'POST':
            form = CollectionForm(request.POST,user=request.user,instance=card_collection)
            if form.is_valid():
                form.save()
                return redirect('card_collections:detail', card_collection.pk)
        else:
            form = CollectionForm(user=request.user,instance=card_collection)
    else:
        return redirect('card_collections:index')
    print(form)
    context = {
        'form': form,
        'card_collection': card_collection,
    }
    return render(request, 'card_collections/update.html', context)

@require_POST
def likes(request, card_collection_pk):
    if request.user.is_authenticated:
        card_collection = Card_collection.objects.get(pk=card_collection_pk)
        print(card_collection)
        if card_collection.user_id==request.user.pk:
            pass
        else:
            if card_collection.like_users.filter(pk=request.user.pk).exists():
                card_collection.like_users.remove(request.user)
                is_liked = False
                likes=card_collection.like_users.all()
            else:
                card_collection.like_users.add(request.user)
                is_liked = True
                likes=card_collection.like_users.all()
            context = {
                'is_liked': is_liked,
                'likes':len(likes),
            }
            return JsonResponse(context)
    return redirect('accounts:login')