from django.http import HttpResponseForbidden
from .models import Api
import time
import os
import hashlib

def check_token(token):
    try:
        token = Api.objects.get(token=token)
        return True
    except Api.DoesNotExist:
        return False

def api_token(func):
    def _check(request,*args,**kwargs):
        if request.method == 'GET':
            data = request.GET
        else:
            data = request.POST
        if 'token' in data and check_token(data['token']):
            return func(request,*args,**kwargs)
        return HttpResponseForbidden()
    return _check

def code():
    t1 = time.time()
    t2 = ''.join([hex(c).replace('0x','') for c in os.urandom(8)])
    code = hashlib.md5((str(t1)+t2).encode()).hexdigest()
    return code

def create(user):
    try:
        token = Api.objects.get(user=user)
        token.token = code()
        token.save()
        return token
    except Api.DoesNotExist:
        token = Api.objects.create(user=user,token=code())
        token.save()
        return token

def read(user):
    try:
        token = Api.objects.get(user=user)
        return token.token
    except Api.DoesNotExist:
        token = create(user)
        return token.token
