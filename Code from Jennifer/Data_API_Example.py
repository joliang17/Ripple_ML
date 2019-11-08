# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
# from IPython import get_ipython


# #%%
# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')


#%%
import pyrds
import pandas as pd
import requests
import datetime

# from google.cloud import bigquery
# client = bigquery.Client()


#%%

# Define the time range of transactions we want to obtain from Data API
lookback = 7

today = datetime.datetime.today()
start_date = (today - datetime.timedelta(days=lookback)).strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

#%% [markdown]
# Accounts created daily

#%%

# Define the specific address of Data API that we will call
url = f'https://data.ripple.com/v2/stats/?start={start_date}&end={end_date}&interval=day&family=metric&metrics=accounts_created'

# Core code to download data from online
res = requests.get(url)
xrp_accts = pd.DataFrame(res.json()['stats'])
xrp_accts

#%% [markdown]
# Network stats: number of nodes and validators

#%%
date_list = [x.strftime('%Y-%m-%dT%H:%M:%SZ') for x in list(pd.date_range((today - datetime.timedelta(days=lookback)).strftime('%Y%m%d'),today.strftime('%Y%m%d'),freq='1D'))]
node_list = []

for d in date_list:
    url = f'https://data.ripple.com/v2/network/topology?verbose=true&date={d}'
    res = requests.get(url)
    try:
        node_list.append(res.json()['node_count'])
    except:
        node_list.append(None)
        print(f'Error with {d}')
nodes_df = pd.DataFrame({'date': date_list, 'nodes': node_list})
nodes_df


#%%
res = requests.get(f'https://data.ripple.com/v2/network/validators')
res.json()['count']

#%% [markdown]
# Ledger data: transaction count and value
# 
# Requires a GBQ account. You can provide service account JSON credentials as an argument. If you want to run as your google user from your PC, you should first install the [Google Cloud SDK](https://cloud.google.com/sdk/), then run:
# `gcloud auth application-default login`

# #%%
# def gbq_query(query, query_params=None):
#     """
#     Run a query against Google Big Query, returning a pandas dataframe of the result.

#     Parameters
#     ----------
#     query: str
#         The query string
#     query_params: list, optional
#         The query parameters to pass into the query string
#     """
#     client = bigquery.Client()
#     job_config = bigquery.QueryJobConfig()
#     job_config.query_parameters = query_params
#     return client.query(query, job_config=job_config).to_dataframe()


# #%%
# query = """
# select
#     date(l.CloseTime) as `date`
#     , t.TransactionType
#     , count(1) as txn_count
#     , sum(t.AmountXRP) / 1e6 as txn_value
# from `xrpledgerdata.fullhistory.transactions` t
# join `xrpledgerdata.fullhistory.ledgers` l
#     on t.LedgerIndex = l.LedgerIndex
# where t.TransactionResult = "tesSUCCESS"
#     and date(l.CloseTime) >= CAST(@start_date AS DATE)
# group by 1,2
# order by 1 desc, 2
# """

# query_params = [
#     bigquery.ScalarQueryParameter("start_date", "STRING", start_date)
# ]

# xrp = gbq_query(query,query_params)
# xrp


# #%%


