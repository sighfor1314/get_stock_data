import json
import pandas as pd
import datetime


class GetTop3Industry:
    def __init__(self,stock_info,industry):
        self.stock_info=stock_info
        self.industry= industry

    '''
            get yesterday 'yyyymmdd'
    '''
    def get_last_day(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday.strftime('%Y%m%d')

    '''
        calculate each  IndustryType top3 ChangeRate  and output json
    '''
    def get_industry_top3(self, df):
        top3= df.sort_values(['IndustryType', 'ChangeRate'], ascending=False).groupby('IndustryType').head(3)
        for i in self.industry:
            filter = top3['IndustryType'] == i
            output= top3[filter]
            with open(i+'_top3.json', 'w', encoding='utf-8') as file:
                output.to_json(file,orient='records', force_ascii=False)

    '''
         calculate ChangeRate  from today stock informatiom  and convert to  dataframe
    '''
    def convert_to_pd(self):
        last_day= self.get_last_day() # get yesterday

        with open(last_day+'_listed.json') as f: # from last_day json get closing price
            data = json.load(f)
        closing_price_list=[]
        for i in range(len(data['data'])):
            closing_price_list.append([data['data'][i][0],data['data'][i][8]])

        # get today stock_info
        stock_info = pd.DataFrame(list(self.stock_info['data']), \
                                  columns= ["Code","Name","IndustryType" , "TradeVolume", "TradeValue","OpeningPrice","HighestPrice","LowestPrice","ClosingPrice", "Change", "Transaction"])

        last_close_price_df = pd.DataFrame(list(closing_price_list), columns= ["Code","LastClosingPrice"])
        result = pd.merge(stock_info,last_close_price_df)  # add LastClosingPrice to dataframe


        result['ClosingPrice'] = ( result['ClosingPrice'].str.split()).apply(lambda x: float(x[0].replace(',', '')))
        result[ 'LastClosingPrice'] = ( result[ 'LastClosingPrice'].str.split()).apply(lambda x: float(x[0].replace(',', '')))

        change_rate_list=[] # from last_day get closing price
        for i in range( result.shape[0]):

            closing_price = result['ClosingPrice'][i]  #  get today closing price
            last_closing_price = result['LastClosingPrice'][i] #  get last_day closing price

            if  last_closing_price == 0: # if last closing price == 0 , change_rate asign to None
                change_rate_list.append([data['data'][i][0],None])
            else:
                change_rate_list.append([data['data'][i][0],((closing_price - last_closing_price ) / last_closing_price )*100])

        change_rate = pd.DataFrame(list(change_rate_list), columns=["Code", "ChangeRate"])
        result = pd.merge(result, change_rate) # merge ChangeRate to result
        self.get_industry_top3(result)


