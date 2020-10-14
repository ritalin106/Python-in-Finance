#!/usr/bin/env python
# coding: utf-8

# # Data Acquisition

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

