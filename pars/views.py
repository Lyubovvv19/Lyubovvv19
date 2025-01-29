from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .forms import DocumentUploadForm, LoginUserForm
from .models import Raspisanie,UploadedFile
import json
from datetime import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import chardet
import logging
import logging.config
# def is_admin(user):
#     return user.is_superuser
# @user_passes_test(is_admin)
logger = logging.getLogger('main')
def login_pars(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('pars:pars'))
    else:
        form = LoginUserForm()
    return render(request, 'pars/login.html', {'form': form})

def logout_pars(request):
    logout(request)
    return HttpResponseRedirect(reverse('pars:login'))
def rez_pars(request):
    pass


@login_required
def pars(request):

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = request.FILES['document']
            file_content = document.read()  # Читаем содержимое файла в байтах
            result = chardet.detect(file_content)  # Определяем кодировку
            encoding = result['encoding']
            print('11111111111111111111111', encoding)
            uploaded_file = UploadedFile(file=document)
            uploaded_file.save()
            full_path = uploaded_file.file.path
            FName = full_path
            logger.info(f'[{datetime.today()}] загрузка файла {FName} началась')
            with open(FName, 'r') as file:
                data = json.load(file)

                # print('---------------------------------', data, type(data))
                cont = 0
                for record in data:

                    user = record["timetable"]
                    # print(user)
                    cont += 1
                    logger.info(f'[{datetime.today()}] загрузка {cont} недели № {user[0]['week_number']}')
                    print(f'[{datetime.today()}] загрузка {cont} недели № {user[0]['week_number']}')
                    Raspisaniee = []
                    g = []
                    for item in user:
                        for i_item in item['groups']:
                            # print(i_item)
                            d = i_item['group_name']
                            start = datetime.strptime((item['date_start']),'%d-%m-%Y')
                            finish = datetime.strptime((item['date_end']),'%d-%m-%Y')
                            g.append(d)
                            # Raspisanie.objects.filter(group_name=d, date__range=(start, finish)).delete()
                            for i in i_item['days']:

                                if 'lessons' in i:
                                    for j in i['lessons']:
                                        if j['subject'] == '.':
                                            continue
                                        for k in j['teachers']:
                                            for l in j['auditories']:

                                                # Raspisaniee.save()

                                                Raspisaniee.append(Raspisanie(group_name=(str(i_item['group_name'])), weekday=(str(i['weekday'])), subject=str(j['subject']), type_subject=str(j['type']), subgroup=(int(j['subgroup'])), time=str(j['time_start']+'-'+j['time_end']), date=datetime.strptime((j['date']),'%d-%m-%Y'),teacher_name=str(k['teacher_name']), auditory_name=str(l['auditory_name'])))
                    start2 = datetime.strptime((user[0]['date_start']), '%d-%m-%Y')
                    finish2 = datetime.strptime((user[0]['date_end']), '%d-%m-%Y')
                    # print(start2, finish2)
                    # # print(set(g))
                    Raspisanie.objects.filter(group_name__in=(set(g)), date__range=(start2, finish2)).delete()
                    Raspisanie.objects.bulk_create(Raspisaniee)
                    # rez1 = Raspisanie.objects.filter(group_name__in=(set(g)), date__range=(start2, finish2))
                    # rez2 = Raspisaniee
                    # print('11111111', rez1.count(), '1111111111')
                    # print('2222222222', len(rez2), '2222222222222')
                    # # print(g)




            # print('================================================')
            # print('+++++++++++++++++++++++++++++++++++++++++++++++')
            #
            # print(len(data))
            logger.info(('Загрузка прошла успешно'))
            return render(request, 'pars/rez.html', {'file_name': document.name})
    else:
        form = DocumentUploadForm()
    return render(request, 'pars/ind.html', {'form': form})


