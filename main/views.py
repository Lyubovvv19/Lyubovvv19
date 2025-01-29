from django.shortcuts import render
import json
from .models import Raspisanie
from datetime import *
import pandas as pd
from django.db.models import Max

from django.db.models import Count
const_len = 65

def Pars():


    '''
    with open('media/Raspisaie_1.json', 'r') as file:
        data = json.load(file)
    group = []
    group_dict = {}
    groups = []
    teacher = []
    teacher_dict = {}
    teachers = []

    for record in data:
        user = record["timetable"]
        for item in user:
            for i_item in item['groups']:
                group.append(i_item['group_name'])
    for record in data:
        user = record["timetable"]
        for item in user:
            for i_item in item['groups']:
                for i in i_item['days']:
                    if 'lessons' in i:
                        for j in i['lessons']:
                            for k in j['teachers']:
                                teacher.append(k['teacher_name'])
    teacher = list(set(teacher))
    for i in sorted(group):
        group_dict = {'id': i, 'name': i}
        groups.append(group_dict)

    for i in sorted(teacher):
        teacher_dict = {'id': i, 'name': i}
        teachers.append(teacher_dict)
'''
    group = []
    teacher = []
    a = Raspisanie.objects.filter()
    for i in a:
        group.append(i.group_name)
        teacher.append(i.teacher_name)


    groups = []
    for i in sorted(set(group)):
        group_dict = {'id': i, 'name': i}
        groups.append(group_dict)

    teachers = []
    for i in sorted(set(teacher)):
        teacher_dict = {'id': i, 'name': i}
        teachers.append(teacher_dict)
    return groups, teachers


def index(request):
    groups, teachers = Pars()
        # print(group_dict)
    return render(request, 'main/index.html', {'groups': groups, 'teachers': teachers})
class Rasp:
    def __init__(self, data, day, tm, lst):
        data = pd.to_datetime(data).strftime("%d-%m-%Y")
        self.data = data
        self.day = day
        ls = []
        for i in range(len(lst)):
            ls.append((tm[i], lst[i]))
        self.para = ls

def str_obj(shedule, start, finish):
    sub = max_sub(shedule)
    # print(sub, type(sub))
    tims = ['09:00-10:35', '10:45-12:20', '12:40-14:15', '14:40-16:15', '16:25-18:00', '18:10-19:45']
    # print(int((finish-start).days))
    lst = [' '] * (int((finish-start+timedelta(days=1)).days)*(6+2))
    for sh in shedule:
        # print('================================', sh.date)
        if sh.subgroup == 0:
            lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time))+1)] = [sh.subject + "("+sh.type_subject+")-" + sh.teacher_name +" - " + sh.auditory_name]
        else:
            if len(lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time))+1)]) == 1:
                #Возможно sub+1
                sp = [' '] * sub
                # print(sp)
                sp[sh.subgroup-1] = sh.subject + "("+sh.type_subject+")-" + sh.teacher_name +" - " + sh.auditory_name
                lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time)) + 1)] = sp
                # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', lst)
            else:
                sp = lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time))+1)]
                sp[sh.subgroup-1] = sh.subject + "("+sh.type_subject+")-" + sh.teacher_name +" - " + sh.auditory_name
                lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time))+1)] = sp



    return lst
def str_obj2(shedule, start, finish):
    tims = ['09:00-10:35', '10:45-12:20', '12:40-14:15', '14:40-16:15', '16:25-18:00', '18:10-19:45']
    # было так [' '] * (int((finish-start).days)*6+2)
    lst = [' '] * (int((finish-start+timedelta(days=1)).days)*6+1)
    for sh in shedule:
        if len(lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time)) + 1)]) == 1:
            lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time))+1)] = sh.subject + "("+sh.type_subject+")-" + sh.auditory_name + '['+sh.group_name + "]"
        else:
            sp = lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time)) + 1)]
            sp += ',['+sh.group_name + "]"
            lst[int((sh.date - start).days) * 6 + ((tims.index(sh.time)) + 1)] = sp
    # print(lst)
    return lst


def max_sub(shedule):
    m_s = [0]
    for sh in shedule:
        m_s.append(int(sh.subgroup))
    return max(m_s)
def column_width(max_sub):
    if max_sub == 0:
        return 600
    else:
        return 600//max_sub

def group(request):
    if request.method == 'POST':
        max_date = Raspisanie.objects.aggregate(max_date=Max('date'))['max_date']
        n = date.today().weekday()
        start = date.today() - timedelta(days=n)
        print(start, type(start))
        # finish = start + timedelta(days= const_len)
        finish = max_date
        r = request.POST.get('group')
        #p = 'ФМ-ИД_Оb221'
        # print(r, type(r))
        wiks = ['ПН', "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        #shedule = Raspisanie.objects.filter(group_name=r, date__range=(start, finish)).order_by('date')
        shedule = list(Raspisanie.objects.filter(group_name=r, date__range=(start, finish)).order_by('date'))
        # print(shedule)


        # print(r, start, finish, shedule)
        # print(len(shedule))
        times = ['09:00-10:35', '10:45-12:20', '12:40-14:15', '14:40-16:15', '16:25-18:00', '18:10-19:45']
        dates = pd.date_range(start, finish).strftime('%Y-%m-%d').tolist()
        groups, teachers = Pars()

        lst_str = str_obj(shedule, start, finish)
        lst = []
        k = 1
        for d in dates:
            m = Rasp(d, wiks[date.fromisoformat(d).weekday()], times, lst_str[k:k+6])
            k += 6
            lst.append(m)
        # print(lst)
        group_count = max(1, max_sub(shedule))
        # print(group_count)
        width = column_width(max_sub(shedule))







        # current_data = start
        # while current_data <= finish:
        #    for i in range(1, 7):  # 6 строк для пар
        #         lesson = (shedual.filter(date=current_data))
        #         if lesson.exists():
        #             day_schedule['lessons'].append(lesson)
        #         else:
        #             day_schedule['lessons'].append(None)
        #    shedual_data.append(day_schedule)
        #    current_data += timedelta(days=1)
        # print(Raspisanie.objects.filter(group_name=p, date__range=(start, finish)))
        # print(shedual_data)
        # print(Raspisanie.objects.filter(date__range=(start, finish)))
        return render(request, 'main/group.html', {'shedule': shedule, 'start': start, 'finish': finish, 'wiks': wiks, 'lst': lst, 'groups': groups, 'group_count': group_count, 'teachers': teachers, 'width': width})
    else:
        groups, teachers = Pars()
        # print(group_dict)
        return render(request, 'main/index.html', {'groups': groups, 'teachers': teachers})


def teacher(request):


    if request.method == 'POST':
        max_date = Raspisanie.objects.aggregate(max_date=Max('date'))['max_date']
        n = date.today().weekday()
        start = date.today() - timedelta(days=n)
        Message_me = Raspisanie.objects.filter().count()
        print(Message_me)
        # finish = start + timedelta(days= const_len)


        finish = max_date
        r = request.POST.get('teacher')
        # print(r, type(r))
        wiks = ['ПН', "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
        shedule = list(Raspisanie.objects.filter(teacher_name=r, date__range=(start, finish)).order_by('date'))
        # print(r, start, finish, shedule)
        # print(len(shedule))
        times = ['09:00-10:35', '10:45-12:20', '12:40-14:15', '14:40-16:15', '16:25-18:00', '18:10-19:45']
        dates = pd.date_range(start, finish).strftime('%Y-%m-%d').tolist()
        groups, teachers = Pars()
        lst_str = str_obj2(shedule, start, finish)
        lst = []
        k = 1
        for d in dates:
            m = Rasp(d, wiks[date.fromisoformat(d).weekday()], times, lst_str[k:k + 6])
            k += 6
            lst.append(m)
        # print(lst)


        return render(request, 'main/teacher.html',
                  {'shedule': shedule, 'start': start, 'finish': finish, 'wiks': wiks, 'lst': lst, 'groups': groups, 'teachers': teachers})

    else:
        return render(request, 'main/teacher.html')
