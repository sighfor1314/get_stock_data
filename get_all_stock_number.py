import requests
import re
from bs4 import BeautifulSoup
'''
    goal : get all stock number and name to dictionary
'''
class  GetStockNumber:
    def get_number(self):
        stock_dic = {}

        try:
            response = requests.get('https://isin.twse.com.tw/isin/C_public.jsp?strMode=2')
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        soup = BeautifulSoup(response.text, "html.parser")
        stock_table = soup.find_all("tr")
        for i in stock_table:
            stock_info= i.find_all("td")
            is_number = re.match(r'^[0-9]', stock_info[0].text[0])
            if stock_info[0].text == " 上市認購(售)權證  ":
                break
            if stock_info[0].text[0] == ' ' or not is_number:
                continue

            stock_list=stock_info[0].text.split()
            stock_dic[stock_list[0]] = stock_info[4].text

        return stock_dic


