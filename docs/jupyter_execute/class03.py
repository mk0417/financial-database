#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


url = 'https://www.dropbox.com/s/qro99n7ngq0aztr/funda_raw.txt?dl=1'
funda_raw = pd.read_csv(url, sep='\t', low_memory=False)

# View first 5 rows and first 5 columns
funda_raw.iloc[:5, :5]


# In[3]:


# Data types
funda_raw.info()


# In[4]:


# Read the data again with consideration of the data type of gvkey
funda_raw = pd.read_csv(url, sep='\t', low_memory=False, dtype={'gvkey': str})

# View first 5 rows and first 5 columns
funda_raw.iloc[:5, :5]


# In[5]:


# Data types
funda_raw.info()


# In[6]:


funda_raw = funda_raw.sort_values(['gvkey', 'fyear', 'datadate'], ignore_index=True)
print(f'Number of obs: {len(funda_raw)}')

# Keep the most recent one if there are duplicates
funda = funda_raw.drop_duplicates(['gvkey', 'fyear'], keep='last').copy()
print(f'Number of obs after removing duplicates: {len(funda)}')

# Keep main stock exchanges
funda = funda[funda['exchg'].isin([11, 12, 14])].copy()
print(f'Number of obs after keeping main stock exchanges: {len(funda)}')

# Drop unnecessary variables
drop_vars = ['indfmt', 'consol', 'popsrc', 'datafmt', 'costat', 'curcd']
funda = funda.drop(columns=drop_vars)

# Drop if total asset and equity are not positive
funda = funda.query('at>0 & seq>0').copy()
print(f'Number of obs after requiring positive asset: {len(funda)}')


# In[7]:


funda['exchg'].value_counts()


# In[8]:


funda['date'] = pd.to_datetime(funda['datadate'], format='%Y%m%d')
funda['month'] = funda['date'].dt.month
funda['month'].value_counts()


# In[9]:


funda['roa'] = funda['ebit'] / funda['at']
funda['roe'] = funda['ebit'] / funda['seq']


# In[10]:


funda = funda.sort_values(['gvkey', 'fyear'], ignore_index=True)
funda['lag_at'] = funda.groupby('gvkey')['at'].shift(1)
funda['lag_fyear'] = funda.groupby('gvkey')['fyear'].shift(1)
funda['ag'] = funda['at'] / funda['lag_at'] - 1


# In[11]:


funda['fyear_diff'] = funda['fyear'] - funda['lag_fyear']
funda.query('fyear_diff>1')[['gvkey', 'fyear', 'lag_fyear', 'fyear_diff', 'ag']].head()


# In[12]:


funda.loc[funda['fyear_diff']>1, 'ag'] = np.nan


# In[13]:


round(funda[['roa', 'roe', 'ag']].describe(), 3)


# In[14]:


# Winsorising at 1% and 99% percentile
for i in ['roa', 'roe', 'ag']:
    funda['p1'] = funda.groupby('fyear')[i].transform(lambda x: x.quantile(0.01))
    funda['p99'] = funda.groupby('fyear')[i].transform(lambda x: x.quantile(0.99))
    funda.loc[funda[i]<funda['p1'], i] = funda['p1']
    funda.loc[funda[i]>funda['p99'], i] = funda['p99']
    funda = funda.drop(columns=['p1', 'p99'])

round(funda[['roa', 'roe', 'ag']].describe(), 3)

