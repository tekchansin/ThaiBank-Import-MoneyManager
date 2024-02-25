from src.BankStatement import BankStatement
import pandas 
import re
from dateutil import parser

class TTBCredit(BankStatement):
   
    def __init__(self, *args, **kwargs):
        super(TTBCredit, self).__init__(*args, **kwargs)
    
    def extract_data(self, df_list):
        dataframe_list = []
        for table in df_list:
            df = pandas.DataFrame(table)
            df.columns = ["Date", "Date2",  "Description", 'Amount']
            df.drop(['Date2'], axis=1, inplace=True)
            # print(df)
            df['Note'] = ''
            df['Date'] = pandas.to_datetime(df['Date'], format='%d %b %y')
            df['Description'] =df['Description'].str.replace('\r', ' ')
            df['Amount'] =df['Amount'].str.replace(',', '')
            df['Amount'] =df['Amount'].str.replace(' THB', '').astype(float)
            df['Type'] = ''
            
            df = df.convert_dtypes()
            
            df = dataframe_list.append(df)
            
        table_list = pandas.concat(dataframe_list, ignore_index=True )
                
        ## Calculate Expense/Income        
        for row in table_list.itertuples():
            if row.Amount > 0:
                table_list.at[row.Index, 'Type'] = 'Expense'
            elif re.search('Payment', row.Description, re.IGNORECASE):
                #force drop
                table_list.drop(row.Index, inplace=True)
            else:
                table_list.drop(row.Index, inplace=True)
        
        table_list = self.remove_original_installment(table_list,'Reversal to Installment')
        table_list = self.remove_non_first_installment(table_list)
        next_ins_data = self.generate_installment(table_list)
        table_list = pandas.concat([table_list, pandas.DataFrame(next_ins_data)], ignore_index=True)
        
        # print(table_list)
        table_list = table_list[['Date','Type','Amount', 'Description', 'Note']]
        
        return table_list