# Import packages
import os
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time


def CallAPI(url):
    r = requests.get(url)
    content = json.loads(r.content.decode('utf-8'))

    # If API returns error, the program will sleep for 1 minute and recall the API
    while 'accounts' not in content.keys():
        print(content)
        time.sleep(60)
        r = requests.get(url)
        content = json.loads(r.content.decode('utf-8'))

    # len(Accounts_Detail) = Total_Account_Num
    Accounts_Detail = content['accounts']

    return Accounts_Detail
    
def Create_DataFrame(ExistingDF, New_Account):

    # Create a dataframe for new account record 
    Feature_List = list(New_Account.keys())
    Account_Value = list(New_Account.values())
    New_Account_DF = pd.DataFrame([Account_Value], columns=Feature_List)
    ExistingDF = ExistingDF.append(New_Account_DF)

    return ExistingDF

def Write_New_CSV(DF, Local_Path):
    DF.to_csv(Local_Path,index=False)

def Write_Existing_CSV(DF, Local_Path):
    DF.to_csv(Local_Path, index=False, mode='a', header=False)

        
# Define the time interval for the records to be download
Num_Days = 30
Num_Half_Days = 2*Num_Days

# Current time
Current_Time = datetime.utcnow()
# End at 00:00
Current_Time = datetime.combine(Current_Time, datetime.min.time())

Original_Time = Current_Time + timedelta(days=-0)

i = 1
Accounts_DF = pd.DataFrame()

while i <= Num_Half_Days:
    # End time
    End_Time = Original_Time + timedelta(hours=-12*(i-1))
    End_Time_Str = End_Time.strftime('%Y-%m-%dT%H:%M:%SZ')
    # Start time
    Start_Time = Original_Time + timedelta(hours=-12*i)
    Start_Time_Str = Start_Time.strftime('%Y-%m-%dT%H:%M:%SZ')

    # API url
    API_url = 'https://data.ripple.com/v2/accounts/?start=' + Start_Time_Str + '&end=' + End_Time_Str + '&limit=1000'

    # Download Data for that 'day'
    Accounts_Detail = CallAPI(API_url)
    # If Accounts_Detail has data records
    if (len(Accounts_Detail) != 0):
        Accounts_DF_Day = pd.DataFrame(Accounts_Detail)
        Accounts_DF = Accounts_DF.append(Accounts_DF_Day)
        Accounts_DF = Accounts_DF.reset_index(drop=True)
    
    i += 1

# Data transformation
Accounts_DF['DateTime'] = Accounts_DF['inception'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
del Accounts_DF['inception']
Accounts_DF.sort_values(by=['DateTime'], inplace=True, ascending=False)
Accounts_DF = Accounts_DF.reset_index(drop=True)
print(len(Accounts_DF))

# Write data to csv file
cwd = os.path.dirname(os.path.realpath(__file__))
FilePath = cwd + '\\Create_Accounts_Num.csv'

if os.path.exists(FilePath):
    Write_Existing_CSV(Accounts_DF, FilePath)
else:
    Write_New_CSV(Accounts_DF, FilePath)