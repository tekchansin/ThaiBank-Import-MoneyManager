from src.FirstChoice import FirstChoice
from src.Kbank import KBANK
from src.SCB import SCB
from src.TTB import TTBCredit
import os

outputpath = './output/mew/'

def firstchoice():
    pdf_pass = 'xxx'
    trim_start_date = None
    # trim_start_date = '16/02/2024'
    path = './input/xxx/krungsri/*.PDF'
    account = 'Krungsri'
    FirstChoice(path, outputpath, account, pdf_pass, trim_start_date).exec()
    
def scb():
    pdf_pass = 'xxxx'
    # trim_start_date = None
    trim_start_date = '21/02/2024'
    path = './input/xxx/scb/*.pdf'
    account = 'SCB xxx'
    SCB(path, outputpath, account, pdf_pass, trim_start_date).exec()

def kbank():
    trim_start_date = None
    # trim_start_date = '21/02/2024'
    pdf_pass = 'xxx'
    path = './input/xxxx/kbank/*.pdf'
    account = 'xxx'
    KBANK(path, outputpath, account, pdf_pass, trim_start_date).exec()

def ttb():
    pdf_pass = 'xxxx'
    trim_start_date = None
    trim_start_date = '13/02/2024'
    path = './input/xxxxx/ttb/*.pdf'
    account = 'TTB Absolute'
    TTBCredit(path, outputpath, account, pdf_pass, trim_start_date).exec()

def cleanup():
    import glob
    for filename in glob.glob(outputpath+'/*.tsv'):
        os.remove(filename)


cleanup()

firstchoice()
scb()
kbank()
ttb()
