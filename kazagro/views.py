from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime
from xlsxwriter.utility import xl_col_to_name
import requests

import os.path
import os
import gspread
from bs4 import BeautifulSoup


SAMPLE_SPREADSHEET_ID = '10W1gWd0Ftzb6iXuW1o9b1U4kLo_bpB9Em6V6oiSOweo'
# SAMPLE_RANGE_NAME = 'Sheet1!A1:Ac'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gc = gspread.service_account(filename=os.path.join(BASE_DIR, 'kazagrofood-dfd69b4ebbfd.json'))
sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
def next_available_row(worksheet):
    str_list = len(list(filter(None, worksheet.col_values(1)))) + 1
    str_list2 = len(list(filter(None, worksheet.col_values(2)))) + 1
    if str_list > str_list2:
        return str_list
    else:
        return str_list2

def main():
    worksheet = sh.get_worksheet(1)

    values_name = worksheet.row_values(3)
    values_prices = worksheet.row_values(2)
    # r = requests.get('https://docs.google.com/spreadsheets/d/10W1gWd0Ftzb6iXuW1o9b1U4kLo_bpB9Em6V6oiSOweo/edit?usp=sharing')
    # soup = BeautifulSoup(r.text, 'html.parser')
    # body = soup.find("body")
    # a = soup.find_all("script")[24]
    data = []
    # a=str(a)
    # print(a.find("390822454"))
    # print(a[245199:])
    # print(next_available_row(worksheet)+3)

    # print(len(values_name)-1)
    for i in range(2, len(values_name)):
        if values_name[i] != "":
            data.append({'name': values_name[i], 'price': values_prices[i], 'count': 0})
    return {
        'data': data,
    }


def index(request):
    a = main()
    return render(request, 'index.html', {'data': a['data'][:15]})


def addRow(request):
    if request.is_ajax and request.method == "POST":
        worksheet = sh.get_worksheet(1)
        # worksheet.resize(1)

        data = json.loads(request.POST.get('dada'))
        name = request.POST.get('name')
        address = request.POST.get('address')
        area = request.POST.get('area')
        phone = request.POST.get('phone')

        ind = next_available_row(worksheet) + 3
        dateTimeObj = datetime.now()
        ddd = dateTimeObj.strftime("%d.%M.%Y %H:%M:%S")
        print(ind, ddd)
        
        summ = 0
        res = [ind-4, ddd]
        for i in data:
            if i['count'] > 0:
                summ += int(i['price'].replace(" ", "")) * i['count']
                res.append(i['count'])
            else:
                res.append("")
        for i in range(79-len(data)):
            res.append("")
        res.append(summ)
        res.append(name)
        res.append(area)
        res.append(address)
        res.append(phone)
        print(summ)
        
        ranges = "A{}:CL{}".format(ind, ind)
        # print(worksheet.row_values(1))
        # print(ranges)

        # sh.values_append('оптовая!{}'.format(ind),{'valueInputOption': 'USER_ENTERED'}, {'values': res})
        # worksheet.append_row(res, table_range=ranges)

        worksheet.update(ranges, [res])
        return JsonResponse({"status": "ok"})

