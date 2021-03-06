# Class02

## CRSP overview
- Data: security price (and many other trading related data)
- Coverage: US stock exchanges
- Time period: 1925 - present
- Frequency: daily and monthly

### Web access
Downlaod data from CRSP via WRDS web access.
- Dataset: CRSP monthly stock file
- Time period: Jan 2011 to Dec 2020
- Search the entire database
- Variables
    - shrcd
    - exchcd
    - siccd
    - prc
    - ret
    - shrout
    - cfacpr
    - permco
    - cusip
    - ncusip
- Output format
    - Tab-delimited text
    - Uncompressed
    - Date format: YYMMDDn8

### Identifiers
<dl>
<dt><dbvar>PERMNO</dbvar>
<dd>CRSP permanent security level identifier
<dd>They are permanent and never change
<dt><dbvar>PERMCO</dbvar>
<dd>CRSP permanent firm level identifier
<dd>One <dbvar>PERMCO</dbvar> might have different <dbvar>PERMNO</dbvar> because a company can issue different securities. For example, Alphabet (Google) has class A and class C shares.
<dd>They are permanent and never change
<dt><dbvar>CUSIP</dbvar>
<dd>Current 8-digit <dbvar>CUSIP</dbvar> (security level)
<dd>They can be changed. And we can use <dbvar>NCUSIP</dbvar> to track the change history.
<dt><dbvar>NCUSIP</dbvar><dd>Historical 8-digit <dbvar>CUSIP</dbvar> (security level)
</dl>

```{note}
<dbvar>TICKER</dbvar> and company name (<dbvar>COMNAM</dbvar>) are also available identifiers in CRSP. However, we usually do not use them to match stocks/firms unless we have no other widely used identifiers.
```

### Stock exchange code
<dl>
<lh><dbvar>EXCHCD</dbvar></lh>
<dt><varvalue>1</varvalue><dd>NYSE
<dt><varvalue>2</varvalue><dd>AMEX
<dt><varvalue>3</varvalue><dd>NASDAQ
</dl>

<div>
<img class="imgshadow" src="https://raw.githubusercontent.com/mk0417/image-lib/master/cnw2021.png">
<figcaption class="captionfont">Chinco, Neuhierl and Weber. (2021). <i>Journal of Financial Economics</i>.</figcaption>
</div>

<div>
<img class="imgshadow" src="https://raw.githubusercontent.com/mk0417/image-lib/master/ls2000.png">
<figcaption class="captionfont">Lee and Swaminathan. (2000). <i>Journal of Finance</i>.</figcaption>
</div>

<a class="weblink" href="https://wrds-www.wharton.upenn.edu/data-dictionary/crsp_a_stock/msenames/exchcd/" target="_blank">See other stock exchange codes here</a>

### Share code
<dl>
<lh><dbvar>SHRCD</dbvar></lh>
<dt><varvalue>10</varvalue> or <varvalue>11</varvalue><dd>Common stocks
</dl>

<div>
<img class="imgshadow" src="https://raw.githubusercontent.com/mk0417/image-lib/master/ads2016.png">
<figcaption class="captionfont">Antoniou, Doukas and Subrahmanyam. (2016). <i>Management Science</i>.</figcaption>
</div>

<div>
<img class="imgshadow" src="https://raw.githubusercontent.com/mk0417/image-lib/master/hhhz.png">
<figcaption class="captionfont">Han, Huang, Huang and Zhou. (forthcoming). <i>Journal of Financial Economics</i>.</figcaption>
</div>

<a class="weblink" href="https://wrds-www.wharton.upenn.edu/data-dictionary/crsp_a_stock/msenames/shrcd/" target="_blank">See other share codes here</a>

### Stock price
<dl>
<dt><dbvar>PRC</dbvar>
<dd>Stock price (unadjusted)
<dd>Some stock prices have negative sign (-)
<dd>Need to take absolute value of price
</dl>

- $\text{adjusted price} = \frac{\left|prc\right|}{cfacpr}$
- It is important to adjust stock price when evaluating stock performance

Take the example of Microsoft stock price. The vertical red lines indicate corporate actions (e.g. stock splits, dividends). Clearly, the stock return is not correct if unadjusted price is applied.
![](https://raw.githubusercontent.com/mk0417/image-lib/master/adjprc.png)

```{note}
<dbvar>RET</dbvar> (stock return) in CRSP is already adjusted. You can download it and there is no need to do any adjustment.
```

### Market value
$\text{market value (millions)} = \frac{|prc| \times shrout}{1000}$

<dl>
<dt><dbvar>SHROUT</dbvar><dd>number of shares outstanding (in 1,000 shares)
</dl>

### Volume
<dl>
<dt><dbvar>VOL</dbvar>
<dd>Number of traded shares
<dd>1 share in Daily Stock File
<dd>100 shares in Monthly Stock File
</dl>

## Python
- Import packages
```{jupyter-execute}
import pandas as pd
import numpy as np
```

- Import CRSP raw data
    - Import data from local directory
    ```{code-block} python
    # Please make sure to change the path to where you save your data
    file_path = '/Users/ml/Dropbox/teaching/data/crsp_month_raw.txt'
    crsp_raw = pd.read_csv(file_path, sep='\t', low_memory=False)

    # View first 5 rows
    # crsp_raw.head()
    ````

    - Import data from a url
    ```{jupyter-execute}
    # This url contains sample data from CRSP
    url = 'https://www.dropbox.com/s/6mk86g97uji2f80/crsp_month_raw.txt?dl=1'
    crsp_raw = pd.read_csv(url, sep='\t', low_memory=False)

    # View first 5 rows and first 5 columns
    crsp_raw.iloc[:5, :5]
    ````

    **API reference**: <a class="apilink" href="https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html" target="_blank">pandas.read_csv</a>

    <br>

    ```{attention}
    **Comments**
    - Any lines starting with `#` will be treated as comments and Python will not execute the lines.
        - This is useful when you need to write some comments or notes

    **Folder path and operating system**
    - Use **pathlib** library is a better solution if you want to run your codes without problem on different operating systems.
        - Import the package: `from pathlib import Path`
    - MacOS (Linux)
        - Forward slash: **/folder/file.txt**
    - Windows
        - Backslash: **C:\folder\file.txt**
        - Please use double slashes when typing path: `C:\\folder\\file.txt`
    - <a class="weblink" href="https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f" target="_blank">Check the folder path tips</a>
    ```

- Data dimension
```{jupyter-execute}
# Observations
len(crsp_raw)
```

```{jupyter-execute}
# Number of rows and columns (variables)
crsp_raw.shape
```

- Data type
```{jupyter-execute}
# List all variables in the dataset
crsp_raw.columns
```

```{jupyter-execute}
# Data type of variables
crsp_raw.dtypes

crsp_raw.info()
```

```{jupyter-execute}
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
```

- Stock exchanges and common shares
```{jupyter-execute}
crsp = crsp_raw.copy()

# Keep NYSE/AMEX/NASDAQ
crsp = crsp[crsp['exchcd'].isin([1, 2, 3])]

# Keep common shares
crsp = crsp[crsp['shrcd'].isin([10, 11])]

# Convert shrcd and exchcd to int
crsp[['exchcd', 'shrcd']] = crsp[['exchcd', 'shrcd']].astype(int)

len(crsp)
```

- Drop duplicates
It is a good practice to check if there are duplicated observations.
```{jupyter-execute}
crsp = crsp.drop_duplicates(['permno', 'date'])
len(crsp)
```

**API reference**: <a class="apilink" href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html" target="_blank">pandas.dataframe.drop_duplicates</a>

<br>

```{tip}
Categorical data is a good way to reduce the memory usage especially when the data eats up too much your computer memory.
```

```{jupyter-execute}
temp = crsp.copy()
# Convert shrcd and exchcd to category
temp[['exchcd', 'shrcd']] = temp[['exchcd', 'shrcd']].astype('category')
temp.info()
```

**!!!** 38M vs. 80M

- Save data
```{code-block} python
# Remember to change the file path on your machine
outpath = '/Users/ml/Dropbox/teaching/data/crsp_month.txt'
crsp.to_csv(outpath, sep='\t', index=False)
```

**API reference**: <a class="apilink" href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html" target="_blank">pandas.dataframe.to_csv</a>

- Read clean data
```{jupyter-execute}
# If you want to import from local
# file_path = '/Users/ml/Dropbox/teaching/data/crsp_month.txt'
# crsp = pd.read_csv(file_path, sep='\t', parse_dates=['date'])

# Import from url
url = 'https://www.dropbox.com/s/0nuxwo3cf7vfcy3/crsp_month.txt?dl=1'
crsp = pd.read_csv(url, sep='\t', parse_dates=['date'])
```

- Generate new variables
```{jupyter-execute}
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
```

**API reference**: <a class="apilink" href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html" target="_blank">pandas.dataframe.loc</a>

**API reference**: <a class="apilink" href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html" target="_blank">pandas.dataframe.query</a>

<br>

```{attention}
Pay attention to month gaps when we use information over multiple periods. Your calculation might be right but data might not be always perfect. Do we have past 6-month data when we compute past 6-month returns?
```
```{jupyter-execute}
temp1[['permno', 'yyyymm', 'midx', 'midx_lag', 'gap', 'ret', 'hpr']]
```

```{jupyter-execute}
temp2[['permno', 'yyyymm', 'midx', 'midx_lag', 'gap', 'ret', 'hpr']]
```

Alternative way is to fill the gaps and assume the returns during the gaps are 0. This will keep more valid cumulative returns.

- Summary statistics
```{jupyter-execute}
crsp[['ret', 'lnme']].describe()
```

```{jupyter-execute}
# Percentiles
crsp[['ret', 'lnme']].describe(percentiles=[0.1, 0.9])
```

```{jupyter-execute}
# Summary statistics by year
crsp['year'] = crsp['date'].dt.year
round(crsp.groupby('year')[['ret', 'lnme']].describe()
.loc[:, (slice(None), ['mean', '50%', 'std'])], 4)
```

```{jupyter-execute}
# Summary statistics by stock exchange
round(crsp.groupby('exchcd')[['ret', 'lnme']].describe()
.loc[:, (slice(None), ['mean', '50%', 'std'])], 4)
```

```{jupyter-execute}
# Summary statistics in subsamples
print('Before 2015')
print(crsp.query('year<=2015')[['ret', 'lnme']].describe())
print('\nAfter 2015')
print(crsp.query('year>=2016')[['ret', 'lnme']].describe())
```

**API reference**: <a class="apilink" href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html" target="_blank">pandas.dataframe.describe</a>

## Stata
- Import CRSP raw data
    - Import data from a url
    ```{code-block} stata
    local repo_url "https://raw.githubusercontent.com/mk0417/financial-database"
    local data_url "/master/data/crsp_demo.txt"
    local url = "`repo_url'" + "`data_url'"
    import delimited "`url'", clear
    ```

    - Import data from local directory
    ```{code-block} stata
    clear
    set more off

    cd "/Users/ml/Dropbox/teaching/data/"

    import delimited crsp_month_raw.txt, clear

    // list first five observations
    l permno date shrcd exchcd ret in 1/5
    ```

    ```{code-block} stata-output
       +------------------------------------------------+
       | permno       date   shrcd   exchcd         ret |
       |------------------------------------------------|
    1. |  10026   20201231      11        3    0.072598 |
    2. |  10028   20201231      11        2    0.125541 |
    3. |  10032   20201231      11        3    0.046848 |
    4. |  10044   20201231      11        3   -0.051522 |
    5. |  10051   20201231      11        1   -0.030851 |
       +------------------------------------------------+
    ```

- Data dimension
```{code-block} stata
// Number of observations
count
di _N
```

- Data type
```{code-block} stata
describe
```

```{code-block} stata-output
Contains data
  obs:       870,692
 vars:            12
-------------------------------------------------------------------------------
              storage   display    value
variable name   type    format     label      variable label
-------------------------------------------------------------------------------
permno          long    %12.0g                PERMNO
date            long    %12.0g
shrcd           byte    %8.0g                 SHRCD
exchcd          byte    %8.0g                 EXCHCD
siccd           str4    %9s                   SICCD
ncusip          str8    %9s                   NCUSIP
permco          long    %12.0g                PERMCO
cusip           str8    %9s                   CUSIP
prc             float   %9.0g                 PRC
ret             str9    %9s                   RET
shrout          long    %12.0g                SHROUT
cfacpr          float   %9.0g                 CFACPR
-------------------------------------------------------------------------------
Sorted by:
     Note: Dataset has changed since last saved.
```

```{code-block} stata
// Convert date to date format
tostring date, replace
gen date1 = date(date, "YMD")

l permno date date1 ret in 1/5
```

```{code-block} stata-output
     +-------------------------------------------+
     | permno       date       date1         ret |
     |-------------------------------------------|
  1. |  10001   20110131   31jan2011    0.028992 |
  2. |  10001   20110228   28feb2011    0.022727 |
  3. |  10001   20110331   31mar2011    0.072404 |
  4. |  10001   20110429   29apr2011   -0.038789 |
  5. |  10001   20110531   31may2011    0.028050 |
     +-------------------------------------------+
```

```{code-block} stata
// Convert ret to numerical
gen ret1 = real(ret)
drop ret
rename ret1 ret

// Convert siccd to numerical
gen siccd1 = real(siccd)
drop siccd
rename siccd1 siccd

describe
```

```{code-block} stata-output
Contains data
  obs:       870,692
 vars:            13
-------------------------------------------------------------------------------
              storage   display    value
variable name   type    format     label      variable label
-------------------------------------------------------------------------------
permno          long    %12.0g                PERMNO
date            str8    %9s
shrcd           byte    %8.0g                 SHRCD
exchcd          byte    %8.0g                 EXCHCD
ncusip          str8    %9s                   NCUSIP
permco          long    %12.0g                PERMCO
cusip           str8    %9s                   CUSIP
prc             float   %9.0g                 PRC
shrout          long    %12.0g                SHROUT
cfacpr          float   %9.0g                 CFACPR
date1           float   %td
ret             float   %9.0g
siccd           float   %9.0g
-------------------------------------------------------------------------------
Sorted by:
     Note: Dataset has changed since last saved.
```

- Stock exchanges and common shares
```{code-block} stata
// Keep NYSE/AMEX/NASDAQ
keep if inlist(exchcd, 1, 2, 3)
* Equivalently,
* keep if exchcd==1 | exchcd==2 | exchcd==3

// Keep common shares
keep if inlist(shrcd, 10, 11)
* Equivalently
* keep if shrcd==10 | shrcd==11
```

- Drop duplicates
```{code-block} stata
duplicates drop permno date, force
```

- Save data
```{code-block} stata
save crsp_month, replace
```

- Read clean data
```{code-block} stata
use crsp_month, clear
```

- Generate new variables
```{code-block} stata
// Market value
gen price = abs(prc)
gen me = (price*shrout) / 1000
gen lnme = ln(me)

// Adjusted price
gen adjprc = price / cfacpr

// Holding period return
gen yyyymm = mofd(date1)
format yyyymm %tm

gen logret = ln(1+ret)

sort permno yyyymm

forvalues i=1/5 {
	by permno: gen l`i' = logret[_n-`i']
}

gen hpr = logret+l1+l2+l3+l4+l5

by permno: gen yyyymm_lag = yyyymm[_n-5]
format yyyymm_lag %tm
gen gap = yyyymm - yyyymm_lag

replace hpr = . if gap!=5

replace hpr = exp(hpr) - 1
```

- Summary statistics
```{code-block} stata
summ ret lnme

summ ret lnme, d

// Summary statistics by year
gen year = year(date1)

tabstat ret lnme, by(year) stat(mean p50 sd) long

tabstat ret lnme, by(year) stat(mean p50 sd) long nototal

tabstat ret lnme, by(year) stat(mean p50 sd) long nototal col(stat)

// Summary statistics by stock exchange
tabstat ret lnme, by(exchcd) stat(mean p50 sd) long nototal col(stat)

// Summary statistics in subsamples
summ ret lnme if year<=2015

summ ret lnme if year>2015
```
