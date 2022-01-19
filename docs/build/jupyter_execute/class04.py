#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

url = 'https://www.dropbox.com/s/3x230qb3fkopij3/datastream_asset.xlsx?dl=1'
asset = pd.read_excel(url, sheet_name='asset')


# In[2]:


asset = pd.melt(asset, id_vars='Code', value_vars=asset.columns[1:],
    value_name='asset')
asset['isin'] = asset['variable'].str[:12]
asset = asset[['isin','Code','asset']]
asset = asset.rename(columns={'Code': 'year'})
asset.head()

