#!/usr/bin/env python
# coding: utf-8

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

def parse(r):
    if r.status_code == 200:
        print('Successfully scraped {}'.format(r.url))
        return BeautifulSoup(r.content, "html.parser")
    else:
        print('Error Code: ' + str(r.status_code))

def scrape_url(link):
    r = requests.get(link)
    return parse(r)

raw = scrape_url(url)

for loc in raw.select('url > loc'):
    if re.search(r'coronavirus-2019-covid-19-di-malaysia/$', loc.text.strip()):
        links.append(loc.text)

maindf = []
appended_data = []

def make_task():
    for i in tqdm(links):
        df = pd.read_html(i, header=0, flavor='lxml')
        for dfs in df:
            if (dfs.columns[0].strip().lower()) in keyword:
                df2 = dfs
                appended_data.append(df2)
    return pd.concat(appended_data)

result = make_task()
result.dropna(subset=['Negeri', 'Jantina (Warganegara)',
                      'Hospital / Tempat Kematian', 'Latar Belakang Penyakit'])
