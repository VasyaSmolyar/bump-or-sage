from django.urls import path,include
from . import views

app_name = 'index'

urlpatterns = [
    path('',views.index,name='index'),
    path('pull/<int:img_id>',views.pull,name='pull'),
    path('top',views.bump,name='bump'),
    path('top/<str:bump>',views.bump,name='top'),
    path('user/',views.user,name='user'),
    path('user/<int:uid>',views.user,name='userid'),
    path('loadimg/',views.loadimg,name='loadimg'),
    path('dev/',views.token,name='token'),
    path('dev/new_token',views.new_token,name='new_token')
]
