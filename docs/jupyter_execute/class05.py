#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


url = 'https://www.dropbox.com/s/u1safsdjh4n7pt3/dataucomp.txt?dl=1'
data = pd.read_csv(url, sep='\t', encoding='ISO-8859-1')
len(data)


# In[3]:


data.columns = data.columns.str.lower()
data = data.drop_duplicates(['gvkey', 'year', 'execid'])
len(data)


# In[4]:


data['chair_id'] = np.where(data['titleann'].str.contains('chmn|chairman'), 1, 0)
data['duality'] = np.where((data['ceoann']=='CEO') & (data['chair_id']==1), 1, 0)


# In[5]:


# Count number of executives
pct_female = (data.groupby(['gvkey', 'year', 'gender'])
    ['execid'].count().unstack())

# Fill missing values
pct_female = pct_female.fillna(0)

# Total number of executives
pct_female['total'] = pct_female['FEMALE'] + pct_female['MALE']

# Count number of female CEO
female_ceo = (data[(data['ceoann']=='CEO') & (data['gender']=='FEMALE')]
    .groupby(['gvkey', 'year'])['execid'].count().to_frame('n_female_ceo'))

# Merge datasets
pct_female = pct_female.join(female_ceo, how='left')

# Fill missing values
pct_female = pct_female.fillna(0)

# Percentage of female executives
pct_female['pct_female'] = pct_female['FEMALE'] / pct_female['total']

# Percentage of female CEOs
pct_female['pct_female_ceo'] = pct_female['n_female_ceo'] / pct_female['total']

# Calculate averge percentage by year
pct_female = (pct_female.groupby(level=1)
    [['pct_female', 'pct_female_ceo']].mean())

# Average during the sample period
pct_female.mean()

