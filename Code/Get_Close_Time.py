#%%
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time

def CallAPI(url):
    r = requests.get(url)
    content = json.loads(r.content.decode('utf-8'))
    content_parsed = content
    while 'ledger' not in content_parsed.keys():
        print(content_parsed)
        time.sleep(1)
        r = requests.get(url)
        content = json.loads(r.content.decode('utf-8'))
        content_parsed = content
    # try: 
    #     Ledger_Content = content_parsed['ledger']
    # except: 
    #     print(r.content)
    #     time.sleep(5)
    #     Ledger_Data = 0
    #     Ledger_Index = 0
    #     Ledger_Time = 0
    # else:
    Ledger_Content = content_parsed['ledger']
    Feature_List = list(Ledger_Content.keys())
    Ledger_Value = list(Ledger_Content.values())

    Ledger_Data = pd.DataFrame([Ledger_Value], columns=Feature_List)

    Ledger_Index = Ledger_Content['ledger_index']
    Ledger_Time = Ledger_Content['close_time']
    Ledger_Time = datetime.fromtimestamp(int(Ledger_Time)) + timedelta(hours=7)
    return Ledger_Data, Ledger_Index, Ledger_Time

#%%
End_Time = datetime.utcnow()
Start_Time = datetime.utcnow() + timedelta(hours=-24)
Start_Time_Str = Start_Time.strftime('%Y-%m-%dT%H:%m:%SZ')

#%%

Ledger_Data, Last_Ledger_Index, Last_Ledger_Time = CallAPI('https://data.ripple.com/v2/ledgers/' + Start_Time_Str)

while Last_Ledger_Time <= End_Time:
    Last_Ledger_Index = Last_Ledger_Index + 1

    temp, Ledger_Index, Ledger_Time = CallAPI('https://data.ripple.com/v2/ledgers/' + str(Last_Ledger_Index))
    if (Ledger_Index != 0):
        Ledger_Data = Ledger_Data.append(temp)
        Last_Ledger_Time = Ledger_Time
        Last_Ledger_Index = Ledger_Index

Ledger_Data
Ledger_Data.to_csv('Ledger_Data.csv')