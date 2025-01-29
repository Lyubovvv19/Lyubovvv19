from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name ='pars'
urlpatterns = [
    path('', views.pars, name='pars'),
    path('login/', views.login_pars, name='login'),
    path('logout/', views.logout_pars, name='logout'),
    path('rez/', views.rez_pars, name='rez')
]