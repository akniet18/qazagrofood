from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import os.path
import os
import gspread


SAMPLE_SPREADSHEET_ID = '10W1gWd0Ftzb6iXuW1o9b1U4kLo_bpB9Em6V6oiSOweo'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gc = gspread.service_account(filename=os.path.join(BASE_DIR, 'kazagrofood-dfd69b4ebbfd.json'))
sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)

def next_available_row(worksheet):
    a = worksheet.col_values(1)
    b = worksheet.col_values(2)
    # print(len(a), len(b))
    # str_list = []
    # for i in a:
    #     str_list.append()
    # str_list = len(list(filter(None, worksheet.col_values(1)))) + 1
    # str_list2 = len(list(filter(None, worksheet.col_values(2)))) + 1
    # print(worksheet.col_values(2))
    if len(a) > len(b):
        return len(a)
    else:
        return len(b)

def main(razdel):
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNX6FcoIutGWY6VolvaL6GbCcRwj__YImi2EFAFEcLW4NL-pc9YAil8oxaB5-uaZfGgKIV5rMEPc8h/pubhtml?gid=62247483&single=true"
    r = requests.get(url)
    # worksheet = sh.get_worksheet(1)
    # values_name = worksheet.row_values(3)
    # values_prices = worksheet.row_values(2)
    # ovosh_img = ["Картофель урожай 2020 года.jpg", "Лук.jpg", "svekla.jpg", "kapusta.jpg", "Баклажаны.jpg", "kabachki.jpg", "Морковь.jpg", "Огурцы1.jpg", "Светофор.jpg",
    #     "Рава.jpg", "potato.jpg", "yellowmorkov.jpg", "rozpotato.jpg", "cherri.jpg", "backlo.jpg",
    #     "kapustacv.jpg", "Брокколи.jpg", "kapusta.jpg"
    # ]
    # fruck_img = ["apelsin.jpg", "apple3.jpg", "apple2.jpg", "apple1.jpg", "grusha.jpg", "banan.jpg"]

    ovosh = ['Картофель урожай 2020 года', 'Лук', 'Морковь', 
            'Свекла', 'Капуста', 'Жёлтая морковь',
            'Баклажаны',  'Кабачки', 'Болгарский перец "Светофор"',
            'Помидоры "Розовые Юсуповские"', 'Помидоры "Черри" упаковка 500 гр', 'Помидоры',
            'Болгарский перец зеленый', 'Огурцы "Миринда"', 'Огурцы "Рава"',
            'Брокколи', 'Пекинская капуста', 'Капуста цветная']
    # fruck = ['Апельсины "Балади"', 'Яблоки "Салтанат"', 'Яблоки "Симеренко"', 'Яблоки Ранетки', 'Груша "Форель"', 'Бананы "Кавендиш"']  
    fruck = ['Лимон "Кутдикен"','Яблоки  "Granny Smith" ', 'Персик "Никтарин"',
             'Яблоки "Превосход"', 'Абрикос', 'Мандарины "murcoot" ',
             'Бананы "Кавендиш"',  'Дыня Торпедо',  "Арбуз "]

    zelen = ['Укроп (упаковка 50 гр)', 'Щавель (упаковка 50 гр)', 'Руколла (упаковка 50 гр)', 
             'Сельдерей (упаковка 50 гр)', 'Кинза (упаковка 50 гр)', 'Петрушка (упаковка 50 гр)',
             'Жусай (упаковка 50 гр)', 'Мята (упаковка 50 гр)', 'Листья салата (пучок)']

    data1 = []
    data2 = []
    data3 = []
    soup = BeautifulSoup(r.text, 'lxml')
    a = soup.find_all("tr")

    for i in range(len(ovosh)):
        for k in range(3, len(a)):
            b = a[k].find_all('td')
            if razdel == "roznica":
                if ovosh[i] == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[3].get_text(), 'count': 0})
            elif razdel == "optom":
                if ovosh[i] == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[5].get_text(), 'count': 0})
            else:
                if ovosh[i] == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[10].get_text(), 'count': 0})
    for i in range(len(fruck)):
        for k in range(3, len(a)):
            b = a[k].find_all('td')
            if razdel == "roznica":
                if fruck[i] == b[1].get_text() and (b[2].get_text() == "Фрукты" or b[2].get_text() == "Экзотика" or b[2].get_text() == "фрукты"):
                    data2.append({'name': b[1].get_text(), 'price': b[3].get_text(), 'count': 0})
            elif razdel == "optom":
                if fruck[i] == b[1].get_text() and (b[2].get_text() == "Фрукты" or b[2].get_text() == "Экзотика" or b[2].get_text() == "фрукты"):
                    data2.append({'name': b[1].get_text(), 'price': b[5].get_text(), 'count': 0})
            else:
                if fruck[i] == b[1].get_text() and (b[2].get_text() == "Фрукты" or b[2].get_text() == "Экзотика" or b[2].get_text() == "фрукты"):
                    data2.append({'name': b[1].get_text(), 'price': b[10].get_text(), 'count': 0})
    for i in range(len(zelen)):
        for k in range(3, len(a)):
            b = a[k].find_all('td')
            if razdel == "roznica":
                if zelen[i] == b[1].get_text() and b[2].get_text() == "Зелень":
                    data3.append({'name': b[1].get_text(), 'price': b[3].get_text(), 'count': 0})
            elif razdel == "optom":
                if zelen[i] == b[1].get_text() and b[2].get_text() == "Зелень":
                    data3.append({'name': b[1].get_text(), 'price': b[5].get_text(), 'count': 0})
            else:
                if zelen[i] == b[1].get_text() and b[2].get_text() == "Зелень":
                    data3.append({'name': b[1].get_text(), 'price': b[10].get_text(), 'count': 0})

    return {
        'data1': data1,
        'data2': data2,
        'data3': data3
    }


def base(request):
    return render(request, 'base.html', {'data1': ""})


def index(request, razdel):
    a = main(razdel)
    return render(request, 'index.html', {'data1': a['data1'], 'data2': a['data2'],'data3': a['data3'], 'razdel': json.dumps(razdel)})


def addRow(request):
    if request.is_ajax and request.method == "POST":
        razdel = request.POST.get('razdel')
        if razdel == "optom":
            worksheet = sh.get_worksheet(1)
        elif razdel == "roznica":
            worksheet = sh.get_worksheet(0)
        else:
            worksheet = sh.get_worksheet(2)

        data1 = json.loads(request.POST.get('data1'))
        data2 = json.loads(request.POST.get('data2'))
        data3 = json.loads(request.POST.get('data3'))
        summ = request.POST.get('summ')
        name = request.POST.get('name')
        address = request.POST.get('address')
        area = request.POST.get('area')
        phone = request.POST.get('phone')

        ind = next_available_row(worksheet) + 1
        dateTimeObj = datetime.now()

        
        ii = worksheet.find("Сумма Заказа")
        # print(ii)
        res=[]
        for i in range(ii.col-1):
            res.append("")
        ddd = dateTimeObj.strftime("%d.%M.%Y %H:%M:%S")
        # print(ind, ddd)
        
        # res[0] = ind-4
        res[1] = ddd
        # indx = [11, 12, 13, 14, 15, 23, 25, 26, 19, 21, 22, 20, 18, 24, 17, 27, 29, 30, 45, 31, 44, 36, 47, 40, 43, 58, 51]
        indx =   [11, 12, 13, 14, 15, 24, 26, 27, 20, 22, 23, 21, 19, 25, 18, 28, 30, 31, 48, 32, 47, 37, 50, 44, 46, 60, 61, 70, 75, 76, 80, 72, 70, 78, 79, 73]
        indx2 = []
        # for i in data1:
        #     ii = worksheet.find(i['name'])
        #     indx2.append(ii.col)
        #     # res[ii.col] = i['count']
        # for i in data2:
        #     ii = worksheet.find(i['name'])
        #     # print(i)
        #     indx2.append(ii.col)
        # for i in data3:
        #     ii = worksheet.find(i['name'])
        #     # print(i)
        #     indx2.append(ii.col)
        #     # res[ii.col] = i['count']
        # print(len(indx2), indx2)
        # indx = indx2
        for i in range(len(indx)-18):
            # print(indx[i])
            if data1[i]['count'] != 0:
                res[indx[i]-1] = data1[i]['count']

        for i in range(9):
            if data2[i]['count'] != 0:
                res[indx[18+i]-1] = data2[i]['count']

        for i in range(9):
            if data3[i]['count'] != 0:
                res[indx[27+i]-1] = data3[i]['count']


        res.append(summ)
        res.append(name)
        if razdel == "optom":
            res.append("")
        # res.append(area)
        res.append(address)
        res.append(phone)
        # print(summ)
        # print(res)
        
        ranges = "A{}:DB{}".format(ind, ind)
        worksheet.update(ranges, [res])
        return JsonResponse({"status": "ok"})

