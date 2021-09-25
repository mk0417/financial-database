# Class01

## Introduction to WRDS
### History
- Constructed by Wharton in **1993**
- Written by SAS
- To facilitate data collection and data analysis for finance research
- First academic subscriber: **Stanford University**

### Development
- WRDS cloud and Postgres connection are developed over past few years
- More than **350TB** data
- Over **500** subscribers

### WRDS access
- Register WRDS account
    1. Go to <a class="weblink" href="https://wrds-www.wharton.upenn.edu/">WRDS</a>
    2. Click **REGISTER** on top right
    3. Fill registration form and then submit

- Access methods
    - Web interface
    - WRDS cloud (SSH)
    - Computer language/software (Python, R, SAS, Stata)

## Introduction to Python
### Install Anaconda
1. Go to <a class="weblink" href="https://www.anaconda.com/products/individual">Anaconda</a>
2. Scroll down to find the installation files

![](https://raw.githubusercontent.com/mk0417/image-lib/master/anaconda.png)

Choose the operating system (Linux/MacOS/Windows) and make sure to download the **64-bit Graphical Installer**
3. Double click the installation file and follow the wizard to complete the installation

```{seealso}
Anaconda installation tutorial <a class="weblink" href="https://www.youtube.com/watch?v=_hsPV5ZZoJo">Youtube video from <b>Ties</b></a>
```

### Python editors
#### Jupyter Notebook
1. Open your terminal (MacOS) or start Anaconda prompt (Windows), then type in `jupyter lab`. This will open notebook in your default web browser.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/jupyter1.png)

2\. Click Python3

![](https://raw.githubusercontent.com/mk0417/image-lib/master/jupyter2.png)

3\. Type in `print('This is Python')` in the first cell and press <kbd>shift</kbd> + <kbd>enter</kbd> (this is the keyboard shortcut to run the code in that cell). The string will be printed out below. In the second cell, let's write mutiple lines code and run it. In the example below, 2 will be printed.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/jupyter3.png)

#### VSCode
There are many other ways to execute Python code. VSCode is a very popular one.
1\. Visit <a class="weblink" href="https://code.visualstudio.com/">VSCode</a> to download installation file and install it.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode1.png)

2\. Start VSCode and click the icon on the left bar as indicated below

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode2.png)

3\. You will find Python extension and click **install**.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode3.png)

4\. Please type in `python` in the search bar if you cannot see the extension.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode4.png)

5\. <kbd>cmd</kbd>+<kbd>n</kbd> (MacOS) or <kbd>alt</kbd>+<kbd>n</kbd> (Windows) to create a new file, type in `print('This is Python')` and save the file with the extension of **.py**.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode5.png)

6\. Check if you have the Anaconda version of Python at left bottom corner. Just click it if you are not sure the Python version. Choose the Python version with anaconda path.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode6.png)

7\. <kbd>cmd</kbd>+<kbd>shift</kbd>+<kbd>p</kbd> (MacOS) or <kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>p</kbd> to open command palette. Type in `setting` and click **Preferences: Open Setting (UI)**.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode7.png)

8\. Type in `send selection` in the search on top and make sure **Jupyter: Send Selection to Interactive Window** is ticked.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode8.png)

9\. Move your cursor anythere in the fisrt line and press <kbd>shift</kbd>+<kbd>enter</kbd>, then an interactive window will be pop up on the right and the result will be printed there. For multiple line code, just select all the codes first and then press <kbd>shift</kbd>+<kbd>enter</kbd> to run the selection. You will see the results on the right.

![](https://raw.githubusercontent.com/mk0417/image-lib/master/vscode9.png)

#### Other editors
- **Spyder**. This is included in Anaconda distribution (<a class="weblink" href="https://www.youtube.com/watch?v=E2Dap5SfXkIYoutube">video tutorial</a>)
- **Vim** (an article <a class="weblink" href="https://www.fullstackpython.com/vim.html">how to build a Python IDE in **Vim**</a>)
- **Emacs** (an article <a class="weblink" href="https://realpython.com/emacs-the-best-python-editor/">how to configure a Python environment in **Emacs**</a>; <a class="weblink" href="https://github.com/hlissner/doom-emacs">**Doom Emacs** is an out-of-box configuration</a>)

```{note}
There is a learning curve to use **Emacs** and **Vim** if you have no previous experience. Therefore, have a try only if you are interested in **Emacs** and **Vim**. Both of them have unique features to make your empirical research more productive. You can also see my **Emacs** configuration (<a class="weblink" href="https://github.com/mk0417/.emacs.d">.emacs.d</a>).

I use **Emacs** to do all my empirical research.
```

### Retrieve WRDS data
WRDS provides Python package **wrds** to make our life much easier to download data from WRDS (the package is kind of wrapper of postgres connction to WRDS).

- Import required packages
```{code-block} python
import wrds
import pandas as pd
```

- Connect to WRDS
```{code-block} python
conn = wrds.Connection()
```
After you run it, type in your WRDS username and press <kbd>enter</kbd>; type in your WRDS password and press <kbd>enter</kbd>

- List databases
```{code-block} python
lib = conn.list_libraries()
# view first 3 databases
lib[:3]
```

- List tables
```{code-block} python
# get tables from CRSP database
table = conn.list_tables('crsp')
# view first 3 tables
table[:3]
```

- Describe tables
```{code-block} python
# list variables in monthly stock file (msf) from CRSP
conn.describe_table('crsp', 'msf')
```

- Extract data
```{code-block} python
msf = conn.raw_sql("""
    select permno, date, ret
    from crsp.msf
    where date>='01/01/2020' and date<='05/31/2020'
""")

# list first 5 observations
msf.head()
```

<dl class="defsection">
<lh class="deftitle">SQL syntax</lh>
<dt><cmd>select</cmd><dd>claim which variables you want to download and seprate them by comma (,)
<dt><cmd>from</cmd><dd>declare which table the variables are from
<dt><cmd>where</cmd><dd>conditional statement (like a filter)
</dl>

```{seealso}
Learn more SQL from <a class="weblink" href="https://www.postgresqltutorial.com/">PostgreSQL tutorial</a>
```

