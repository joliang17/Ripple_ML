#%% 
import requests
import json
import csv

#%%
r = requests.get('https://data.ripple.com/v2/transactions?start=2019-10-07')
#%%
r
#%%
content = json.loads(r.content.decode('utf-8'))
# print(content)

content_parsed = content
Ripple_data = content_parsed['transactions']
# open a file for writing
Ripple_csv = open('Data.csv', 'w')

# create the csv writer object
csvwriter = csv.writer(Ripple_csv)
count = 0

# Read dictionary type of data, and transform it to csv
for Transaction in Ripple_data:
      if count == 0:
            header = Transaction.keys()
            csvwriter.writerow(header)
            count += 1
      csvwriter.writerow(Transaction.values())

Ripple_csv.close()