from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import datetime

import os.path
import os
import gspread


SAMPLE_SPREADSHEET_ID = '10W1gWd0Ftzb6iXuW1o9b1U4kLo_bpB9Em6V6oiSOweo'
# SAMPLE_RANGE_NAME = 'Sheet1!A1:Ac'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gc = gspread.service_account(filename=os.path.join(BASE_DIR, 'kazagrofood-dfd69b4ebbfd.json'))

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+1

def main():

    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)

    worksheet = sh.get_worksheet(1)
    # worksheet.append_row(['asfasf', "asfasf"], table_range='1:6')
    # ind = next_available_row(worksheet)
    # print(worksheet.find('статус').col)
    # worksheet.update_acell("A{}".format(ind), ["mmmmmmyyy", "asdasdasdewdsdvewvere"])

    values_name = worksheet.row_values(3)
    values_prices = worksheet.row_values(2)
    # print(values_name)
    data = []
    print(len(values_name)-1)
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
        sh = gc.open_by_key("10W1gWd0Ftzb6iXuW1o9b1U4kLo_bpB9Em6V6oiSOweo")
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

