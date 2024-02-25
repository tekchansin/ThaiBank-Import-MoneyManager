from src.BankStatement import BankStatement
from src.MoneyManager import MoneyManager
from src.PDF import PDFExtract
import pandas 
import re
from dateutil import parser
import glob

class KBANK(BankStatement):
        
    def __init__(self, *args, **kwargs):
        super(KBANK, self).__init__(*args, **kwargs)
    
    def extract_data(self, df_list):
        dataframe_list = []
        # print(df_list)
        # return
        for table in df_list:
            df = pandas.DataFrame(table)
            row, col = df.shape
            print('Table: Row/Columns: ',row,'/',col)
            if col != 9:
                ## Unread main table
                continue
            
            df.drop(index=[0,1,2], inplace=True)
            
            df.columns = ["Date", "Time","Type","Tmp2", "Amount", "Balance","Channel","Channel2",'Description']
            df.drop(['Time','Tmp2',"Channel",'Channel2'], axis=1, inplace=True)
            df['Note'] = ''
            
            ## Multiline Description      
            for row in df.itertuples():
                if type(row.Date) == float and type(row.Description) == str:
                    first_desc = df.at[row.Index-1, 'Description']
                    new_desc = first_desc+' '+row.Description
                    df.at[row.Index-1, 'Description'] = new_desc
                    df.drop(row.Index, inplace=True)
                if row.Type == 'คาธรรมเนยม':
                    df.at[row.Index, 'Description'] = 'ค่าธรรมเนียม '+row.Description
                    
            # Remove which can't parse data
            for row in df.itertuples():
                try:
                    parser.parse(row.Date)
                except:
                    df.drop(row.Index, inplace=True)
                    
            df['Date'] = pandas.to_datetime(df['Date'], format='%d-%m-%y')
            
            
            df['Type'].replace('ฝากเงนสด','Income', inplace=True)
            df['Type'].replace('รบโอนเงน','Income', inplace=True)
            df['Type'].replace('รบโอนเงนอตโนมต','Income', inplace=True)
            df['Type'].replace('ชําระเงน','Expense', inplace=True)
            df['Type'].replace('โอนเงน','Expense', inplace=True)
            df['Type'].replace('หกบญช','Expense', inplace=True)
            df['Type'].replace('โอนเงน','Expense', inplace=True)
            df['Type'].replace('คาธรรมเนยม','Expense', inplace=True)
            df['Type'].replace('ถอนเงนสด','Expense', inplace=True)
             
            df['Amount'] =df['Amount'].str.replace(',', '').astype(float)     
                        
            dataframe_list.append(df)
            
        table_list = pandas.concat(dataframe_list, ignore_index=True )  
        
        table_list = table_list[['Date','Type','Amount',  'Description', 'Note']]
        
        return table_list
    