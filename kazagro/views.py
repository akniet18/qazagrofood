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
# SAMPLE_RANGE_NAME = 'Sheet1!A1:Ac'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gc = gspread.service_account(filename=os.path.join(BASE_DIR, 'kazagrofood-dfd69b4ebbfd.json'))
sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)\

def next_available_row(worksheet):
    a = worksheet.col_values(1)
    b = worksheet.col_values(2)
    print(len(a), len(b))
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
    ovosh_img = ["Картофель урожай 2020 года.jpg", "Лук.jpg", "svekla.jpg", "kapusta.jpg", "Баклажаны.jpg", "kabachki.jpg", "Морковь.jpg", "Огурцы1.jpg", "Светофор.jpg",
        "Рава.jpg", "potato.jpg", "yellowmorkov.jpg", "rozpotato.jpg", "cherri.jpg", "backlo.jpg",
        "kapustacv.jpg", "Брокколи.jpg", "kapusta.jpg"
    ]
    fruck_img = ["apelsin.jpg", "apple3.jpg", "apple2.jpg", "apple1.jpg", "grusha.jpg", "banan.jpg"]

    ovosh = ['Картофель урожай 2020 года', 'Лук', 'Свекла', 'Капуста', 'Баклажаны', 'Кабачки','Морковь', 'Огурцы "Миринда"', 'Болгарский перец "Светофор"',
    'Огурцы "Рава"', 'Помидоры', 'Жёлтая морковь', 'Помидоры "Розовые Юсуповские"','Помидоры "Черри" упаковка 500 гр', 'Болгарский перец зеленый',
    'Капуста цветная', 'Брокколи', 'Пекинская капуста']
    fruck = ['Апельсины "Балади"', 'Яблоки "Салтанат"', 'Яблоки "Симеренко"', 'Яблоки Ранетки', 'Груша "Форель"', 'Бананы "Кавендиш"']  

    data1 = []
    data2 = []
    data3 = []
    soup = BeautifulSoup(r.text, 'lxml')
    a = soup.find_all("tr")
    for i in range(3, len(a)):
        b = a[i].find_all('td')
        if razdel == "roznica":
            for i in range(len(ovosh)):
                if ovosh[i] == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[3].get_text(), 'count': 0, "img": ovosh_img[i]})
            for i in range(len(fruck)):
                if fruck[i] == b[1].get_text() and b[2].get_text() == "Фрукты":
                    data2.append({'name': b[1].get_text(), 'price': b[3].get_text(), 'count': 0, "img": fruck_img[i]})
        elif razdel == "optom":
            for i in range(len(ovosh)):
                if ovosh[i] == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[5].get_text(), 'count': 0, "img": ovosh_img[i]})
            for i in range(len(fruck)):
                if fruck[i] == b[1].get_text() and b[2].get_text() == "Фрукты":
                    data2.append({'name': b[1].get_text(), 'price': b[5].get_text(), 'count': 0, "img": fruck_img[i]})
        else:
            for i in range(len(ovosh)):
                if ovosh[i] == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[10].get_text(), 'count': 0, "img": ovosh_img[i]})
            for i in range(len(fruck)):
                if fruck[i] == b[1].get_text() and b[2].get_text() == "Фрукты":
                    data2.append({'name': b[1].get_text(), 'price': b[10].get_text(), 'count': 0, "img": fruck_img[i]})
    # print(len(data1), len(data2))
            
        # if b[2].get_text() != "":
        #     name = b[1].get_text()
        #     price = b[3].get_text()
        #     data.append({'name': name, 'price': price, 'count': 0})
            # print(name)
    # print(len(values_name)-1)
    # for i in range(2, len(values_name)):
    #     if values_name[i] != "":
    #         data.append({'name': values_name[i], 'price': values_prices[i], 'count': 0})
    data3 = data1 + data2
    return {
        'data1': data1,
        'data2': data2,
        'data3': data3
    }


def base(request):
    return render(request, 'base.html', {'data1': ""})


def index(request, razdel):
    # print(razdel, "index")
    a = main(razdel)
    return render(request, 'index.html', {'data1': a['data1'], 'data2': a['data2'], 'data3': a['data3'], 'razdel': json.dumps(razdel)})


def addRow(request):
    if request.is_ajax and request.method == "POST":
        razdel = request.POST.get('razdel')
        if razdel == "optom":
            worksheet = sh.get_worksheet(1)
        elif razdel == "roznica":
            worksheet = sh.get_worksheet(2)
        else:
            worksheet = sh.get_worksheet(0)

        data1 = json.loads(request.POST.get('data1'))
        data2 = json.loads(request.POST.get('data2'))
        summ = request.POST.get('summ')
        name = request.POST.get('name')
        address = request.POST.get('address')
        area = request.POST.get('area')
        phone = request.POST.get('phone')

        ind = next_available_row(worksheet) + 1
        dateTimeObj = datetime.now()
        res=[]
        for i in range(78):
            res.append("")
        ddd = dateTimeObj.strftime("%d.%M.%Y %H:%M:%S")
        print(ind, ddd)
        
        res[0] = ind-4
        res[1] = ddd
        indx = [11, 12, 13, 17, 14, 15, 20, 21, 22, 29, 30, 27, 23, 24, 25, 26, 18, 19, 32, 33, 37, 39, 43, 42]
        # for i in data1:
        #     ii = worksheet.find(i['name'].lower())
        #     indx.append(ii.col)
        #     # res[ii.col] = i['count']
        # for i in data2:
        #     ii = worksheet.find(i['name'].lower())
        #     # print(i)
        #     indx.append(ii.col)
        #     # res[ii.col] = i['count']
        # print(indx)
        for i in range(len(indx)-6):
            # print(indx[i])
            if data1[i]['count'] != 0:
                res[indx[i]-1] = data1[i]['count']

        for i in range(6):
            # print(indx[18+i])
            if data2[i]['count'] != 0:
                res[indx[18+i]-1] = data2[i]['count']


        res.append(summ)
        res.append(name)
        if razdel == "optom":
            res.append("")
        # res.append(area)
        res.append(address)
        res.append(phone)
        # print(summ)
        print(len(res))
        
        ranges = "A{}:CL{}".format(ind, ind)
        worksheet.update(ranges, [res])
        return JsonResponse({"status": "ok"})

