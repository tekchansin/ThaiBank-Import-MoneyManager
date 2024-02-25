
import pandas
import re
import csv
import os
import glob
## Date – Account – Category – Subcategory – Note – Amount -Income/Expense – Description

class MoneyManager:
    
     def etl(df: pandas, account = '', category='Other'):
          if type(df) == None:
               return df
          #    print(type(df))
          row, col = df.shape
          if row == 0:
               return df
          
          df.columns = ["Date", "Income/Expense", "Amount", 'Note', 'Description']
          df['Date'] = df['Date'].dt.strftime("%d/%m/%Y")
          df['Account']=account
          df['Category']=category
          df['Description']=''
          df['Subcategory']=''
          for row in df.itertuples():
               
               ## Expense
               keywork_7_11 = ['TRUE MONEY', '7-11']
               keywork_Coffee = ['BOONTERM']
               keyword_Food = ['PromptPay x1940', 'KBANK x5554', 'SPAGHETTI', 'MO-MO-PARADISE', 
                              'RESTAURANT', 'UNATOTO', 'LINE MAN', 'PONZU', 'BUFFET', 'PromptPay x3892', 
                              'PromptPay x2415', 'PHEEPORK', 'เตมเงน', 'รานถงเงน', 'ไลนแมน', 'DONKI', 'WONGNAI',
                              'พซซา', 'x9346', 'X5147', 'GRAB']
               keyword_Gift = ['KBANK x7217', 'BAY x5866','KBANK x1843', 'ภทราพร', 'X4379', 'X0330']
               keyword_Shopping = ['SHOPEE' ,'UNIQLO', 'TIKTOK', 'BEAUTRIUM', 'MR.D.I.Y.','EVEANDBOY', 'LAZADA','LOFT','WATSONS']
               keyword_Credit = ['First Choice', 'TTB x8650', 'SCB/CardX']
               keyword_Transport = ['ESSO', 'CALTEX', 'PPT', 'ENERGY', 'BANGCHAK','BSRC-TERM TEM THANG', 'ROOJAI', 'เอสโซ']
               keyword_Health = ['Xtend-Life', 'SAMSUNG LIFE-TH', 'ALLIANZ AYUDHYA', 'HOSPITAL']
               keyword_Social = ['Netflix', 'Google Storage', 'APPLE.COM', 'KBANK x1415', 'ISERVICECCP', 'เอไอเอส', 'X9844']
               keyword_Household = ['ttb touch\* BANGKOK', 'LIVING MALL', 'X3887']
               keywork_Transfer = ['ชาญศลป', 'กญชลา']
               keywork_Investment = ['ONE TWO PAY']
               
               ## Income
               keyword_Salary = ['NIPA', 'PAYROLL']
               
               ## Transfer to self account     
               if re.search('|'.join(keywork_Transfer), row.Note, re.IGNORECASE) or row.Note == 'Transfer out':
                    df.at[row.Index, "Income/Expense"] = 'Transfer out'  
                    if re.search('X8120', row.Note, re.IGNORECASE): ## Mew
                         df.at[row.Index, 'Category'] =  'SCB saving'   
                    elif re.search('X4120', row.Note, re.IGNORECASE): ## Mew
                         df.at[row.Index, 'Category'] =  'Kbank'       
                    elif re.search('X7550', row.Note, re.IGNORECASE): ## Mew
                         df.at[row.Index, 'Category'] =  'Kbank invest'       
                    elif re.search('X7336', row.Note, re.IGNORECASE): ## Mew
                         df.at[row.Index, 'Category'] =  'Kbank dream'  
                    elif re.search('X8721', row.Note, re.IGNORECASE): ## Mew
                         df.at[row.Index, 'Category'] =  'Kbank short'   
                    else:
                         df.at[row.Index, 'Category'] =  'Transfer'   
               
               if re.search('|'.join(keywork_7_11), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '🍘 7-11'
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif re.search('|'.join(keywork_Coffee), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '☕️ Coffee'
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif re.search('|'.join(keyword_Food), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '🍜 Food'    
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif re.search('|'.join(keyword_Gift), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '🎁 Gift'  
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif re.search('|'.join(keyword_Shopping), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '🧥 Shopping'     
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif re.search('|'.join(keyword_Credit), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '💳 Credit Card'    
                    df.at[row.Index, "Income/Expense"] = 'Expense'  
               elif re.search('|'.join(keyword_Transport), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '🚖 Transport'   
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif re.search('|'.join(keyword_Health), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '🧘🏼 Health'       
                    df.at[row.Index, "Income/Expense"] = 'Expense'  
               elif re.search('|'.join(keyword_Social), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '👬🏻 Social Life'    
                    df.at[row.Index, "Income/Expense"] = 'Expense'      
               elif re.search('|'.join(keyword_Household), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '🪑 Household'
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif re.search('|'.join(keyword_Salary), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '💰 Salary'
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif re.search('|'.join(keywork_Investment), row.Note, re.IGNORECASE):
                    df.at[row.Index, 'Category'] = '💰 Invest'
                    df.at[row.Index, "Income/Expense"] = 'Expense' 
               elif row.Category == category and row.Amount <= 300:
                    df.at[row.Index, 'Category'] = '🍜 Food'
               
               ### Pay with true money
               if re.search('X2838', row.Note, re.IGNORECASE):
                    ## Credit Card Homepro
                    df.at[row.Index, 'Category'] = 'Krungsri'
                    df.at[row.Index, "Income/Expense"] = 'Transfer out'  
                    
               ## amount less than 300, set to Food
               
          return df
    
     def save_csv(df, outputpath, prefix):
          row, col = df.shape
          if row != 0:
               prefix = prefix.replace(" ", "-")
               lastday = df['Date'].values[0:][0].replace('/','')
               firstday = df['Date'].values[-1:][0].replace('/','')
               outputfile =  outputpath+'./'+prefix+firstday+'-'+lastday+'.tsv'
               df.to_csv(outputfile, encoding='utf-8', index=False, sep="\t", quoting=csv.QUOTE_NONNUMERIC,
                         columns=['Date','Account','Category',  'Subcategory',  'Note', 'Amount', 'Income/Expense',  'Description'])
        
     def cleanup(self, outputpath):
          for filename in glob.glob(outputpath+'/*.tsv'):
               os.remove(filename)