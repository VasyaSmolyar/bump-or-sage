from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.db.utils import IntegrityError
from .forms import RegForm

# Вспомогательные функции

def get_of_false(obj,**kwargs):
    try:
        return obj.get(**kwargs)
    except User.DoesNotExist:
        return False

def not_login(func):
    def ret_me(*args,**kwargs):
        request = args[0]
        if not request.user.is_authenticated:
            return func(*args,**kwargs)
        else:
            return redirect('/')
    return ret_me

# Собственно, контроллеры
@not_login
def auth(request):
    try:
        uname = request.POST['login']
        upass = request.POST['pwd']
        user = authenticate(request,username=uname,password=upass)
        if not user:
            data = {
                'err' : 'Неправильный логин или пароль',
            }
            return render(request,'login.html',data)
        else:
            login(request,user)
<<<<<<< HEAD
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect(reverse('index:index'))
=======
            return redirect('index:index')
>>>>>>> 026dd696a308ccaea197609a21a7b4c524bf0c98
    except KeyError:
        return render(request,'login.html',{})

def log_out(request):
    logout(request)
    return redirect('index:index')

@not_login
def reg(request):
    if request.method == "GET":
        return render(request,'reg.html',{'form' : RegForm(),})
    try:
        form = RegForm(request.POST)
        if not form.is_valid():
            newform = RegForm()
            return render(request,'reg.html',{'form' : newform, 'errors' : form.errors})
        uname = request.POST['login']
        uemail = request.POST['email']
        upass = request.POST['pwd']
        user = get_of_false(User.objects,username=uname)
        if user:
            return render(request,'reg.html',{'err' : 'Логин занят!', 'form' : form})
        user = User.objects.create_user(uname,uemail,upass)
    except IntegrityError:
        '''
        Этот костыль создан с целью обойти баг Django, т.к исключение
        генерируется даже когда логина не существует
        '''
        pass

    if user is not None:
        login(request,user)
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    return redirect(reverse('index:index'))
