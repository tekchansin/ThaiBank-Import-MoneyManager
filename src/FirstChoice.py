from src.BankStatement import BankStatement
from src.MoneyManager import MoneyManager
from src.PDF import PDFExtract
import pandas 
import re
from dateutil import parser
import glob
import PyPDF2

class FirstChoice(BankStatement):
        
    def __init__(self, *args, **kwargs):
        super(FirstChoice, self).__init__(*args, **kwargs)
    
    def exec(self):
        print('Scanning: '+self.__class__.__name__)
        files = glob.glob(self.inputpath)
        for file in files:
            statementfile = file 
            ## Read page number
            reader = PyPDF2.PdfReader(open(statementfile, mode='rb'), password=self.pdfpass )
            nums_page = len(reader.pages)
            
            df_list = PDFExtract.read_pdf(statementfile, self.pdfpass, 
                                        pdfpages='1', ignore_header=True, streammode=True,
                                        # area_table=[542.817,36.461,824.085,578.906],
                                        area_table=[440.876,37.205,826.317,578.162],
                                        pdfcolumns=[20,30,70,85,95]
                                        )
            
            table_list = self.extract_data(df_list)
            # Select from page 2 and skip last page
            for page in range(2, (nums_page)):
                df_list = PDFExtract.read_pdf(statementfile, self.pdfpass, 
                                            pdfpages=page, ignore_header=True, streammode=True,
                                            area_table=[116.451,29.764,817.388,578.162],
                                            pdfcolumns=[20,30,70,85,95]
                                            )
                other_page = self.extract_data(df_list)
                table_list = pandas.concat([table_list,other_page], ignore_index=True )
            
            
            table_list = self.trim_date_after(table_list)
            # print(type(table_list))
            table_list = MoneyManager.etl(table_list, self.account)
            
            # print(table_list)
            MoneyManager.save_csv(table_list, self.outputpath, self.account)
    
        
    def extract_data(self, df_list):
        dataframe_list = []
        # print(df_list)
        # return
        for table in df_list:
            df = pandas.DataFrame(table)
            row, col = df.shape
            print('Table: Row/Columns: ',row,'/',col)
            if col == 6:
                df.columns = ["Date2", "Date",  "Description", 'other','Installment', 'Amount']
                df.drop(['Date2'], axis=1, inplace=True)
                df.drop(['other'], axis=1, inplace=True)    
                df['Note'] = ''   
                dataframe_list.append(df)
            
        ## Merge Table   
        if not dataframe_list:
           return  
        table_list = pandas.concat(dataframe_list, ignore_index=True )
        
        ## Installment Grouping
        for row in table_list.itertuples():
            if (type(row.Description) == str)  and re.search('FIRST CHOICE PLAN ON DEMAND', row.Description, re.IGNORECASE):
                item = table_list.at[row.Index+1, 'Description']
                table_list.at[row.Index, 'Description'] = item+' '+row.Installment
                table_list.drop(row.Index+1, inplace=True)
                table_list.drop(row.Index+2, inplace=True)    
          
        ## Remove thousond ','
        table_list['Amount'].replace(',','', regex=True, inplace=True)
          
        ## Remove which can't parse data
        for row in table_list.itertuples():
            try:
                parser.parse(row.Date)
                float(row.Amount)
                pandas.to_datetime(row.Date, format='%d/%m/%y') 
            except:
                table_list.drop(row.Index, inplace=True)
        
        ## Convert Amount to numberic   
        table_list['Amount'] = pandas.to_numeric(table_list['Amount'])
      
        table_list = self.remove_original_installment(table_list,'REV-FC PLAN')
        
        ## Calculate Expense/Income        
        for row in table_list.itertuples():
            if row.Amount > 0:
                table_list.at[row.Index, 'Type'] = 'Expense'
            elif re.search('ยอดชาระดว้ยเงินสด', row.Description, re.IGNORECASE):
                #force drop
                table_list.drop(row.Index, inplace=True)
            else:
                table_list.drop(row.Index, inplace=True)
            
        ## Convert type to DateTime        
        table_list['Date'] = pandas.to_datetime(table_list['Date'], format='%d/%m/%y',errors='coerce') 
        is_thai_year = False
        for row in table_list.itertuples():
            if row.Date.year > 2050:
                is_thai_year =True
        ## Convert พศ to คศ
        if is_thai_year:
            table_list['Date'] = table_list['Date'] - pandas.DateOffset(years=43)
            
        # Remapping Column
        table_list.drop(['Installment'], axis=1, inplace=True)
        table_list = table_list[['Date','Type','Amount',  'Description', 'Note']]

        # Replace new line
        table_list['Description'] =table_list['Description'].str.replace('\r', ' ').astype(str)
        
        table_list = self.remove_non_first_installment(table_list)
        next_ins_data = self.generate_installment(table_list)
        table_list = pandas.concat([table_list, pandas.DataFrame(next_ins_data)], ignore_index=True)
        
        # print(table_list)
        return table_list
    