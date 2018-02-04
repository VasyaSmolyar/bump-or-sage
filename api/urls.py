from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('',views.index,name='index'),
    path('image/',views.images,name='image'),
    path('user/',views.users,name='users'),
    path('user/<int:uid>/',views.get_user,name='get_user'),
    path('top/<str:bump>/',views.top,name="top")
]
