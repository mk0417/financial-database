# Class02

## CRSP overview
- Data: security price (and many other trading related data)
- Coverage: US stock exchanges
- Time period: 1925 - present
- Frequency: daily and monthly

### Web access

### Identifiers
<dl>
<dt><dbvar>PERMNO</dbvar>
<dd>CRSP permanent security level identifier
<dd>They are permanent and never change
<dt><dbvar>PERMCO</dbvar>
<dd>CRSP permanent firm level identifier
<dd>One <dbvar>PERMCO</dbvar> might have different <dbvar>PERMNO</dbvar> because a company can issue different securities. For example, Alphabet had class A and class C shares.
<dd>They are permanent and never change
<dt><dbvar>CUSIP</dbvar>
<dd>Current 8-digit <dbvar>CUSIP</dbvar> (security level)
<dd>They can be changed. And we can use <dbvar>NCUSIP</dbvar> to track the change history.
<dt><dbvar>NCUSIP</dbvar><dd>Historical 8-digit <dbvar>CUSIP</dbvar> (security level)
</dl>

```{note}
<dbvar>TICKER</dbvar> and company name (<dbvar>COMN</dbvar>) are also available identifiers in CRSP. However, we usually do not use them to match stocks/firms unless we have no other widely used identifiers.
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
<figcaption class="captionfont">Chinco, Neuhierl and Weber. (2021). <i>Journal of Financeial Economics</i>.</figcaption>
</div>

<div>
<img class="imgshadow" src="https://raw.githubusercontent.com/mk0417/image-lib/master/ls2000.png">
<figcaption class="captionfont">Lee and Swaminathan. (2000). <i>Journal of Finance</i>.</figcaption>
</div>

<a class="weblink" src="https://wrds-www.wharton.upenn.edu/data-dictionary/crsp_a_stock/msenames/exchcd/">See other stock exchange codes here</a>

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

<a class="weblink" src="https://wrds-www.wharton.upenn.edu/data-dictionary/crsp_a_stock/msenames/shrcd/">See other share codes here</a>

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

### Market value (equity)
$\text{market value (millions)} = \frac{|prc| \times shrout}{1000}$

<dbvar>SHROUT</dbvar> is number of share outstanding (in 1,000 shares)

## Python
- Import packages
```{code-block} python
import pandas as pd
import numpy as np
````

- Import CRSP data
    - Import data from a url
    ```{code-block} python
    crsp_raw = pd.read_csv()
    crsp_raw.head()
    ````
    - Import data from local directory
    ```{code-block} python
    crsp_raw = pd.read_csv('change to the path where your save your data')
    crsp_raw.head()
    ````

## Stata
