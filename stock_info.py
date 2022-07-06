from get_all_stock_number import GetStockNumber
import requests
import json
import datetime
import time
import random
'''
    goal : generate daily stock infomation to json file
'''
class GetStockInfo:
    def __init__(self,stock_number):
        self.stock_number=stock_number
        self.date = datetime.datetime.now().strftime('%Y%m%d')
        self.result = {
            "stat":None,
            'date': None,
            'title': None,
            "fields": ["有價證券代號", "有價證券名稱","產業別", "成交股數", "成交金額", "開盤價", "最高價", "最低價", "收盤價", "漲跌價差", "成交筆數"],
            "data": [],
            'notes':None
        }
        self.proxies_list=['xxxxxx','xxxxx','xxxx']  # initial proxies list

    '''
               from twse STOCK_DAY api get each stock info
    '''
    def get_stock_data(self,index=0):

        stock_list=[]
        for i in  self.stock_number.keys():
            stock_list.append(i)


        for i in range(index, len(stock_list)):
            new_proxy = random.choice(self.proxies_list) # random pick proxy
            proxies = {"http": new_proxy}
            try:

                response = requests.get('https://www.twse.com.tw/exchangeReport/STOCK_DAY?'+
                                        'date='+self.date+\
                                        '&stockNo='+stock_list[i]
                                        ,proxies=proxies
                                        )
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                self.get_stock_data(i)
                raise SystemExit(e)
            data  = json.loads(response.text)
            length=len(data['data'])
            self.result['data'].append( [stock_list[i]]+data['data'][length-2])

        file = open(data['date']+'_listed.json', "w",encoding="utf-8")  # output json file
        json.dump(self.result, file, ensure_ascii=False)

    '''
            from twse STOCK_DAY_ALL api get today's all stock info
    '''
    def get_stock_all_data(self):
        # proxies = {"http": '211.43.214.205:80'}
        headers = {'user-agent': 'Mozilla/5.0'}
        try:  # Check requests url is succeeded
            response = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=json',headers=headers)

        except requests.exceptions.RequestException as e:
                raise SystemExit(e)

        data = json.loads(response.text)  # load twse response json file
        self.result['stat'] = data['stat'] # add stat info
        self.result['date'] = data['date'] # add date info
        self.result['title'] = data['title'] # add title  info
        industry = tuple(set (self.stock_number.values())) # get all industry to tuple

        for i in range(len(data['data'])):

            if data['data'][i][0] in self.stock_number.keys():  # if stock_number in data ,appending to result
                data['data'][i].insert(2, self.stock_number[data['data'][i][0]])
                self.result['data'].append( data['data'][i])

        self.result['notes'] = data['notes'] # add notes info
        file = open(data['date']+'_listed.json', "w",encoding="utf-8")  # output json file
        json.dump(self.result, file,ensure_ascii=False)

        return self.result,industry

