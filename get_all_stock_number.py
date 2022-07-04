import requests
import re
from bs4 import BeautifulSoup
'''
    goal : get all stock number and name to dictionary
'''
class  GetStockNumber:
    def get_number(self):
        stock_dic = {}

        try:  # Check requests url is succeeded
            response = requests.get('https://isin.twse.com.tw/isin/C_public.jsp?strMode=2')
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)

        soup = BeautifulSoup(response.text, "html.parser")  # Use BeautifulSoup get html data
        stock_table = soup.find_all("tr")  # find tag 'tr'

        for i in stock_table: # find tr -> td for getting all stock number and name
            stock_info= i.find_all("td")
            is_number = re.match(r'^[0-9]', stock_info[0].text[0])
            if stock_info[0].text == " 上市認購(售)權證  ":  # Stop to tr.text = 上市認購(售)權證
                break
            if stock_info[0].text[0] == ' ' or not is_number: #before tr.text = 上市認購(售)權證 only find stock_number
                continue

            stock_list=stock_info[0].text.split() # stock_number stock_name to stock_list[stock_number,stock_name]
            stock_dic[stock_list[0]] = stock_info[4].text # map  industry_type to dictionary {stock_number: industry_type}

        return stock_dic


