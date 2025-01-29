from django.shortcuts import render
from django.shortcuts import render
import json
from .models import Raspisanie
from datetime import *
import pandas as pd

def Pars():
    auditoryy = []
    auditorys = []
    a = Raspisanie.objects.filter()
    for i in a:
        auditoryy.append(i.auditory_name)

    for i in sorted(set(auditoryy)):
        auditorys_dict = {'id': i, 'name': i}
        auditorys.append(auditorys_dict)

    return auditorys
class Rasp:
    def __init__(self, tm, lst1, lst2):
        ls = []
        for i in range(len(lst1)):
            lobj=[]
            for j in range(len(lst1[i])):
                lobj.append((lst1[i][j],lst2[i][j]))
            ls.append((tm[i], lobj))

        self.para = ls
def str_obj(shedule, auditorya, datee):
    tims = ['09:00-10:35', '10:45-12:20', '12:40-14:15', '14:40-16:15', '16:25-18:00', '18:10-19:45']


    # было так [' '] * (int((finish-start).days)*6+2)
    lst1 = []
    for i in range(len(tims)):
        lst1.append(['-']*len(auditorya))
    lst2 = []
    for i in range(len(tims)):
        lst2.append(['Свободна!']*len(auditorya))
    for sh in shedule:
        lst2[(tims.index(sh.time))][(auditorya.index(sh.auditory_name))] = sh.group_name + ' ' + sh.subject + "(" + sh.type_subject + ")-" + sh.teacher_name
        lst1[(tims.index(sh.time))][(auditorya.index(sh.auditory_name))] = '+'
    # c = 0
    # if len(auditorya) == 1:
    #     for sh in shedule:
    #         lst2[(tims.index(sh.time))] = sh.group_name + '' + sh.subject + "(" + sh.type_subject + ")-" + sh.teacher_name
    #     for i, l in enumerate(lst2):
    #         if l == ' ':
    #             lst2[i] = 'Свободна!'
    #             lst1[i] = '-'
    #         else:
    #             lst1[i] = '+'

            # for t in tims:
            #     print('ttttttttttttt', t)
            #     print('sssssshhhhhhhhhhhhhhhhhhhhh', sh.time)
            #     print(tims.index(sh.time))
            #     c += 1
                # lst1[(tims.index(sh.time))] = '+'
                # print('lalalalla')

            # else:
            #     lst1[(tims.index(sh.time))] = '-'
            #     lst2[(tims.index(sh.time))] = 'Свободна!'




            # if sh.time == t:
            #     lst1.append('+')
            #     lst2.append(sh.group_name + '' + sh.subject + "(" + sh.type_subject + ")-" + sh.teacher_name)
            # else:
            #     lst1.append('-')
            #     lst2.append('Свободна!')





    #
    # for t in tims:
    #     for audit in auditorya:
    #         for sh in shedule:
    #             if sh.time == t and sh.auditory_name == audit:
    #                 lst1.append('+')
    #             else:
    #                 lst1.append('-')
    # print(lst1)

        # print(lst)


    return lst1, lst2
def max_sub(auditorya):
    return len(auditorya)
def column_width(max_sub):
    if max_sub == 0:
        return 1000
    else:
        return 1000//max_sub
def aud(request):
    if request.method == 'POST':
        r = request.POST.get('a')
    a = Pars()
    return render(request, 'auditory/aud.html', {'a': a})

def aa(request):
    a = Pars()
    if request.method == 'POST':
        auditorya = request.POST.getlist('auditorya')
        datee = request.POST.get('calendar')
        shedule = list(Raspisanie.objects.filter(auditory_name__in=auditorya, date=(datee)).order_by('time'))
        times = ['09:00-10:35', '10:45-12:20', '12:40-14:15', '14:40-16:15', '16:25-18:00', '18:10-19:45']
        lst1, lst2 = str_obj(shedule, auditorya, datee)
        m = Rasp(times, lst1, lst2)
        lst = []
        lst.append(m)
        minus = '-'
        plus = '+'
        width = column_width(max_sub(auditorya))

        # print(a)
        return render(request, 'auditory/aa.html', {'a': a, 'auditorya': auditorya, 'lst': lst, 'minus': minus, 'plus': plus,'width': width})
    else:
        return render(request, 'auditory/aa.html', {'a': a})

# Create your views here.
