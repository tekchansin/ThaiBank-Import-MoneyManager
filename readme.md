## Install on MacOS
- brew install java
- pip3 install -r requirement.txt
- export JAVA_HOME=/opt/homebrew/opt/openjdk

## Feature
- Read all PDFs from folder
- ETL processing for each Type
- grouping Installment line
- Remove USD Currency
- export to TSV format (Money Manager)
- trim start date from Statement (repeat import in same month)
- Auto categories by text description
- Auto detect transaction type (Expense/Income/Transfer)
- Detect first month of Installment and create others

## Benefit on MoneyManager
- Trace all credit card usage by transaction date
- Know How much need to pay at the end of the month
- See all expenses on all wallet type

## Statement support tyoe
- SCB Statement account (SCB Easy)
- TTB Creditcard (TTB touch, export statement)
- FirstChoice Credicard (Monthly via email)
- KBank Statement account 

## How to use
- upload statement to folder input/<profile>/banktype/<pdf>
- modify sample.py, input pdf pass
- run python script, output will be at /output/xx
- upload output file to MoneyManager
- import from MoneyManager App (Select DateFormat dd.mm.yyy)