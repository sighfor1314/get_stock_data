from get_all_stock_number import GetStockNumber
import requests
import json
from datetime import datetime
import time
'''
    goal : generate daily stock infomation to json file
'''
class GetStockInfo:
    def __init__(self,stock_number):
        self.stock_number=stock_number
        self.date = datetime.now().strftime('%Y%m%d')
        self.result = {
            "stat":None,
            'date': None,
            'title': None,
            "fields": ["有價證券代號", "有價證券名稱","產業別", "成交股數", "成交金額", "開盤價", "最高價", "最低價", "收盤價", "漲跌價差", "成交筆數"],
            "data": [],
            'notes':None
        }
        # self.proxies_list=['66.196.238.181:3128','160.3.168.70:8080','140.227.65.59:3180']

    def get_stock_data(self,index=0):

        # self.df=['1101','1102','1103']
        new_proxy = self.proxies_list.pop()
        # print(new_proxy)
        proxies = {"http": '133.125.54.107:80'}
        for i in self.stock_number.keys():
            try:
                print(i)
                response = requests.get('https://www.twse.com.tw/exchangeReport/STOCK_DAY?'+
                                        'date='+self.date+\
                                        '&stockNo='+i
                                        ,proxies=proxies
                                        )
                time.sleep(3)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            data  = json.loads(response.text)
            length=len(data['data'])
            self.result['data'].append( {i:data['data'][length-1]})

    '''
            from twse STOCK_DAY_ALL api get today's all stock info
    '''
    def get_stock_all_data(self):

        headers = {'user-agent': 'Mozilla/5.0'}
        try:  # Check requests url is succeeded
            response = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json',headers=headers)

        except requests.exceptions.RequestException as e:
                raise SystemExit(e)

        data = json.loads(response.text)  # load twse response json file
        self.result['stat'] = data['stat']
        self.result['date'] = data['date']
        self.result['title'] = data['title']
        for i in range(len(data['data'])):

            if data['data'][i][0] in self.stock_number.keys():  # if stock_number in data ,appending to result
                self.result['data'].append( data['data'][i])

        self.result['notes'] = data['notes']
        file = open('listed.json', "w",encoding="utf-8")
        json.dump(self.result, file,ensure_ascii=False)
        # return data

