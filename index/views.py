from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from .models import Image, Vote
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from random import randint
from django.urls import reverse
from django.db.models import F
from django.contrib.auth.decorators import login_required
from .forms import LoadForm
from .img import check_img

# Вспомогательные функиции

def check_url(url):
    return check_img(url)

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request,'landing.html',{})
    votes = Vote.objects.filter(user = request.user).all()
    votes = {i.img for i in votes}
    imgs = set(Image.objects.all())
    imgs = list(imgs - votes)
    if len(imgs) == 0:
        return render(request,'index.html', {'img' : False})
    pk = randint(0,len(imgs)-1)
    return render(request,'index.html', { 'img' : imgs[pk] })


@login_required
def pull(request,img_id):
    try:
        val = request.POST['vote']
        if val == 'BUMP':
            vote = 1
        elif val == 'SAGE':
            vote = -1
        else:
            raise KeyError
        img = Image.objects.get(pk=img_id)
        img.votes = F('votes') + vote
        img.save()
        vote = Vote.objects.create(img = img, user = request.user)
        vote.save()
    except (KeyError,Image.DoesNotExist):
        pass
    return redirect(reverse('index:index'))

def bump(request,bump='bump'):
    if bump == "bump":
        imgs = Image.objects.order_by('-votes').all()[:100]
    elif bump == "sage":
        imgs = Image.objects.order_by('votes').all()[:100]
    else:
        raise Http404("Страница не найдена")
    page = Paginator(imgs,10)
    if 'page' in request.GET:
        pid = request.GET['page']
    else:
        pid = 1
    return render(request,'list.html',{'imgs' : page.get_page(pid), 'top' : bump.upper()})

def user(request,uid = 0):
    if uid == 0:
        if not request.user.is_authenticated:
            return redirect(reverse('myauth:login'))
        udata = request.user
    else:
        udata = get_object_or_404(User,pk = uid)
    imgs = Image.objects.filter(user=udata).all()[:10]
    rating = sum([i.votes for i in imgs])
    return render(request,'user.html',{'user' : udata, 'imgs' : imgs,
    'rating' : rating })

@login_required
def loadimg(request):
    form = LoadForm(request.POST)
    if form.is_valid():
        url = form.cleaned_data['url']
        if check_url(url):
            img = Image(img_url = url,user = request.user)
            img.save()
            return render(request,'upload.html',{'ok' : 'Картинка загружена', 'form' : LoadForm()})
        else:
            return render(request,'upload.html',{'err' : 'Введите адрес картинки', 'form' : form })
    else:
        return render(request,'upload.html',{'form' : LoadForm()})
        
