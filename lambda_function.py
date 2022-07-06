from get_all_stock_number import GetStockNumber
from stock_info import GetStockInfo
from top3_industry import GetTop3Industry
import json

def lambda_handler(event, context):
    # TODO implement
    task = GetStockNumber()
    stock_dic = task.get_number()

    task = GetStockInfo(stock_dic)
    result_dic,industry = task.get_stock_all_data()
    task = GetTop3Industry(result_dic,industry)
    task.convert_to_pd ()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
