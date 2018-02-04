from django.shortcuts import render
from django.http import JsonResponse, Http404
from .api_funcs import api_token
from index.models import Image, Vote
from django.contrib.auth.models import User

# Create your views here.
@api_token
def index(request):
    return JsonResponse({'response' : "Доступ к API еcть"})

@api_token
def images(request):
    imgs = Image.objects.all()
    response = [{'img_url' : i.img_url, 'votes' : i.votes, 'user_id' : i.user_id} for i in imgs]
    return JsonResponse({'response' : response})

@api_token
def get_user(request,uid):
    try:
        user = User.objects.get(pk=uid)
        imgs = Image.objects.filter(user=user).all()
        user_images = [{'img_url' : i.img_url, 'votes' : i.votes, 'user_id' : i.user_id} for i in imgs]
        rating = sum([i['votes'] for i in user_images])
        response = {
            'username' : user.username,
            'rating' : rating,
            'user_images' : user_images,
        }
    except User.DoesNotExist:
        response = {'error' : 'Пользователя с данным id не существует' }
    finally:
        return JsonResponse({'response' : response})

@api_token
def users(request):
    users = User.objects.order_by('id').all()
    response = [{'id' : u.id, 'username' : u.username} for u in users]
    return JsonResponse({'response' : response})

@api_token
def top(request,bump = 'bump'):
    if bump == "bump":
        imgs = Image.objects.order_by('-votes').all()[:100]
    elif bump == "sage":
        imgs = Image.objects.order_by('votes').all()[:100]
    else:
        raise Http404("Страница не найдена")
    response = [{'img_url' : i.img_url, 'votes' : i.votes, 'user_id' : i.user_id} for i in imgs]
    return JsonResponse({'response' : response })
