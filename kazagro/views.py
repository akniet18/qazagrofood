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

    ovosh = ['Картофель урожай 2020 года', 'Лук', 'Свекла', 'Капуста', 'Баклажаны', 'Кабачки','Морковь', 'Огурцы "Миринда"', 'Болгарский перец "Светофор"',
    'Огурцы "Рава"', 'Помидоры', 'Жёлтая морковь', 'Помидоры "Розовые Юсуповские"','Помидоры "Черри" упаковка 500 гр', 'Болгарский перец зеленый',
    'Капуста цветная', 'Брокколи', 'Пекинская капуста']
    fruck = ['Апельсины "Балади"', 'Яблоки "Салтанат"', 'Яблоки "Симеренко"', 'Яблоки Ранетки', 'Груша "Форель"', 'Бананы "Кавендиш"']  

    data1 = []
    data2 = []
    soup = BeautifulSoup(r.text, 'lxml')
    a = soup.find_all("tr")
    for i in range(3, len(a)):
        b = a[i].find_all('td')
        if razdel == "roznica":
            for i in ovosh:
                if i == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[3].get_text(), 'count': 0})
            for i in fruck:
                if i == b[1].get_text() and b[2].get_text() == "Фрукты":
                    data2.append({'name': b[1].get_text(), 'price': b[3].get_text(), 'count': 0})
        elif razdel == "optom":
            for i in ovosh:
                if i == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[5].get_text(), 'count': 0})
            for i in fruck:
                if i == b[1].get_text() and b[2].get_text() == "Фрукты":
                    data2.append({'name': b[1].get_text(), 'price': b[5].get_text(), 'count': 0})
        else:
            for i in ovosh:
                if i == b[1].get_text() and b[2].get_text() == "Овощи":
                    data1.append({'name': b[1].get_text(), 'price': b[10].get_text(), 'count': 0})
            for i in fruck:
                if i == b[1].get_text() and b[2].get_text() == "Фрукты":
                    data2.append({'name': b[1].get_text(), 'price': b[10].get_text(), 'count': 0})
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
    data = []
    return {
        'data1': data1,
        'data2': data2
    }


def base(request):
    return render(request, 'base.html', {'data1': ""})


def index(request, razdel):
    # print(razdel, "index")
    a = main(razdel)
    return render(request, 'index.html', {'data1': a['data1'], 'data2': a['data2'], 'razdel': json.dumps(razdel)})


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
        # nn = ["Картофель очищенный ( 0,5 кг )", "Лук очищенный ( 0,5 кг )","Морковь очищенная ( 0,5 кг )","Картофель очищенный (опт. 5кг упаковки)",
        # "Лук очищенный (опт. 5кг упаковки)","Морковь очищенная (опт. 5кг упаковки)","Картофель белый","Картофель красный",
        # "Картофель урожай 2020 года","Лук","Морковь","Свекла","Капуста","Редька","Жёлтая морковь","Болгарский перец зеленый",
        # 'Болгарский перец "Светофор"',"Помидоры",'Помидоры "Розовые Юсуповские"','Помидоры "Черри" упаковка 500 гр',
        # 'Огурцы "Миринда"','Огурцы "Рава"',"Баклажаны","Кабачки","Брокколи",'Тыква "Груша"',
        # "Капуста цветная","Пекинская капуста",'Яблоки "Granny Smith"',"Яблоки Ранетки",'Яблоки "Симеренко"','Яблоки "Голден"',
        # 'Яблоки "Айдаред"','Яблоки "Превосход"',	'Яблоки "Салтанат"', 'Груша "Конференция"', 	'Груша "Форель"','Мандарины "kinnow"',
        # 'Мандарины "murcoot"','Апельсины "Балади"','Бананы "Кавендиш"','Персик "Никтарин"','Лимон "Кутдикен"','Киви "Bruno"','Абрикос',
        # 'Гранат "Wonderfull"','Ананас "Mini Queen"','Арбуз','Арбуз Иран','Слива','Виноград "Бычий глаз"','Виноград','Манго "Kent"',
        # 'Авокадо "Fuerte"',"клубника 'Driscoll's' 400гр",'Клубника (упаковка 500 гр.)','Черешня ( упаковка 500 гр. )','Имбирь',
        # 'Чеснок "Априор"','Редис (упаковка 500 гр)','Укроп (упаковка 50 гр)','Петрушка (упаковка 50 гр)','Лук зеленый (пучок)',
        # 'Кинза (упаковка 50 гр)','Листья салата (пучок)','Шпинат (упаковка 50 гр)','Щавель (упаковка 50 гр)','Руколла (упаковка 50 гр)',
        # 'Жусай (упаковка 50 гр)','Мята (упаковка 50 гр)','Сельдерей (упаковка 50 гр)','Айсберг',"Грибы Шампиньоны",'Яблоки для Компота',
        # 'кр. Смородина "coloured" 125гр']


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

