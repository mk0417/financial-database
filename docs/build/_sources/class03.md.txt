# Class03

## Compustat North America overview
- Data: accounting and price data
- Coverage: US and Canada
- Time period: 1950 - present (Fundamentals Annual)
- Frequency
    - Accounting data: yearly and quarterly
    - Price data: daily and monthly
- Dataset structure
    - Fundamentals Annual
    - Fundamentals Quarterly
    - Security Daily
    - Security Monthly

### Web access
Downlaod data from Compustat North America via WRDS web access.
- Dataset: Compustat North Ameria - Fundamentals Annual
- Time period: Jan 2000 to Dec 2020
- Search the entire database
- Screening variables
    - Consolidation Level: **C**
    - Industry Format: **INDL**
    - Data Format: **STD**
    - Population Source: **D**
    - Currency: **USD**
    - Company Status: **Active (A)** and **Inactive (I)**
- Variables
    - gvkey
    - cusip
    - exchg
    - sic
    - fyear
    - at
    - seq
    - ebit
- Output format
    - Tab-delimited text
    - Uncompressed
    - Date format: YYMMDDn8

### Industry Format
<dl>
<dt><dbvar>INDFMT</dbvar>
<dd>FS - financial services (includes banks, insurance companies, broker/dealers, real estate and other financial services)
<dd>INDL - other than financial services
</dl>

|gvkey  |fyear |indfmt |at        |capr1 |
|-------|------|-------|----------|------|
|007647 |2020  |FS     |2819627.0 |13.5  |
|007647 |2020  |INDL   |2819627.0 |      |

### Identifiers
<dl>
<dt><dbvar>GVKEY</dbvar>
<dd>Compustat permanent firm level identifier
<dd>They are permanent and never change
<dt><dbvar>CUSIP</dbvar>
<dd>Current 9-digit <dbvar>CUSIP</dbvar> (security level)
<dd>They can be changed.
<dt><dbvar>CIK</dbvar>
<dd>Central Index Key used for SEC filings
</dl>

```{attention}
**Leading zeros of GVKEY**

**GVKEY** is 6-digit character in string fromat. However, **GVKEY** contains numbers only and it will be recoganised as numerical values in some software by default. Therefore, the leading zeros will be dropped. For example, GVKEY 001050 might become 1050. This will cause matching problem if one dataset has 6-digit GVKEY and another one has GVKEY without leading zero.
```

### Datadate vs fiscal year
- Datadate is the date of fiscal year end
- Fiscal year (fyear)

|Calendar Year |Fiscal Year-end Month |Fiscal Year|
|--------------|----------------------|-----------|
|2019          |January               |2018       |
|2019          |February              |2018       |
|2019          |March                 |2018       |
|2019          |April                 |2018       |
|2019          |May                   |2018       |
|2019          |June                  |2019       |
|2019          |July                  |2019       |
|2019          |August                |2019       |
|2019          |September             |2019       |
|2019          |October               |2019       |
|2019          |November              |2019       |
|2019          |December              |2019       |


```{attention}
Keep in mind that we do not know the accounting information on **datadate**. The accounting numbers are public avaiable after companies release their financial reports.
```
<br>

<div>
<img class="imgshadow" src="https://raw.githubusercontent.com/mk0417/image-lib/master/ff1992.png">
<figcaption class="captionfont">Fama and French. (1992). <i>Journal of Finance</i>.</figcaption>
</div>

<div>
<img class="imgshadow" src="https://raw.githubusercontent.com/mk0417/image-lib/master/sec_deadline1.png">
<figcaption class="captionfont">Source: http://www.sec.gov/about/forms/form10-k.pdf</figcaption>
</div>

<div>
<img class="imgshadow" src="https://raw.githubusercontent.com/mk0417/image-lib/master/sec_deadline2.png">
<figcaption class="captionfont">Source: https://www.investor.gov/introduction-investing/investing-basics/glossary/form-10-k</figcaption>
</div>

### Stock exchange code
<dl>
<lh><dbvar>EXCHG</dbvar></lh>
<dt><varvalue>11</varvalue><dd>NYSE
<dt><varvalue>12</varvalue><dd>AMEX
<dt><varvalue>14</varvalue><dd>NASDAQ
<dt><varvalue>0</varvalue><dd>Subsidiary/Private
<dt><varvalue>19</varvalue><dd>OTC
</dl>

<a class="weblink" href="https://wrds-www.wharton.upenn.edu/documents/1647/Exchange_Codes_by_Code.pdf" target="_blank">See other stock exchange codes here</a>

## Python
- Import packages
```{jupyter-execute}
import pandas as pd
import numpy as np
````

- Import Compustat North America raw data
```{jupyter-execute}
url = 'https://www.dropbox.com/s/qro99n7ngq0aztr/funda_raw.txt?dl=1'
funda_raw = pd.read_csv(url, sep='\t', low_memory=False)

# View first 5 rows and first 5 columns
funda_raw.iloc[:5, :5]
```

```{jupyter-execute}
# Data types
funda_raw.info()
```

```{jupyter-execute}
# Read the data again with consideration of the data type of gvkey
funda_raw = pd.read_csv(url, sep='\t', low_memory=False, dtype={'gvkey': str})

# View first 5 rows and first 5 columns
funda_raw.iloc[:5, :5]
```

```{jupyter-execute}
# Data types
funda_raw.info()
```

- Clean dataset
```{jupyter-execute}
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
```

**API reference**: <a class="apilink" href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html" target="_blank">pandas.dataframe.sort_values</a>

- Firm-year obs in each stock exchange
```{jupyter-execute}
funda['exchg'].value_counts()
```

- Seasonality of fiscal year end
```{jupyter-execute}
funda['date'] = pd.to_datetime(funda['datadate'], format='%Y%m%d')
funda['month'] = funda['date'].dt.month
funda['month'].value_counts()
```

- ROA and ROE
```{jupyter-execute}
funda['roa'] = funda['ebit'] / funda['at']
funda['roe'] = funda['ebit'] / funda['seq']
```

- Asset growth
    - Generate lagged variables and calculate growth rate
    ```{jupyter-execute}
    funda = funda.sort_values(['gvkey', 'fyear'], ignore_index=True)
    funda['lag_at'] = funda.groupby('gvkey')['at'].shift(1)
    funda['lag_fyear'] = funda.groupby('gvkey')['fyear'].shift(1)
    funda['ag'] = funda['at'] / funda['lag_at'] - 1
    ```
    - Check year gap
    ```{jupyter-execute}
    funda['fyear_diff'] = funda['fyear'] - funda['lag_fyear']
    funda.query('fyear_diff>1')[['gvkey', 'fyear', 'lag_fyear', 'fyear_diff', 'ag']].head()
    ```

    - Deal with gap
    ```{jupyter-execute}
    funda.loc[funda['fyear_diff']>1, 'ag'] = np.nan
    ```

- Summary statistics
```{jupyter-execute}
round(funda[['roa', 'roe', 'ag']].describe(), 3)
```

- Deal with outliers
```{jupyter-execute}
# Winsorising at 1% and 99% percentile
for i in ['roa', 'roe', 'ag']:
    funda['p1'] = funda.groupby('fyear')[i].transform(lambda x: x.quantile(0.01))
    funda['p99'] = funda.groupby('fyear')[i].transform(lambda x: x.quantile(0.99))
    funda.loc[funda[i]<funda['p1'], i] = funda['p1']
    funda.loc[funda[i]>funda['p99'], i] = funda['p99']
    funda = funda.drop(columns=['p1', 'p99'])

round(funda[['roa', 'roe', 'ag']].describe(), 3)
```

## Stata
- Import data from a url
```{code-block} stata
local data_url "https://www.dropbox.com/s/qro99n7ngq0aztr/funda_raw.txt?dl=1"
import delimited "`data_url'", clear
```

- List first five observations
```{code-block} stata
l gvkey datadate at seq ebit in 1/5
```

- Data types
```{code-block} stata
describe
```

- Specify data type when importing data
```{code-block} stata
local data_url "https://www.dropbox.com/s/qro99n7ngq0aztr/funda_raw.txt?dl=1"
import delimited "`data_url'", stringcols(1) clear

describe

l gvkey datadate at seq ebit in 1/5
```

- Keep the most recent one if there are duplicates
```{code-block} stata
sort gvkey fyear datadate

by gvkey fyear: gen id = _n
by gvkey fyear: gen n = _N

keep if id == n
```

- Keep main stock exchanges
```{code-block} stata
keep if exchg==11 | exchg==12 | exchg==14
```

- Drop unnecessary variables
```{code-block} stata
drop indfmt consol popsrc datafmt costat curcd
```

- Drop if total asset and equity are not positive
```{code-block} stata
// Pay attention:
//  missing value (.) is larger than any other values
//  at>0 does not remove missing values
//  seq>0 does not remove missing values
//  This is different from Python

keep if at>0 & seq>0 & at!=. & seq!=.
```

- Firm-year observations in each stock exchange
```{code-block} stata
tab exchg
```

- Seasonality of fiscal year end
```{code-block} stata
tostring datadate, replace
gen date = date(datadate, "YMD")
format date %td

gen month = month(date)

tab month
```

- ROA and ROE
```{code-block} stata
gen roa = ebit / at

gen roe = ebit / seq
```

- Asset growth
```{code-block} stata
sort gvkey fyear

// Generate lagged variables and calculate growth rate
by gvkey: gen lag_at = at[_n-1]
by gvkey: gen lag_fyear = fyear[_n-1]
gen ag = at / lag_at - 1

// Check year gap
gen fyear_diff = fyear - lag_fyear

// Deal with gap
replace ag = . if fyear_diff>1
```

- Summary statistics
```{code-block} stata
summ roa roe ag
```

- Deal with outliers
```{code-block} stata
foreach i of varlist roa roe ag {
	bysort fyear: egen p1 = pctile(`i'), p(1)
	bysort fyear: egen p99 = pctile(`i'), p(99)
	replace `i' = p1 if `i' < p1
	replace `i' = p99 if `i' > p99
	drop p1 p99
}

sort gvkey fyear

summ roa roe ag
```
