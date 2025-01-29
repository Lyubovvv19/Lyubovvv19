from django.urls import path
from . import views
app_name ='mainn'
urlpatterns = [
    path('', views.rsp_date, name='homee'),
    path('groupp', views.groupp, name='groupp'),
    path('teacherr', views.teacherr, name='teacherr')
]