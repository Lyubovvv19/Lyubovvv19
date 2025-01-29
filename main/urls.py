from django.urls import path
from . import views
app_name ='main'
urlpatterns = [
    path('', views.index, name='home'),
    path('group', views.group, name='group'),
    path('teacher', views.teacher, name='teacher')
]