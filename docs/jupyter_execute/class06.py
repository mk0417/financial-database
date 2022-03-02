#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


url = 'https://www.dropbox.com/s/484ynn8mzihgj9q/uk.txt?dl=1'
uk = pd.read_csv(url, sep='\t', low_memory=False, dtype={'gvkey': str})


# In[3]:


# Keep common shares
uk = uk[uk['tpci']=='0'].copy()

# Make sure fic is GBR
uk = uk[uk['fic']=='GBR'].copy()

# Keep primary share
uk = uk[uk['iid']==uk['prirow']].copy()

# Check duplicates
uk = uk.drop_duplicates(['gvkey', 'iid', 'datadate']).copy()

# Security level ID
uk['stkcd'] = uk['gvkey'].astype(str) + uk['iid']

# Adjusted price
uk['p_adj'] = (uk['prccd']/uk['ajexdi']) * uk['trfd']


# In[4]:


date_index = uk.drop_duplicates('datadate')[['datadate']].copy()
date_index = date_index.sort_values('datadate', ignore_index=True)
date_index['date_idx'] = date_index.index + 1


# In[5]:


uk1 = uk.merge(date_index, how='inner', on='datadate')
uk1 = uk1.sort_values(['stkcd', 'datadate'], ignore_index=True)
uk1['ldate_idx'] = uk1.groupby('stkcd')['date_idx'].shift(1)
uk1['lp_adj'] = uk1.groupby('stkcd')['p_adj'].shift(1)
uk1['date_diff'] = uk1['date_idx'] - uk1['ldate_idx']
uk1['ret'] = uk1['p_adj'] / uk1['lp_adj'] - 1

uk1['date_diff'].value_counts()


# In[6]:


uk1['ret'] = np.where(uk1['date_diff']<=3, uk1['ret'], np.nan)


# In[7]:


uk_month = uk1.query('monthend==1')[['stkcd', 'datadate', 'p_adj']].copy()

uk_month['yyyymm'] = (uk_month['datadate']/100).astype(int)
uk_month['year'] = (uk_month['yyyymm']/100).astype(int)
uk_month['month'] = uk_month['yyyymm'] % 100

uk_month['month_idx'] = (uk_month['year']-2020)*12 + uk_month['month'] - 6


# In[8]:


uk_month = uk_month.sort_values(['stkcd', 'yyyymm'], ignore_index=True)
uk_month['lmonth_idx'] = uk_month.groupby('stkcd')['month_idx'].shift(1)
uk_month['lp_adj'] = uk_month.groupby('stkcd')['p_adj'].shift(1)
uk_month['month_diff'] = uk_month['month_idx'] - uk_month['lmonth_idx']
uk_month['ret'] = uk_month['p_adj'] / uk_month['lp_adj'] - 1

# Monthly return is missing if month gap is not 1 month
uk_month['ret'] = np.where(uk_month['month_diff']==1, uk_month['ret'], np.nan)

