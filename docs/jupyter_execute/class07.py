#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import statsmodels.api as sm
from linearmodels import PanelOLS


# In[2]:


url = 'https://www.dropbox.com/s/uso1u9asqam7rp1/merged.dta?dl=1'
data = pd.read_stata(url)
data['yyyymm'] = data['yyyymm'].astype(int)
data = data.sort_values(['cusip', 'yyyymm'], ignore_index=True)


# In[3]:


data['ret'] = pd.to_numeric(data['ret'], errors='coerce')
data['year'] = (data['yyyymm']/100).astype(int)
data = data.drop_duplicates(['cusip', 'year']).copy()
data['lnme'] = np.log(data['me'])
data = data.sort_values(['cusip', 'year'], ignore_index=True)
data['lag_lnme'] = data.groupby('cusip')['lnme'].shift(1)
data['lag_year'] = data.groupby('cusip')['year'].shift(1)
data['year_diff'] = data['year'] - data['lag_year']
data.loc[data['year_diff']!=1, 'lag_lnme'] = np.nan
data = data.dropna(subset=['lag_lnme', 'ret'], how='any')
data = data[['cusip', 'year', 'ret', 'lag_lnme']]


# In[4]:


est = sm.OLS(data['ret'], sm.add_constant(data['lag_lnme'])).fit()
est.summary()

# robust standard error
(sm.OLS(data['ret'], sm.add_constant(data['lag_lnme']))
    .fit(cov_type='hc0', use_t=True).summary())


# In[5]:


data['a'] = est.params[0]
data['b'] = est.params[1]

data['p_calc'] = data['a'] + data['b']*data['lag_lnme']
data['p_est'] = est.predict()

data['e_calc'] = data['ret'] - data['p_calc']
data['e_est'] = est.resid


# In[6]:


data1 = data.set_index(['cusip', 'year'])
panel_est = (PanelOLS(data1['ret'], sm.add_constant(data1['lag_lnme']),
    entity_effects=True).fit())
panel_est.summary


# In[7]:


panel_est = (PanelOLS(data1['ret'], sm.add_constant(data1['lag_lnme']),
    entity_effects=True).fit(cov_type='robust'))
panel_est.summary


# In[8]:


panel_est = (PanelOLS(data1['ret'], sm.add_constant(data1['lag_lnme']),
    entity_effects=True) .fit(cov_type='clustered', cluster_entity=True))
panel_est.summary

