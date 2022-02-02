#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# This url contains sample data from CRSP
url = 'https://www.dropbox.com/s/6mk86g97uji2f80/crsp_month_raw.txt?dl=1'
crsp_raw = pd.read_csv(url, sep='\t', low_memory=False)

# View first 5 rows and first 5 columns
crsp_raw.iloc[:5, :5]


# In[3]:


# Observations
len(crsp_raw)


# In[4]:


# Number of rows and columns (variables)
crsp_raw.shape


# In[5]:


# List all variables in the dataset
crsp_raw.columns


# In[6]:


# Data type of variables
crsp_raw.dtypes

crsp_raw.info()


# In[7]:


# Rename uppercase to lowercase
# Typing lowercase is easier than uppercase
crsp_raw.columns = crsp_raw.columns.str.lower()

# Convert data type of date to date format
# So that we can apply date functions when manipulating dates
crsp_raw['date'] = pd.to_datetime(crsp_raw['date'], format='%Y%m%d')

# Convert data type of ret to numerical value
# Stock return should be numerical values rather than string
# For example,
#  string: '1' + '2' = '12'
#  numerical: 1 + 2 = 3
crsp_raw['ret'] = pd.to_numeric(crsp_raw['ret'], errors='coerce')

# Convert siccd to numerical value
crsp_raw['siccd'] = pd.to_numeric(crsp_raw['siccd'], errors='coerce')

crsp_raw.info()


# In[8]:


crsp = crsp_raw.copy()

# Keep NYSE/AMEX/NASDAQ
crsp = crsp[crsp['exchcd'].isin([1, 2, 3])]

# Keep common shares
crsp = crsp[crsp['shrcd'].isin([10, 11])]

# Convert shrcd and exchcd to int
crsp[['exchcd', 'shrcd']] = crsp[['exchcd', 'shrcd']].astype(int)

len(crsp)


# In[9]:


crsp = crsp.drop_duplicates(['permno', 'date'])
len(crsp)


# In[10]:


temp = crsp.copy()
# Convert shrcd and exchcd to category
temp[['exchcd', 'shrcd']] = temp[['exchcd', 'shrcd']].astype('category')
temp.info()


# In[11]:


# If you want to import from local
# file_path = '/Users/ml/Dropbox/teaching/data/crsp_month.txt'
# crsp = pd.read_csv(file_path, sep='\t', parse_dates=['date'])

# Import from url
url = 'https://www.dropbox.com/s/0nuxwo3cf7vfcy3/crsp_month.txt?dl=1'
crsp = pd.read_csv(url, sep='\t', parse_dates=['date'])


# In[12]:


# Market value
crsp['price'] = crsp['prc'].abs()
crsp['me'] = (crsp['price']*crsp['shrout']) / 1000
crsp['lnme'] = np.log(crsp['me'])

# Adjusted price
crsp.loc[crsp['cfacpr']>0, 'adjprc'] = crsp['price'] / crsp['cfacpr']

# Holding period returns
crsp['yyyymm'] = crsp['date'].dt.year*100 + crsp['date'].dt.month

# Monthly index
# From 1 to n
# For example, month index will be from 1 to 120 if we have 120 months data
month_idx = crsp.drop_duplicates('yyyymm')[['yyyymm']].copy()
month_idx = month_idx.sort_values('yyyymm', ignore_index=True)
month_idx['midx'] = month_idx.index + 1

crsp = crsp.merge(month_idx, how='left', on='yyyymm')

# Past 6-month returns
crsp['logret'] = np.log(crsp['ret']+1)
crsp = crsp.sort_values(['permno', 'yyyymm'], ignore_index=True)
crsp['hpr'] = (crsp.groupby('permno')['logret']
  .rolling(window=6, min_periods=6).sum().reset_index(drop=True))
crsp['hpr'] = np.exp(crsp['hpr']) - 1

crsp['midx_lag'] = crsp.groupby('permno')['midx'].shift(5)
crsp['gap'] = crsp['midx'] - crsp['midx_lag']

temp1 = crsp.query('permno==10028 & 201107<=yyyymm<=201212').copy()

# Replace it by missing if there is month gap.
crsp.loc[crsp['gap']!=5, 'hpr'] = np.nan

temp2 = crsp.query('permno==10028 & 201107<=yyyymm<=201212').copy()


# In[13]:


temp1[['permno', 'yyyymm', 'midx', 'midx_lag', 'gap', 'ret', 'hpr']]


# In[14]:


temp2[['permno', 'yyyymm', 'midx', 'midx_lag', 'gap', 'ret', 'hpr']]


# In[15]:


crsp[['ret', 'lnme']].describe()


# In[16]:


# Percentiles
crsp[['ret', 'lnme']].describe(percentiles=[0.1, 0.9])


# In[17]:


# Summary statistics by year
crsp['year'] = crsp['date'].dt.year
round(crsp.groupby('year')[['ret', 'lnme']].describe()
.loc[:, (slice(None), ['mean', '50%', 'std'])], 4)


# In[18]:


# Summary statistics by stock exchange
round(crsp.groupby('exchcd')[['ret', 'lnme']].describe()
.loc[:, (slice(None), ['mean', '50%', 'std'])], 4)


# In[19]:


# Summary statistics in subsamples
print('Before 2015')
print(crsp.query('year<=2015')[['ret', 'lnme']].describe())
print('\nAfter 2015')
print(crsp.query('year>=2016')[['ret', 'lnme']].describe())

