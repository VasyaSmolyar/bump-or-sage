from django.urls import path
from . import views

app_name = 'myauth'

urlpatterns = [
  path('',views.auth,name='login'),
  path('logout/',views.log_out,name='logout'),
  path('reg/',views.reg,name='reg')
]
