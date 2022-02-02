# Class05

## Execucomp overview
- Data source: company’s annual proxy (DEF14A SEC form)
- The dataset starts from 1992
- Universe
    - US firms
    - S&P500 from 1992 and S&P1500 from 1994
	- There is no ADR firms (ADRs do not need to submit proxy to SEC)

### Web access
WRDS --> Compustat - Capital IQ --> Execucomp

### Identifiers
- <dbvar>GVKEY</dbvar>
- <dbvar>CUSIP</dbvar>

### Important variables
<dl>
<dt><dbvar>YEAR</dbvar>
<dd>This is the fiscal year in Compustat Fundamentals Annual (Quarterly)
<dt><dbvar>CEOANN</dbvar>
<dd>Historical flag to indicate CEO in a particular year
<dt><dbvar>TITLEANN</dbvar>
<dd>Historical flag to describe the title
<dd>It is useful to determin if the executive officer serves as chairman of the board
<dt><dbvar>EXECID</dbvar>
<dd>Permanent ID for each executive
<dd>This ID does not change even the person moved to another company
<dt><dbvar>EXECDIR</dbvar>
<dd>Flag to indicate whether executive officer is also a director
<dt><dbvar>GENDER</dbvar>
<dd>It indicates female or male.
</dl>

- Understand CEOANN vs PCEO and AGE vs PAGE

|EXEC_FULLNAME   |YEAR |CEOANN |PCEO |AGE |PAGE |
|----------------|-----|-------|-----|----|-----|
|Timothy D. Cook |2010 |       |CEO  |49  |59   |
|Timothy D. Cook |2011 |       |CEO  |50  |59   |
|Timothy D. Cook |2012 |CEO    |CEO  |51  |59   |
|Timothy D. Cook |2013 |CEO    |CEO  |52  |59   |
|Timothy D. Cook |2014 |CEO    |CEO  |53  |59   |
|Timothy D. Cook |2015 |CEO    |CEO  |54  |59   |
|Timothy D. Cook |2016 |CEO    |CEO  |55  |59   |
|Timothy D. Cook |2017 |CEO    |CEO  |56  |59   |
|Timothy D. Cook |2018 |CEO    |CEO  |57  |59   |
|Timothy D. Cook |2019 |CEO    |CEO  |58  |59   |
|Timothy D. Cook |2020 |CEO    |CEO  |59  |59   |

## Python
- Import packages
```{jupyter-execute}
import pandas as pd
import numpy as np
```

- Import Execucomp data
```{jupyter-execute}
url = 'https://www.dropbox.com/s/u1safsdjh4n7pt3/dataucomp.txt?dl=1'
data = pd.read_csv(url, sep='\t', encoding='ISO-8859-1')
len(data)
```

```{attention}
You will get <strong>UnicodeDecodeError</strong> if you do not use encoding argument when importing data.
This is caused by special charcater, e.g. é.
See the link to learn about encoding: https://en.wikipedia.org/wiki/ISO/IEC_8859-1
```

- Clean the data
```{jupyter-execute}
data.columns = data.columns.str.lower()
data = data.drop_duplicates(['gvkey', 'year', 'execid'])
len(data)
```

- CEO duality
```{jupyter-execute}
data['chair_id'] = np.where(data['titleann'].str.contains('chmn|chairman'), 1, 0)
data['duality'] = np.where((data['ceoann']=='CEO') & (data['chair_id']==1), 1, 0)
```

- Percentage of female executives or CEOs
```{jupyter-execute}
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
```

## Stata
- Import Execucomp data
```{code-block} stata
local data_url "https://www.dropbox.com/s/u1safsdjh4n7pt3/dataucomp.txt?dl=1"
import delimited "`data_url'", clear
```

- Clean the data
```{code-block} stata
duplicates drop gvkey year execid, force
```

- CEO duality
```{code-block} stata
gen chair_id = 1 if strpos(titleann, "chmn")>0 | strpos(titleann, "chairman")>0
gen duality = 1 if chair_id==1 & ceoann=="CEO"
replace duality = 0 if duality==.
```

- Percentage of female executives or CEOs
```{code-block} stata
/* Count total number of executives */
bysort gvkey year: egen n_total = count(execid)

/* Count number of female executives */
gen gender_id = 1 if gender=="FEMALE"
replace gender_id = 0 if gender=="MALE"
bysort gvkey year: egen n_female = sum(gender_id)

/* Count number of female CEO */
gen gender_ceo = 1 if gender=="FEMALE" & ceoann=="CEO"
replace gender_ceo = 0 if gender_ceo == .
bysort gvkey year: egen n_female_ceo = sum(gender_ceo)

/* Keep firm level data */
duplicates drop gvkey year, force

/* Percentage of female executives */
gen pct_female = n_female / n_total

/* Percentage of female CEO */
gen pct_female_ceo = n_female_ceo / n_total

/* Calculate average percentage by year */
collapse (mean) pct_female=pct_female pct_female_ceo=pct_female_ceo, by(year)

/* Average during the sample period */
tabstat pct_female pct_female_ceo, s(mean)
```
