# Import packages
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time

def CallAPI(url):
    r = requests.get(url)
    content = json.loads(r.content.decode('utf-8'))

    # If want to keep calling this API until return the normal data
    while 'ledger' not in content.keys():
        time.sleep(60)
        r = requests.get(url)
        content = json.loads(r.content.decode('utf-8'))

    Ledger_Content = content['ledger']
    
    # Create a dataframe for this ledger record 
    Feature_List = list(Ledger_Content.keys())
    Ledger_Value = list(Ledger_Content.values())
    Ledger_Data = pd.DataFrame([Ledger_Value], columns=Feature_List)

    # Get this ledger index
    Ledger_Index = Ledger_Content['ledger_index']
    
    # Get the close time for this ledger, and transform it to the datatime (Compare with the End_Time in the while loop below)
    Ledger_Time = Ledger_Content['close_time']
    Ledger_Time = datetime.fromtimestamp(int(Ledger_Time)) + timedelta(hours=7)

    return Ledger_Data, Ledger_Index, Ledger_Time


# End time (current time)
End_Time = datetime.utcnow()

# Start time
Start_Time = datetime.utcnow() + timedelta(hours=-1)
Start_Time_Str = Start_Time.strftime('%Y-%m-%dT%H:%M:%SZ')

Ledger_Data, Last_Ledger_Index, Last_Ledger_Time = CallAPI('https://data.ripple.com/v2/ledgers/' + Start_Time_Str)

while Last_Ledger_Time <= End_Time:
    Last_Ledger_Index = Last_Ledger_Index + 1

    # Use ledger index to get data of the new ledger
    temp, Ledger_Index, Ledger_Time = CallAPI('https://data.ripple.com/v2/ledgers/' + str(Last_Ledger_Index))
    
    Ledger_Data = Ledger_Data.append(temp)
    Last_Ledger_Time = Ledger_Time
    Last_Ledger_Index = Ledger_Index


# Get the close time difference
Ledger_Data['close_time_difference'] = Ledger_Data['close_time'] - Ledger_Data['parent_close_time']

# Write it to csv file
Ledger_Data.to_csv('Ledger_Data.csv')