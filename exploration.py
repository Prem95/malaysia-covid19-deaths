#!/usr/bin/env python
# coding: utf-8

# ## Import basic libraries

# In[17]:


"""
@author: Prem Kumar
@date: 07/06/2021
"""
from bs4 import BeautifulSoup
import re
import pandas as pd
import lxml
import requests
from datetime import date
import time
from tqdm import tqdm

url = 'https://kpkesihatan.com/sitemap.xml'
links = []
keyword = ['no. kematian', 'kes kematian', 'kes no. kematian', 'kes']


# ## Scrape the link from the main url

# In[5]:


def parse(r):
    if r.status_code==200:
        print('Successfully scraped {}'.format(r.url))
        return BeautifulSoup(r.content, "html.parser")
    else:
        print('Error Code: '+ str(r.status_code))


# In[6]:


def scrape_url(link):
    r = requests.get(link)
    return parse(r)    


# In[7]:


raw = scrape_url(url)


# In[8]:


for loc in raw.select('url > loc'):
    if re.search(r'coronavirus-2019-covid-19-di-malaysia/$', loc.text.strip()):
        links.append(loc.text)


# In[9]:


maindf = []
appended_data = []


# ## Read the parsed html and append to the a dataframe

# In[11]:


def make_task():
    for i in tqdm(links):
        df = pd.read_html(i, header = 0, flavor = 'lxml')
        for dfs in df:
            if (dfs.columns[0].strip().lower()) in keyword:
                df2 = dfs
                appended_data.append(df2)
    return pd.concat(appended_data)


# In[12]:


result = make_task()


# In[16]:


result.dropna(subset=['Negeri', 'Jantina (Warganegara)', 'Hospital / Tempat Kematian', 'Latar Belakang Penyakit'])


# In[ ]:




