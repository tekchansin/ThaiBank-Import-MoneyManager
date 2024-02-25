from src.BankStatement import BankStatement
from src.MoneyManager import MoneyManager
from src.PDF import PDFExtract
import pandas 
import re
from dateutil import parser
import glob

class SCB(BankStatement):
    
    def __init__(self, *args, **kwargs):
        super(SCB, self).__init__(*args, **kwargs)
    
    def extract_data(self, df_list):
        dataframe_list = []
        # print(df_list)
        # return
        for table in df_list:
            df = pandas.DataFrame(table)
            df.drop(['Balance/Baht', 'Channel'], axis=1, inplace=True)
            df.drop(index=[0,1], inplace=True)
            df.drop(df.tail(3).index, inplace=True)
            
            df.columns = ["Date", "Type",  "Amount", "Amount2", 'Description']
            df['Note'] = ''
            
            # Remove which can't parse data
            for row in df.itertuples():
                try:
                    parser.parse(row.Date)
                except:
                    df.drop(row.Index, inplace=True)
                    
            df['Date'] = pandas.to_datetime(df['Date'], format='%d/%m/%y %H:%M')
            
            df['Type'].replace('X1','Income', inplace=True)
            df['Type'].replace('X2','Expense', inplace=True)
            df['Type'].replace('IN','Income', inplace=True)
            
             ## Fix missing Amount in some case
            for row in df.itertuples():
                if type(row.Amount) != str:
                    df.at[row.Index, 'Amount'] = str(row.Amount2)
                        
            df['Amount'] =df['Amount'].str.replace(',', '').astype(float)     
            df.drop(['Amount2'], axis=1, inplace=True)
                        
            df = dataframe_list.append(df)
            
            
        table_list = pandas.concat(dataframe_list, ignore_index=True )  
        
        table_list = table_list[['Date','Type','Amount',  'Description', 'Note']]
        
        return table_list
    