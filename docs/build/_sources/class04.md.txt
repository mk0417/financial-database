# Class04

## Datastream
### Overview
- Another important data platform for accounting and finance research
- Useful for international research
- A product offered by Refinitiv (formerly known as Thomson Reuters)

### Access
#### Where to find Eikon terminal
- Terminal in CASIF office
- Bloomberg trading room (LUBS Room 1.30)

#### How to login
1\. Open Excel

2\. Click **REFINITIV EIKON**

3\. Click **Sign In**

![](https://raw.githubusercontent.com/mk0417/image-lib/master/ds_login.png)

4\. **Online** means successful login

![](https://raw.githubusercontent.com/mk0417/image-lib/master/ds_online.png)

5\. Click **REFINITIV EIKON DATASTREAM**

![](https://raw.githubusercontent.com/mk0417/image-lib/master/ds_datastream.png)

### Company list
#### How to screen company list

|Name         |DS symbol |CUSIP     |ISIN         |Primary |Major |Exchange  |
|-------------|----------|----------|-------------|--------|------|----------|
|ALPHABET INC |@GOOGL    |02079K305 |US02079K3059 |P       |Y     |Nasdaq    |
|ALPHABET INC |D:ABEA    |02079K305 |US02079K3059 |S       |Y     |Frankfurt |
|ALPHABET INC |0RIH      |02079K305 |US02079K3059 |S       |Y     |London    |
|ALPHABET INC |@GOOG     |02079K107 |US02079K3059 |P       |N     |Nasdaq    |

<dbvar>Primary</dbvar> = <varvalue>P</varvalue> and <dbvar>Major</dbvar> = <varvalue>Y</varvalue>
will keep the firm below:

|Name         |DS symbol |CUSIP     |ISIN         |Primary |Major |Exchange |
|-------------|----------|----------|-------------|--------|------|---------|
|ALPHABET INC |@GOOGL    |02079K305 |US02079K3059 |P       |Y     |Nasdaq   |

<dl>
<dt><dbvar>Primary</dbvar>
<dd>ISINID returns either P or S where P indicates that the equity record is the primary one (i.e.,
the domestic listing of the share or depository receipt or certificate), and where S indicates that
the equity record is secondary (i.e., a foreign listing of a share or depository receipt or certificate).
</dl>

<dl>
<dt><dbvar>Major</dbvar>
<dd>For companies with more than one equity Security MAJOR returns Y (yes) or N (no) to indicate
which of the securities is the most significant in terms of market value and liquidity of the
primary quotation of that security. Only one security per company is assigned as the major, and all
quotations of that security will return a Y value. All quotations of other securities will return
N. For Companies with only one equity security, all the quotations of that security will return Y.
</dl>

#### Company list from other database
You are able to use your own list if you have firm list from some other databases (for example, you
may have a list from Compustat). Acceptable identifiers include:
- CUSIP. Please remember to add leading **U**, e.g. U02079K305
- ISIN
- IBES ticker

### Static data
- Example: company identifiers

### Time series data
- Example: stock price

Stock price of Tesco

|date           |P         |P#S    |
|---------------|----------|-------|
|12/20/2021     |287.6     |287.6  |
|12/21/2021     |288.5     |288.5  |
|12/22/2021     |287.55    |287.55 |
|12/23/2021     |288.35    |288.35 |
|12/24/2021     |287.9     |287.9  |
|**12/27/2021** |**287.9** |**NA** |
|**12/28/2021** |**287.9** |**NA** |
|12/29/2021     |291.05    |291.05 |
|12/30/2021     |291.25    |291.25 |
|12/31/2021     |289.9     |289.9  |

27 Dec 2021 and 28 Dec 2021 are non-trading days (holidays) in UK. The price will repeat last
availabe price on holidays if you choose <dbvar>P</dbvar> to download stock price. You can use
<dbvar>P#S</dbvar> to avoid this.


```{seealso}
You can read this article to get better understanding of the difference
<a class="weblink" href="https://bizlib247.wordpress.com/2012/04/13/datastream-price-variables-p-ps-pt/" target="_blank">Datastream – Price variables</a>
```

### Data format
- Data from Datastream is not panel data format

![](https://raw.githubusercontent.com/mk0417/image-lib/master/ds_data.png)

- We need to transpose data from wide to long before we analyse the data

Let's assume we have stock price data for two firms.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/wide_to_long.png)

## Python
- Read firm assets from Datastream
```{jupyter-execute}
import pandas as pd
import numpy as np

url = 'https://www.dropbox.com/s/3x230qb3fkopij3/datastream_asset.xlsx?dl=1'
asset = pd.read_excel(url, sheet_name='asset')
```

- Transpose data
```{jupyter-execute}
asset = pd.melt(asset, id_vars='Code', value_vars=asset.columns[1:],
    value_name='asset')
asset['isin'] = asset['variable'].str[:12]
asset = asset[['isin','Code','asset']]
asset = asset.rename(columns={'Code': 'year'})
asset.head()
```

## Stata
- Read firm assets from Datastream
```{code-block} stata
/* Import firm total asset */
local data_url "https://www.dropbox.com/s/3x230qb3fkopij3/datastream_asset.xlsx?dl=1"
import excel using "`data_url'", sheet("asset") first clear

/* Rename variables */
rename Code year

rename US* assetUS*

/* Convert data type */
destring, replace ignore("NA")
```

- Transpose data
```{code-block} stata
/* Reshape wide to long */
reshape long asset, i(year) j(isin) string

/* Extract ISIN */
replace isin = substr(isin, 1, 12)
```
