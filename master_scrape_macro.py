# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 23:03:57 2022

@author: kentj
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
from time import sleep
from random import randint
import datetime
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
s = Service(r'C:\Users\kentj\Desktop\scrape\chromedriver.exe')
driver = webdriver.Chrome(service=s)
import time
import glob
import os
from datetime import date
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


this_next = ['this']

time_period = [] 
date = [] 
announcement_time = [] 
currency = [] 
event_title = [] 
actual = [] 
forecast = [] 
previous = [] 

for company in tqdm(this_next):
    #driver.maximize_window()
    driver.get("https://www.forexfactory.com/calendar?month=" + str(company))
    time.sleep(3)  # Allow 2 seconds for the web page to open

    for i in range(0,3):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(2)
            
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    date_list = soup.find_all('td', class_ = 'calendar__cell calendar__date date')
    
    calender_time = soup.find_all('td', class_ = 'calendar__cell calendar__time time')
    
    currency_list = soup.find_all('td', class_= 'calendar__cell calendar__currency currency')
    
    event_list = soup.find_all('span', class_ = 'calendar__event-title')
    
    actual_list = soup.find_all('td', class_ = 'calendar__cell calendar__actual actual')
    
    forecast_list = soup.find_all('td', class_ = 'calendar__cell calendar__forecast forecast')
    
    previous_list = soup.find_all('td', class_ = 'calendar__cell calendar__previous previous')
    
for a in date_list:
    date.append(a.text)
    
for b in calender_time:
    announcement_time.append(b.text)
    
for c in currency_list:
    currency.append(c.text)

for d in event_list:
    event_title.append(d.text)
    
for e in actual_list:
    actual.append(e.text)
    
for f in forecast_list:
    forecast.append(f.text)    
    
for g in previous_list:
    previous.append(g.text)  
    
df_macro_news = pd.DataFrame({
'date': date,
'announcement_time': announcement_time,
'currency': currency,
'event_title': event_title,
'previous': previous,   
'forecast': forecast,
'actual': actual,
'current_time': datetime.now()    
})

df_macro_news['date'] = df_macro_news['date'].str[4:]
df_macro_news['announcement_time'] = df_macro_news['announcement_time'].str.replace("\n", "")
df_macro_news['currency'] = df_macro_news['currency'].str.replace("\n", "")

import pygsheets

gc = pygsheets.authorize(service_file= r'C:\Users\kentj\Desktop\scrape\amazon scrape\principal-iris-338314-cb4e85371557.json') # authorize

output = gc.open('Yahoo Finance')

df_macro = output[6]

df_macro.set_dataframe(df_macro_news,(1,1))