from src.MoneyManager import MoneyManager
from src.PDF import PDFExtract
import pandas 
import warnings
import re
from dateutil import parser
import math 
import glob

warnings.simplefilter(action='ignore', category=FutureWarning)

class BankStatement:
    
    def __init__(self, inputpath, outputpath, account, pdfpass, trim_start_date=None):
        self.inputpath = inputpath
        self.outputpath = outputpath
        self.account = account
        self.pdfpass = pdfpass
        self.trim_start_date = trim_start_date
        
    def exec(self):
        print('Scanning: '+self.__class__.__name__)
        files = glob.glob(self.inputpath)
        for file in files:
            df_list = PDFExtract.read_pdf(file,self.pdfpass)
            data = self.extract_data(df_list)
            
            data = self.trim_date_after(data)
            print(data)
            data = MoneyManager.etl(data, self.account)
            
            MoneyManager.save_csv(data, self.outputpath, self.account)    

    def trim_date_after(self, df):
        if self.trim_start_date is None: return df
            
        return df[df['Date'] > self.trim_start_date]
    
    def remove_original_installment(self, table_list, re_pattern):
        ## Remove installment items on start on this month   
        for row in table_list.itertuples():
            if re.search(re_pattern, row.Description, re.IGNORECASE):
                installment_item = table_list.index[table_list['Amount'] == abs(row.Amount)]
                table_list.drop(installment_item, inplace=True)
        return table_list
    
    def remove_non_first_installment(self, table_list, re_pattern='(.*)([0-9]{3})\/([0-9]{3})'):
        ## Create Installament for next months   
        for row in table_list.itertuples():
            # print(row.Description)
            installment = re.search(re_pattern, row.Description , re.IGNORECASE)
            if installment :
                ins_max = int(installment[3])
                ins_current = int(installment[2])
                ins_next = ins_current + 1
                
                # Drop for other month on statement
                if ins_current > 1:
                    table_list.drop(row.Index, inplace=True)
        return table_list            
    
    def generate_installment(self, table_list, re_pattern='(.*)([0-9]{3})\/([0-9]{3})'):
                
        table_list = self.trim_date_after(table_list)
        ## Create Installament for next months   
        next_ins_data = []
        for row in table_list.itertuples():
            # print(row.Description)
            installment = re.search(re_pattern, row.Description , re.IGNORECASE)
            if installment :
                ins_max = int(installment[3])
                ins_current = int(installment[2])
                ins_next = ins_current + 1
                
                # Drop for other month on statement
                if ins_current == 1: 
                    # If this month is 1, generate pending
                    description = 'ผ่อน '+installment[1]+' '
                    # Set description to 'ผ่อน'
                    table_list.at[row.Index, 'Description'] = description+str(ins_current)+'/'+str(ins_max)
                    
                    for ins_pending in range(ins_next,(ins_max+1)):
                        
                        new_date = row.Date + pandas.DateOffset(months=(ins_pending-ins_next+1))
                        # print(row.Date,new_date)
                        note = 'ผ่อน ',ins_pending,'/',ins_max
                        df_add = {
                            'Date': new_date,
                            'Description': description+str(ins_pending)+'/'+str(ins_max),
                            'Amount': row.Amount,
                            'Type': 'Expense',
                            'Note': 'ผ่อน '+str(ins_pending)+'/'+str(ins_max)
                        }
                        next_ins_data.append(df_add)
                       
        return next_ins_data                   

