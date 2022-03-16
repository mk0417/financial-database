# Class07

## Regression

## Python
- Import packages
```{jupyter-execute}
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import statsmodels.api as sm
from linearmodels import PanelOLS
```

- Import data
```{jupyter-execute}
url = 'https://www.dropbox.com/s/uso1u9asqam7rp1/merged.dta?dl=1'
data = pd.read_stata(url)
data['yyyymm'] = data['yyyymm'].astype(int)
data = data.sort_values(['cusip', 'yyyymm'], ignore_index=True)
```

- Prepare regression data
```{jupyter-execute}
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
```

- OLS regression
```{jupyter-execute}
est = sm.OLS(data['ret'], sm.add_constant(data['lag_lnme'])).fit()
est.summary()

# robust standard error
(sm.OLS(data['ret'], sm.add_constant(data['lag_lnme']))
    .fit(cov_type='hc0', use_t=True).summary())
```

- Fitted values and residuals
```{jupyter-execute}
data['a'] = est.params[0]
data['b'] = est.params[1]

data['p_calc'] = data['a'] + data['b']*data['lag_lnme']
data['p_est'] = est.predict()

data['e_calc'] = data['ret'] - data['p_calc']
data['e_est'] = est.resid
```

- Panel regression
```{jupyter-execute}
data1 = data.set_index(['cusip', 'year'])
panel_est = (PanelOLS(data1['ret'], sm.add_constant(data1['lag_lnme']),
    entity_effects=True).fit())
panel_est.summary
```

- Panel regression with robust standard error
```{jupyter-execute}
panel_est = (PanelOLS(data1['ret'], sm.add_constant(data1['lag_lnme']),
    entity_effects=True).fit(cov_type='robust'))
panel_est.summary
```

```{attention}
linearmodels robust standard error is different from Stata robust standard error
```

- Panel regression with clustered standard error
```{jupyter-execute}
panel_est = (PanelOLS(data1['ret'], sm.add_constant(data1['lag_lnme']),
    entity_effects=True) .fit(cov_type='clustered', cluster_entity=True))
panel_est.summary
```

```{attention}
linearmodels clustered entity standard error is the same with Stata robust standard error
```

## Stata
- Import data
```{code-block} stata
local data_url "https://www.dropbox.com/s/uso1u9asqam7rp1/merged.dta?dl=1"
use "`data_url'", clear
```

- Prepare regression data
```{code-block} stata
rename ret ret_str
gen ret = real(ret_str)
drop ret_str

gen year = int(yyyymm/100)

duplicates drop cusip year, force

gen lnme = ln(me)

sort cusip year
by cusip: gen lag_lnme = lnme[_n-1]
by cusip: gen lag_year = year[_n-1]

gen year_diff = year - lag_year

replace lag_lnme = . if year_diff!=1
```

- OLS regression
```{code-block} stata
reg ret lag_lnme

reg ret lag_lnme, robust
```

- Fitted values and residuals
```{code-block} stata
gen a = _b[_cons]
gen b = _b[lag_lnme]

gen y_calc = a + b*lag_lnme
predict y_est

gen e_calc = ret - y_calc
predict e_est, resid
```

- Panel regression
```{code-block} stata
encode cusip, gen(stock_id)
xtset stock_id year

xtreg ret lag_lnme, fe
```

- Panel regression with robust standard error
```{code-block} stata
xtreg ret lag_lnme, fe robust
```
