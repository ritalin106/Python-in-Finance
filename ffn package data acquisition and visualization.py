#!/usr/bin/env python
# coding: utf-8
Data Acquisition
# In[ ]:


get_ipython().system('pip install ffn')
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import ffn

portfolio = ffn.get("2330.tw, 2317.tw, 2891.tw", start = "2019-01-01")


# In[ ]:


portfolio.plot(grid = True)


# In[ ]:


portfolio.rebase().plot(grid = True)


# In[ ]:


return_rates = portfolio.diff() / portfolio * 100


# In[ ]:


return_rates.plot(grid = True)


# In[ ]:


return_rates.plot.hist(alpha = 0.4, grid = True)


# Statistics Summary

# In[ ]:


analysis = portfolio.calc_stats()
analysis.display()


# In[ ]:


analysis["2330tw"].plot_histogram()

Correlation
# In[ ]:


portfolio.corr()


# In[ ]:


portfolio.plot_corr_heatmap()

Signal generation
# In[ ]:


import ffn
from ffn.utils import clean_ticker

target = "2330.tw"
name = clean_ticker(target)
asset = ffn.get(target, start = "2012-01-01")
print(asset)


# In[ ]:


asset["sma5"] = asset[name].rolling(5).mean()
asset["sma10"] = asset[name].rolling(10).mean()

print(asset)


# In[ ]:


buy_signal_mask = (asset["sma5"].shift(2) < asset["sma10"].shift(2)) & (asset["sma5"].shift(1) > asset["sma10"].shift(1))
sell_signal_mask = (asset["sma5"].shift(2) > asset["sma10"].shift(2)) & (asset["sma5"].shift(1) < asset["sma10"].shift(1))


# In[ ]:


print(buy_signal_mask)

Backtesting
# In[ ]:


position = False
asset["PV"] = 0.0
turnovers = 0

for i, t in enumerate(asset.index):
    
    if not position:
        
        payoff = 0
        asset["PV"].iloc[i] = asset["PV"].iloc[i - 1] + payoff
        
        if buy_signal_mask[t]:
            position = True
            turnovers = turnovers + 1
            print(">" * 5, "Create a long position.")
    else:
        
        payoff = asset[name].iloc[i] - asset[name].iloc[i - 1]
        asset["PV"].iloc[i] = asset["PV"].iloc[i - 1] + payoff
       
        if sell_signal_mask[t]:
            position = False
            print("<" * 5, "Close a long position.")
            print("{} -> {:.2f} -> {:.2f}".format(t, asset[name][t], asset["PV"][t]))

print("Number of turnovers:", turnovers)

