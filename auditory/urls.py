from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name ='auditory'
urlpatterns = [
    path('', views.aud, name='auditory'),
    path('aa/', views.aa, name='aa'),

]