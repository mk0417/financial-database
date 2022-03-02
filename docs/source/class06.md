# Class06

## Compustat Global overview
- Data
    - Security Daily: stock price
    - Fundamentals Annual (Quarterly): accounting data
- Coverage: global

### Web access
Downlaod data from Compustat Global Security Daily via WRDS web access.
- Dataset: Compustat Global Security Daily
- Time period: 01 Jul 2020 to 31 Dec 2020
- Search the entire database
- Variables
	- iid
	- ajexdi
	- prccd
	- trfd
	- isin
	- tpci
	- fic
	- monthend
	- prirow
- Output format
    - Tab-delimited text
    - Uncompressed
    - Date format: YYMMDDn8

### Identifiers
<dl>
<dt><dbvar>GVKEY</dbvar>
<dd>Permanent firm level identifier
<dt><dbvar>ISIN</dbvar>
<dd>Security level identifier
<dt><dbvar>IID</dbvar>
<dd>Issue ID
</dl>

|GVKEY  |IID |Exchange               |
|-------|----|-----------------------|
|100131 |01W |London Stock Exchange  |
|100131 |02W |Mexican Stock Exchange |
|100131 |03W |Bats Chi-X Europe      |

**GVKEY** + **IID** will identify security, e.g. 10013101W.

### Primary share
<dl>
<dt><dbvar>PRIROW</dbvar>
<dd>Primary share flag
</dl>

|GVKEY  |IID |Exchange               |PRIROW |
|-------|----|-----------------------|-------|
|100131 |01W |London Stock Exchange  |01W    |
|100131 |02W |Mexican Stock Exchange |01W    |
|100131 |03W |Bats Chi-X Europe      |01W    |

**01W** is the primary share.

### Issue type code
<dl>
<lh><dbvar>TPCI</dbvar></lh>
<dt><varvalue>0</varvalue><dd>Common (ordinary) share
</dl>

### Country code
<dl>
<dt><dbvar>FIC</dbvar>
<dd>3-letter country code
</dl>

<a class="weblink" href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3" target="_blank">Check full list of country code</a>

### Stock price
<dl>
<dt><dbvar>PRCCD</dbvar>
<dd>Stock price (unadjusted)
<dd>Need to adjust stock splits and dividends before calculating stock return
<dt><dbvar>AJEXDI</dbvar>
<dd>Adjustment factor
<dt><dbvar>TRFD</dbvar>
<dd>Total return factor
</dl>

- $\text{adjusted price} = \frac{prccd}{cfacpr}\times trfd$

## Python
- Import packages
```{jupyter-execute}
import pandas as pd
import numpy as np
```

- Import Compustat Global data
```{jupyter-execute}
url = 'https://www.dropbox.com/s/484ynn8mzihgj9q/uk.txt?dl=1'
uk = pd.read_csv(url, sep='\t', low_memory=False, dtype={'gvkey': str})
```

- Clean data
```{jupyter-execute}
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
```

- Generate date index
```{jupyter-execute}
date_index = uk.drop_duplicates('datadate')[['datadate']].copy()
date_index = date_index.sort_values('datadate', ignore_index=True)
date_index['date_idx'] = date_index.index + 1
```

- Calculate daily return
```{jupyter-execute}
uk1 = uk.merge(date_index, how='inner', on='datadate')
uk1 = uk1.sort_values(['stkcd', 'datadate'], ignore_index=True)
uk1['ldate_idx'] = uk1.groupby('stkcd')['date_idx'].shift(1)
uk1['lp_adj'] = uk1.groupby('stkcd')['p_adj'].shift(1)
uk1['date_diff'] = uk1['date_idx'] - uk1['ldate_idx']
uk1['ret'] = uk1['p_adj'] / uk1['lp_adj'] - 1

uk1['date_diff'].value_counts()
```

- Treat daily return as missing if there is long gap between two dates
```{jupyter-execute}
uk1['ret'] = np.where(uk1['date_diff']<=3, uk1['ret'], np.nan)
```

- Generate month index
```{jupyter-execute}
uk_month = uk1.query('monthend==1')[['stkcd', 'datadate', 'p_adj']].copy()

uk_month['yyyymm'] = (uk_month['datadate']/100).astype(int)
uk_month['year'] = (uk_month['yyyymm']/100).astype(int)
uk_month['month'] = uk_month['yyyymm'] % 100

uk_month['month_idx'] = (uk_month['year']-2020)*12 + uk_month['month'] - 6
```

- Monthly return
```{jupyter-execute}
uk_month = uk_month.sort_values(['stkcd', 'yyyymm'], ignore_index=True)
uk_month['lmonth_idx'] = uk_month.groupby('stkcd')['month_idx'].shift(1)
uk_month['lp_adj'] = uk_month.groupby('stkcd')['p_adj'].shift(1)
uk_month['month_diff'] = uk_month['month_idx'] - uk_month['lmonth_idx']
uk_month['ret'] = uk_month['p_adj'] / uk_month['lp_adj'] - 1

# Monthly return is missing if month gap is not 1 month
uk_month['ret'] = np.where(uk_month['month_diff']==1, uk_month['ret'], np.nan)
```

## Stata
- Import data
```{code-block} stata
local data_url "https://www.dropbox.com/s/484ynn8mzihgj9q/uk.txt?dl=1"
import delimited "`data_url'", stringcols(1) clear
```

- Clean data
```{code-block} stata
/* Keep common shares */
keep if tpci == "0"

/* Keep primary issue */
keep if iid == prirow

/* fic = GBR */
keep if fic == "GBR"

/* Check duplicates */
duplicates drop gvkey iid datadate, force

/* Adjusted price */
gen p_adj = prccd / ajexdi * trfd

/* Security level id */
gen stkcd = gvkey + iid
order stkcd datadate
```

- Generate date index
```{code-block} stata
preserve
duplicates drop datadate, force
sort datadate
gen date_idx = _n
keep datadate date_idx
save uk_date_idx, replace
restore
```

- Calculate daily return
```{code-block} stata
merge m:1 datadate using uk_date_idx
sort stkcd datadate
bysort stkcd: gen ldate_idx = date_idx[_n-1]
bysort stkcd: gen lp_adj = p_adj[_n-1]
gen date_diff = date_idx - ldate_idx
gen ret = p_adj / lp_adj - 1

tab date_diff
```

```{code-block} stata-output
  date_diff |      Freq.     Percent        Cum.
------------+-----------------------------------
          1 |    192,606       99.99       99.99
          2 |          5        0.00      100.00
          3 |          4        0.00      100.00
          8 |          1        0.00      100.00
------------+-----------------------------------
      Total |    192,616      100.00
```

- Treat daily return as missing if there is long gap between two dates
```{code-block} stata
replace ret = . if date_diff>3

rm uk_date_idx.dta
```

- Generate month index
```{code-block} stata
keep if monthend==1
keep stkcd datadate p_adj

gen yyyymm = int(datadate/100)
gen year = int(yyyymm/100)
gen month = mod(yyyymm, 100)

gen month_idx = (year-2020)*12 + month - 6
```

- Monthly return
```{code-block} stata
sort stkcd yyyymm
bysort stkcd: gen lmonth_idx = month_idx[_n-1]
bysort stkcd: gen lp_adj = p_adj[_n-1]
gen month_diff = month_idx - lmonth_idx
gen ret = p_adj / lp_adj - 1

replace ret = . if month_diff!=1
```
