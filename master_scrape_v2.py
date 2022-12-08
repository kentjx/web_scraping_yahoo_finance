# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 23:03:54 2022

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
import datetime
from tqdm import tqdm
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#s = Service(r'C:\Users\kentj\Desktop\scrape\chromedriver.exe')
#driver = webdriver.Chrome(service=s)
import time
import glob
import os
from datetime import date
from datetime import datetime

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : r'C:\Users\kentj\Desktop\scrape\yahoo scrape\Yahoo News Scrape folder'}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
from selenium.webdriver.common.by import By



faang = ['AAPL', 'AMZN', 'GOOG', 'NFLX', 'META', 'TSLA', 'MSFT', 'SE', 'SHOP', 'SNOW']
faang = sorted(faang)

for i in tqdm(faang):
    #driver.maximize_window()
    driver.get("https://sg.finance.yahoo.com/quote/" +str(i) + "/history?p=" + str(i))
    time.sleep(2)  # Allow 2 seconds for the web page to open


    driver.find_element(By.XPATH, "//span[starts-with(@class, 'C($linkColor) Fz(14px)')]").click()
    driver.find_element(By.XPATH, "//button[starts-with(@class, 'Py(5px) W(45px) Fz(s) C($tertiaryColor) Cur(p) Bd Bdc($seperatorColor) Bgc($lv4BgColor) Bdc($linkColor):h Bdrs(3px)') and contains(., '5Y')]").click()
    #driver.find_element(By.XPATH, "//button[starts-with(@class, ' Bgc($linkColor) Bdrs(3px) Px(20px) Miw(100px) Whs(nw) Fz(s) Fw(500) C(white) Bgc($linkActiveColor):h Bd(0) D(ib) Cur(p) Td(n)  Py(9px) Fl(end)')]").click()
    driver.find_element(By.XPATH, "//a[starts-with(@class, 'Fl(end) Mt(3px) Cur(p)')]").click()
    time.sleep(2)

faang = ['AAPL', 'AMZN', 'GOOG', 'NFLX', 'META', 'TSLA', 'MSFT', 'SE', 'SHOP', 'SNOW']
faang = sorted(faang)

path = r'C:\Users\kentj\Desktop\scrape\yahoo scrape\Yahoo News Scrape folder' # use your path
all_files = glob.glob(path + '\\*.csv')

li = []

for filename, company in tqdm(zip(all_files, faang)):
    
    dataframe = pd.read_csv(filename, index_col=None, header=0)
    dataframe['ticker'] = company
    li.append(dataframe)

df = pd.concat(li, axis=0, ignore_index=True)

filelist = glob.glob(os.path.join(path, "*.csv"))
for f in filelist:
    os.remove(f)

dates = [] 
ticker = [] 
total_revenue = []
gross_profit = [] 
net_income = [] 
ebitda = [] 


for company in tqdm(faang):
    #driver.maximize_window()
    driver.get("https://sg.finance.yahoo.com/quote/" +str(company) + "/financials?p=" + str(company))
    time.sleep(3)  # Allow 2 seconds for the web page to open

    for i in range(0,3):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")

    div = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Tt(u) Bgc($lv1BgColor)')
    div2 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)')
    div3 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Bgc($lv1BgColor)')

    ttm = div[0].text
    n_minus1 = div2[0].text
    n_minus2 = div3[0].text
    n_minus3 = div2[1].text 
    n_minus4 = div3[1].text

    dates.append(ttm)
    dates.append(n_minus1)
    dates.append(n_minus2)
    dates.append(n_minus3)
    dates.append(n_minus4)
    
    ticker.append(str(company))
    ticker.append(str(company))
    ticker.append(str(company))
    ticker.append(str(company))
    ticker.append(str(company))
    
    revenue_div = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)')
    revenue_div2 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)')
    
    ttm_revenue = revenue_div[0].text
    n_minus1_revenue = revenue_div2[0].text
    n_minus2_revenue = revenue_div[1].text
    n_minus3_revenue = revenue_div2[1].text
    n_minus4_revenue = revenue_div[2].text
    
    total_revenue.append(ttm_revenue)
    total_revenue.append(n_minus1_revenue)
    total_revenue.append(n_minus2_revenue)
    total_revenue.append(n_minus3_revenue)
    total_revenue.append(n_minus4_revenue)
    
    ttm_gp = revenue_div[6].text
    n_minus1_gp = revenue_div2[4].text
    n_minus2_gp = revenue_div[7].text
    n_minus3_gp = revenue_div2[5].text
    n_minus4_gp = revenue_div[8].text
    
    gross_profit.append(ttm_gp)
    gross_profit.append(n_minus1_gp)
    gross_profit.append(n_minus2_gp)
    gross_profit.append(n_minus3_gp)
    gross_profit.append(n_minus4_gp)
    
#     if company != 'NFLX':

#         ttm_ni = revenue_div[39].text
#         n_minus1_ni = revenue_div2[26].text
#         n_minus2_ni = revenue_div[40].text
#         n_minus3_ni = revenue_div2[27].text
#         n_minus4_ni =  revenue_div[41].text

#         net_income.append(ttm_ni)
#         net_income.append(n_minus1_ni)
#         net_income.append(n_minus2_ni)
#         net_income.append(n_minus3_ni)
#         net_income.append(n_minus4_ni)

    max_minus19 = len(revenue_div) - 19 
    max_minus20 = len(revenue_div) - 20
    max_minus21 = len(revenue_div) - 21 
    
    max_minus13 = len(revenue_div2) - 13
    max_minus14 = len(revenue_div2) - 14

    ttm_ni = revenue_div[max_minus21].text
    n_minus1_ni = revenue_div2[max_minus14].text
    n_minus2_ni = revenue_div[max_minus20].text
    n_minus3_ni = revenue_div2[max_minus13].text
    n_minus4_ni =  revenue_div[max_minus19].text
    
    net_income.append(ttm_ni)
    net_income.append(n_minus1_ni)
    net_income.append(n_minus2_ni)
    net_income.append(n_minus3_ni)
    net_income.append(n_minus4_ni)

    max_minus1 = len(revenue_div) - 1 
    max_minus2 = len(revenue_div) - 2
    max_minus3 = len(revenue_div) - 3 
    
    maximum_minus1 = len(revenue_div2) - 1 
    maximum_minus2 = len(revenue_div2) - 2 
    
    ttm_ebitda =  revenue_div[max_minus3].text
    n_minus1_ebitda = revenue_div2[maximum_minus2].text
    n_minus2_ebitda = revenue_div[max_minus2].text
    n_minus3_ebitda = revenue_div2[maximum_minus1].text
    n_minus4_ebitda =  revenue_div[max_minus1].text

    ebitda.append(ttm_ebitda)
    ebitda.append(n_minus1_ebitda)
    ebitda.append(n_minus2_ebitda)
    ebitda.append(n_minus3_ebitda)
    ebitda.append(n_minus4_ebitda)
    
    time.sleep(2)
        
#     else: 
        
#         ttm_ni =  revenue_div[36].text
#         n_minus1_ni = revenue_div2[24].text
#         n_minus2_ni = revenue_div[37].text
#         n_minus3_ni = revenue_div2[25].text
#         n_minus4_ni =  revenue_div[38].text

#         net_income.append(ttm_ni)
#         net_income.append(n_minus1_ni)
#         net_income.append(n_minus2_ni)
#         net_income.append(n_minus3_ni)
#         net_income.append(n_minus4_ni)

#         ttm_ebitda =  revenue_div[54].text
#         n_minus1_ebitda = revenue_div2[36].text
#         n_minus2_ebitda = revenue_div[55].text
#         n_minus3_ebitda = revenue_div2[37].text
#         n_minus4_ebitda =  revenue_div[56].text

#         ebitda.append(ttm_ebitda)
#         ebitda.append(n_minus1_ebitda)
#         ebitda.append(n_minus2_ebitda)
#         ebitda.append(n_minus3_ebitda)
#         ebitda.append(n_minus4_ebitda)


cash_flow = []

for company in tqdm(faang):
    #driver.maximize_window()
    driver.get("https://sg.finance.yahoo.com/quote/" +str(company) + "/cash-flow?p=" + str(company))
    #driver.find_element(By.XPATH, "//button[starts-with(@class, 'P(0px) M(0px) C($linkColor) Bd(0px) O(n)')]").click()
    time.sleep(3)  # Allow 2 seconds for the web page to open

    for i in range(0,3):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")


    revenue_div = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)')
    revenue_div2 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)')
    
    max_minus1 = len(revenue_div) - 1 
    max_minus2 = len(revenue_div) - 2
    max_minus3 = len(revenue_div) - 3 
    
    maximum_minus1 = len(revenue_div2) - 1 
    maximum_minus2 = len(revenue_div2) - 2 
    
    ttm_cf = revenue_div[max_minus3].text
    n_minus1_cf = revenue_div2[maximum_minus2].text
    n_minus2_cf = revenue_div[max_minus2].text
    n_minus3_cf = revenue_div2[maximum_minus1].text
    n_minus4_cf = revenue_div[max_minus1].text

    
    cash_flow.append(ttm_cf)
    cash_flow.append(n_minus1_cf)
    cash_flow.append(n_minus2_cf)
    cash_flow.append(n_minus3_cf)
    cash_flow.append(n_minus4_cf)

df_yearly_income = pd.DataFrame({
'date': dates,
'ticker': ticker,
'total_revenue': total_revenue,
'gross_profit': gross_profit,
'net_income': net_income,
'ebitda': ebitda,
'cashflow': cash_flow,
'current_time': datetime.now()    
})

df_yearly_income['date'] = df_yearly_income['date'].str.replace("ttm", datetime.today().strftime('%d/%m/%Y'))

dates = [] 
ticker = [] 
total_revenue = []
gross_profit = [] 
net_income = [] 
ebitda = [] 


for company in tqdm(faang):
    #driver.maximize_window()
    driver.get("https://sg.finance.yahoo.com/quote/" +str(company) + "/financials?p=" + str(company))
    driver.find_element(By.XPATH, "//button[starts-with(@class, 'P(0px) M(0px) C($linkColor) Bd(0px) O(n)')]").click()
    time.sleep(3)  # Allow 2 seconds for the web page to open

    for i in range(0,3):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")

    div = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Tt(u) Bgc($lv1BgColor)')
    div2 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)')
    div3 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Bgc($lv1BgColor)')
        
    if len(div) + len(div2) + len(div3) > 5:

        ttm = div[0].text
        n_minus1 = div2[0].text
        n_minus2 = div3[0].text
        n_minus3 = div2[1].text 
        n_minus4 = div3[1].text
        n_minus5 = div2[2].text


        dates.append(ttm)
        dates.append(n_minus1)
        dates.append(n_minus2)
        dates.append(n_minus3)
        dates.append(n_minus4)
        dates.append(n_minus5)

        ticker.append(str(company))
        ticker.append(str(company))
        ticker.append(str(company))
        ticker.append(str(company))
        ticker.append(str(company))
        ticker.append(str(company))

        revenue_div = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)')
        revenue_div2 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)')

        ttm_revenue = revenue_div[0].text
        n_minus1_revenue = revenue_div2[0].text
        n_minus2_revenue = revenue_div[1].text
        n_minus3_revenue = revenue_div2[1].text
        n_minus4_revenue = revenue_div[2].text
        n_minus5_revenue = revenue_div2[2].text

        total_revenue.append(ttm_revenue)
        total_revenue.append(n_minus1_revenue)
        total_revenue.append(n_minus2_revenue)
        total_revenue.append(n_minus3_revenue)
        total_revenue.append(n_minus4_revenue)
        total_revenue.append(n_minus5_revenue)

        ttm_gp = revenue_div[6].text
        n_minus1_gp = revenue_div2[6].text
        n_minus2_gp = revenue_div[7].text
        n_minus3_gp = revenue_div2[7].text
        n_minus4_gp = revenue_div[8].text
        n_minus5_gp = revenue_div2[8].text

        gross_profit.append(ttm_gp)
        gross_profit.append(n_minus1_gp)
        gross_profit.append(n_minus2_gp)
        gross_profit.append(n_minus3_gp)
        gross_profit.append(n_minus4_gp)
        gross_profit.append(n_minus5_gp)


        max_minus19 = len(revenue_div) - 19 
        max_minus20 = len(revenue_div) - 20
        max_minus21 = len(revenue_div) - 21         

        ttm_ni = revenue_div[max_minus21].text
        n_minus1_ni = revenue_div2[max_minus21].text
        n_minus2_ni = revenue_div[max_minus20].text
        n_minus3_ni = revenue_div2[max_minus20].text
        n_minus4_ni =  revenue_div[max_minus19].text
        n_minus5_ni = revenue_div2[max_minus19].text

        net_income.append(ttm_ni)
        net_income.append(n_minus1_ni)
        net_income.append(n_minus2_ni)
        net_income.append(n_minus3_ni)
        net_income.append(n_minus4_ni)
        net_income.append(n_minus5_ni)

        max_minus1 = len(revenue_div) - 1 
        max_minus2 = len(revenue_div) - 2
        max_minus3 = len(revenue_div) - 3 

        ttm_ebitda =  revenue_div[max_minus3].text
        n_minus1_ebitda = revenue_div2[max_minus3].text
        n_minus2_ebitda = revenue_div[max_minus2].text
        n_minus3_ebitda = revenue_div2[max_minus2].text
        n_minus4_ebitda =  revenue_div[max_minus1].text
        n_minus5_ebitda = revenue_div2[max_minus1].text

        ebitda.append(ttm_ebitda)
        ebitda.append(n_minus1_ebitda)
        ebitda.append(n_minus2_ebitda)
        ebitda.append(n_minus3_ebitda)
        ebitda.append(n_minus4_ebitda)
        ebitda.append(n_minus5_ebitda)
        
    else:
        
        ttm = div[0].text
        n_minus1 = div2[0].text
        n_minus2 = div3[0].text
        n_minus3 = div2[1].text 
        n_minus4 = div3[1].text
        #n_minus5 = div2[2].text


        dates.append(ttm)
        dates.append(n_minus1)
        dates.append(n_minus2)
        dates.append(n_minus3)
        dates.append(n_minus4)
        #dates.append(n_minus5)

        ticker.append(str(company))
        ticker.append(str(company))
        ticker.append(str(company))
        ticker.append(str(company))
        ticker.append(str(company))
        #ticker.append(str(company))

        revenue_div = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)')
        revenue_div2 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)')

        ttm_revenue = revenue_div[0].text
        n_minus1_revenue = revenue_div2[0].text
        n_minus2_revenue = revenue_div[1].text
        n_minus3_revenue = revenue_div2[1].text
        n_minus4_revenue = revenue_div[2].text
       # n_minus5_revenue = revenue_div2[2].text

        total_revenue.append(ttm_revenue)
        total_revenue.append(n_minus1_revenue)
        total_revenue.append(n_minus2_revenue)
        total_revenue.append(n_minus3_revenue)
        total_revenue.append(n_minus4_revenue)
        #total_revenue.append(n_minus5_revenue)

        ttm_gp = revenue_div[6].text
        n_minus1_gp = revenue_div2[4].text
        n_minus2_gp = revenue_div[7].text
        n_minus3_gp = revenue_div2[5].text
        n_minus4_gp = revenue_div[8].text
        #n_minus5_gp = revenue_div2[8].text

        gross_profit.append(ttm_gp)
        gross_profit.append(n_minus1_gp)
        gross_profit.append(n_minus2_gp)
        gross_profit.append(n_minus3_gp)
        gross_profit.append(n_minus4_gp)
        #gross_profit.append(n_minus5_gp)


        max_minus19 = len(revenue_div) - 19 
        max_minus20 = len(revenue_div) - 20
        max_minus21 = len(revenue_div) - 21

        max_minus14 = len(revenue_div2) - 14 
        max_minus13 = len(revenue_div2) - 13

        ttm_ni = revenue_div[max_minus21].text
        n_minus1_ni = revenue_div2[max_minus14].text
        n_minus2_ni = revenue_div[max_minus20].text
        n_minus3_ni = revenue_div2[max_minus13].text
        n_minus4_ni =  revenue_div[max_minus19].text
        #n_minus5_ni = revenue_div2[max_minus19].text

        net_income.append(ttm_ni)
        net_income.append(n_minus1_ni)
        net_income.append(n_minus2_ni)
        net_income.append(n_minus3_ni)
        net_income.append(n_minus4_ni)
        #net_income.append(n_minus5_ni)

        max_minus1 = len(revenue_div) - 1 
        max_minus2 = len(revenue_div) - 2
        max_minus3 = len(revenue_div) - 3 

        maximum_minus1 = len(revenue_div2) - 1 
        maximum_minus2 = len(revenue_div2) - 2 

        ttm_ebitda =  revenue_div[max_minus3].text
        n_minus1_ebitda = revenue_div2[maximum_minus2].text
        n_minus2_ebitda = revenue_div[max_minus2].text
        n_minus3_ebitda = revenue_div2[maximum_minus1].text
        n_minus4_ebitda =  revenue_div[max_minus1].text
        #n_minus5_ebitda = revenue_div2[max_minus1].text

        ebitda.append(ttm_ebitda)
        ebitda.append(n_minus1_ebitda)
        ebitda.append(n_minus2_ebitda)
        ebitda.append(n_minus3_ebitda)
        ebitda.append(n_minus4_ebitda)
        #ebitda.append(n_minus5_ebitda) 

cash_flow = []

for company in tqdm(faang):
    #driver.maximize_window()
    driver.get("https://sg.finance.yahoo.com/quote/" +str(company) + "/cash-flow?p=" + str(company))
    driver.find_element(By.XPATH, "//button[starts-with(@class, 'P(0px) M(0px) C($linkColor) Bd(0px) O(n)')]").click()
    time.sleep(3)  # Allow 2 seconds for the web page to open

    for i in range(0,3):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    div = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Tt(u) Bgc($lv1BgColor)')
    div2 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)')
    div3 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Bgc($lv1BgColor)')
    
    revenue_div = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)')
    revenue_div2 = soup.find_all('div', class_='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)')
    
    if len(div) + len(div2) + len(div3) > 5:
    
        max_minus1 = len(revenue_div) - 1 
        max_minus2 = len(revenue_div) - 2
        max_minus3 = len(revenue_div) - 3 

        ttm_cf = revenue_div[max_minus3].text
        n_minus1_cf = revenue_div2[max_minus3].text
        n_minus2_cf = revenue_div[max_minus2].text
        n_minus3_cf = revenue_div2[max_minus2].text
        n_minus4_cf = revenue_div[max_minus1].text
        n_minus5_cf = revenue_div2[max_minus1].text

        cash_flow.append(ttm_cf)
        cash_flow.append(n_minus1_cf)
        cash_flow.append(n_minus2_cf)
        cash_flow.append(n_minus3_cf)
        cash_flow.append(n_minus4_cf)
        cash_flow.append(n_minus5_cf)
    
    else:
        
        max_minus1 = len(revenue_div) - 1 
        max_minus2 = len(revenue_div) - 2
        max_minus3 = len(revenue_div) - 3 

        maximum_minus1 = len(revenue_div2) - 1 
        maximum_minus2 = len(revenue_div2) - 2 

        ttm_cf = revenue_div[max_minus3].text
        n_minus1_cf = revenue_div2[maximum_minus2].text
        n_minus2_cf = revenue_div[max_minus2].text
        n_minus3_cf = revenue_div2[maximum_minus1].text
        n_minus4_cf = revenue_div[max_minus1].text
        #n_minus5_cf = revenue_div2[max_minus1].text

        cash_flow.append(ttm_cf)
        cash_flow.append(n_minus1_cf)
        cash_flow.append(n_minus2_cf)
        cash_flow.append(n_minus3_cf)
        cash_flow.append(n_minus4_cf)
        #cash_flow.append(n_minus5_cf)

df_quarterly_income = pd.DataFrame({
'date': dates,
'ticker': ticker,
'total_revenue': total_revenue,
'gross_profit': gross_profit,
'net_income': net_income,
'ebitda': ebitda,
'cashflow': cash_flow,
'current_time': datetime.now()    
})

df_quarterly_income['date'] = df_quarterly_income['date'].str.replace("ttm", datetime.today().strftime('%d/%m/%Y'))

ticker = []
market_cap_intraday = [] 
enterprise_value = [] 
trailing_pe = [] 
forward_pe = [] 
peg_ratio = [] 
price_over_sales = [] 
price_over_book = [] 
ev_over_revenue = [] 
ev_over_ebitda = [] 
profit_margin = [] 
operating_margin = [] 
total_cash_mrq = [] 
total_debt_mrq = [] 
total_debt_over_equity_mrq = [] 
operating_cash_flow_ttm = [] 
shares_outstanding = [] 

for company in tqdm(faang):
    #driver.maximize_window()
    driver.get("https://sg.finance.yahoo.com/quote/" +str(company) + "/key-statistics?p=" + str(company))
    time.sleep(3)  # Allow 2 seconds for the web page to open

    for i in range(0,3):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    valuation = soup.find_all('td', class_='Fw(500) Ta(end) Pstart(10px) Miw(60px)')
    #valuation2 = soup.find_all('td', class_='Fw(500) Ta(end) Pstart(10px) Miw(60px)')
    
    ticker.append(str(company))
    
    marketcapintraday = valuation[0].text 
    market_cap_intraday.append(marketcapintraday)
    
    ev = valuation[1].text
    enterprise_value.append(ev)
    
    trailingpe = valuation[2].text
    trailing_pe.append(trailingpe)
    
    forwardpe = valuation[3].text
    forward_pe.append(forwardpe)
    
    pegratio = valuation[4].text
    peg_ratio.append(pegratio)
    
    priceoversales = valuation[5].text
    price_over_sales.append(priceoversales)
    
    priceoverbook = valuation[6].text
    price_over_book.append(priceoverbook)
    
    evoverrevenue = valuation[7].text
    ev_over_revenue.append(evoverrevenue)
    
    evoverebitda = valuation[8].text
    ev_over_ebitda.append(evoverebitda)
    
    profitmargin = valuation[40].text
    profit_margin.append(profitmargin)
    
    operatingmargin = valuation[41].text
    operating_margin.append(operatingmargin)
    
    total_cash = valuation[52].text
    total_cash_mrq.append(total_cash)
    
    total_debt = valuation[54].text
    total_debt_mrq.append(total_debt)
    
    total_debt_over_equity = valuation[55].text
    total_debt_over_equity_mrq.append(total_debt_over_equity)
    
    operating_cash_flow = valuation[58].text
    operating_cash_flow_ttm.append(operating_cash_flow) 
    
    share_out_standing = valuation[18].text
    shares_outstanding.append(share_out_standing)
    
df_main_statistics_info = pd.DataFrame({
'ticker': ticker,
'market_cap_intraday': market_cap_intraday,
'enterprise_value': enterprise_value,
'trailing_pe': trailing_pe,
'forward_pe': forward_pe,
'peg_ratio': peg_ratio,
'price_over_sales': price_over_sales,
'price_over_book': price_over_book, 
'ev_over_revenue': ev_over_revenue, 
'ev_over_ebitda': ev_over_ebitda, 
'profit_margin': profit_margin, 
'operating_margin': operating_margin, 
'total_cash_mrq': total_cash_mrq, 
'total_debt_mrq': total_debt_mrq, 
'total_debt_over_equity_mrq': total_debt_over_equity_mrq,
'operating_cash_flow_ttm': operating_cash_flow_ttm, 
'shares_outstanding': shares_outstanding,
'current_time': datetime.now()    
})

cleaned_enterprise_value = []
cleaned_market_cap = [] 
cleaned_total_cash = [] 
cleaned_total_debt = []
cleaned_operating_cashflow = [] 
cleaned_shares_outstanding = [] 

for i in tqdm(df_main_statistics_info['enterprise_value']): 
    if i[-1:] == 'B':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000
        cleaned_enterprise_value.append(cleaned_value)
    if i[-1:] == 'T':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000000
        cleaned_enterprise_value.append(cleaned_value)
    if i[-1:] == 'M':
        cv = float(i[:-1])
        cleaned_value = cv * 1000
        cleaned_enterprise_value.append(cleaned_value)
        

for i in tqdm(df_main_statistics_info['market_cap_intraday']): 
    if i[-1:] == 'B':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000
        cleaned_market_cap.append(cleaned_value)
    if i[-1:] == 'T':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000000
        cleaned_market_cap.append(cleaned_value)
    if i[-1:] == 'M':
        cv = float(i[:-1])
        cleaned_value = cv * 1000
        cleaned_market_cap.append(cleaned_value)
        
for i in tqdm(df_main_statistics_info['total_cash_mrq']): 
    if i[-1:] == 'B':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000
        cleaned_total_cash.append(cleaned_value)
    if i[-1:] == 'T':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000000
        cleaned_total_cash.append(cleaned_value)
    if i[-1:] == 'M':
        cv = float(i[:-1])
        cleaned_value = cv * 1000
        cleaned_total_cash.append(cleaned_value)
        
for i in tqdm(df_main_statistics_info['total_debt_mrq']): 
    if i[-1:] == 'B':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000
        cleaned_total_debt.append(cleaned_value)
    if i[-1:] == 'T':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000000
        cleaned_total_debt.append(cleaned_value)
    if i[-1:] == 'M':
        cv = float(i[:-1])
        cleaned_value = cv * 1000
        cleaned_total_debt.append(cleaned_value)
        
for i in tqdm(df_main_statistics_info['operating_cash_flow_ttm']): 
    if i[-1:] == 'B':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000
        cleaned_operating_cashflow.append(cleaned_value)
    if i[-1:] == 'T':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000000
        cleaned_operating_cashflow.append(cleaned_value)
    if i[-1:] == 'M':
        cv = float(i[:-1])
        cleaned_value = cv * 1000
        cleaned_operating_cashflow.append(cleaned_value)
        
for i in tqdm(df_main_statistics_info['shares_outstanding']): 
    if i[-1:] == 'B':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000
        cleaned_shares_outstanding.append(cleaned_value)
    if i[-1:] == 'T':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000000
        cleaned_shares_outstanding.append(cleaned_value)
    if i[-1:] == 'M':
        cv = float(i[:-1])
        cleaned_value = cv * 1000
        cleaned_shares_outstanding.append(cleaned_value)
        
df_main_statistics_info['enterprise_value'] = cleaned_enterprise_value
df_main_statistics_info['market_cap_intraday'] = cleaned_market_cap
df_main_statistics_info['total_cash_mrq'] = cleaned_total_cash
df_main_statistics_info['total_debt_mrq'] = cleaned_total_debt
df_main_statistics_info['operating_cash_flow_ttm'] = cleaned_operating_cashflow
df_main_statistics_info['shares_outstanding'] = cleaned_shares_outstanding

date_quarter = [] 
ticker = []
earnings_estimate = [] 
year_ago_eps = [] 
revenue_estimate = [] 
actual_revenue = [] 

for company in tqdm(faang):
    #driver.maximize_window()
    driver.get("https://sg.finance.yahoo.com/quote/" +str(company) + "/analysis?p=" + str(company))
    #driver.find_element(By.XPATH, "//button[starts-with(@class, 'P(0px) M(0px) C($linkColor) Bd(0px) O(n)')]").click()
    time.sleep(2)  # Allow 2 seconds for the web page to open

    for i in range(0,3):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    div = soup.find_all('th', class_='Fw(400) W(20%) Fz(xs) C($tertiaryColor) Ta(end)')
    
    date_range = div[0].text 
    date_range2 = div[1].text 
    date_range3 = div[2].text 
    date_range4 = div[3].text 
    
    date_quarter.append(date_range)
    date_quarter.append(date_range2)
    date_quarter.append(date_range3)
    date_quarter.append(date_range4)
    
    ticker.append(str(company))
    ticker.append(str(company))
    ticker.append(str(company))
    ticker.append(str(company))
    
    earnings = soup.find_all('td', class_ = 'Ta(end)')
    
    ee1 = earnings[4].text 
    ee2 = earnings[5].text
    ee3 = earnings[6].text
    ee4 = earnings[7].text
    
    earnings_estimate.append(ee1)
    earnings_estimate.append(ee2)
    earnings_estimate.append(ee3)
    earnings_estimate.append(ee4)
    
    year_ago1 = earnings[16].text 
    year_ago2 = earnings[17].text
    year_ago3 = earnings[18].text
    year_ago4 = earnings[19].text
    
    year_ago_eps.append(year_ago1)
    year_ago_eps.append(year_ago2)
    year_ago_eps.append(year_ago3)
    year_ago_eps.append(year_ago4)
    
    rev_est1 = earnings[24].text 
    rev_est2 = earnings[25].text
    rev_est3 = earnings[26].text
    rev_est4 = earnings[27].text
    
    revenue_estimate.append(rev_est1)
    revenue_estimate.append(rev_est2)
    revenue_estimate.append(rev_est3)
    revenue_estimate.append(rev_est4)
    
    rev_act1 = earnings[36].text 
    rev_act2 = earnings[37].text
    rev_act3 = earnings[38].text
    rev_act4 = earnings[39].text
    
    actual_revenue.append(rev_act1)
    actual_revenue.append(rev_act2)
    actual_revenue.append(rev_act3)
    actual_revenue.append(rev_act4)    

date_ranges = []
ticker = []
est_eps = []
actual_eps = [] 
difference = [] 
surprise = [] 

for company in tqdm(faang):
    #driver.maximize_window()
    driver.get("https://sg.finance.yahoo.com/quote/" +str(company) + "/analysis?p=" + str(company))
    #driver.find_element(By.XPATH, "//button[starts-with(@class, 'P(0px) M(0px) C($linkColor) Bd(0px) O(n)')]").click()
    time.sleep(2)  # Allow 2 seconds for the web page to open

    for i in range(0,3):
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    div = soup.find_all('th', class_='Fw(400) W(20%) Fz(xs) C($tertiaryColor) Ta(end)')
    
    date_range = div[8].text 
    date_range2 = div[9].text 
    date_range3 = div[10].text 
    date_range4 = div[11].text 
    
    date_ranges.append(date_range)
    date_ranges.append(date_range2)
    date_ranges.append(date_range3)
    date_ranges.append(date_range4)
    
    ticker.append(str(company))
    ticker.append(str(company))
    ticker.append(str(company))
    ticker.append(str(company))
    
    earnings = soup.find_all('td', class_ = 'Ta(end)')
    
    eeps1 = earnings[44].text 
    eeps2 = earnings[45].text
    eeps3 = earnings[46].text
    eeps4 = earnings[47].text
    
    est_eps.append(eeps1)
    est_eps.append(eeps2)
    est_eps.append(eeps3)
    est_eps.append(eeps4)
    
    
    aeps1 = earnings[48].text 
    aeps2 = earnings[49].text
    aeps3 = earnings[50].text
    aeps4 = earnings[51].text

    actual_eps.append(aeps1)
    actual_eps.append(aeps2)
    actual_eps.append(aeps3)
    actual_eps.append(aeps4)
    
    diff1 = earnings[52].text 
    diff2 = earnings[53].text
    diff3 = earnings[54].text
    diff4 = earnings[55].text

    difference.append(diff1)
    difference.append(diff2)
    difference.append(diff3)
    difference.append(diff4)
    
        
    surprise1 = earnings[56].text 
    surprise2 = earnings[57].text
    surprise3 = earnings[58].text
    surprise4 = earnings[59].text

    surprise.append(surprise1)
    surprise.append(surprise2)
    surprise.append(surprise3)
    surprise.append(surprise4)
    
df_analysis_info = pd.DataFrame({
'date_quarter' : date_quarter,
'ticker': ticker,
'earnings_estimate': earnings_estimate, 
'year_ago_eps': year_ago_eps,
'revenue_estimate': revenue_estimate,
'actual_revenue': actual_revenue,
'current_time': datetime.now()    
})

cleaned_revenue_estimate = []
cleaned_actual_revenue = [] 

for i in tqdm(df_analysis_info['revenue_estimate']): 
    if i[-1:] == 'B':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000
        cleaned_revenue_estimate.append(cleaned_value)
    if i[-1:] == 'T':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000000
        cleaned_shares_outstanding.append(cleaned_value)
    if i[-1:] == 'M':
        cv = float(i[:-1])
        cleaned_value = cv * 1000
        cleaned_revenue_estimate.append(cleaned_value)
        
for i in tqdm(df_analysis_info['actual_revenue']): 
    if i[-1:] == 'B':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000
        cleaned_actual_revenue.append(cleaned_value)
    if i[-1:] == 'T':
        cv = float(i[:-1])
        cleaned_value = cv * 1000000000
        cleaned_actual_revenue.append(cleaned_value)
    if i[-1:] == 'M':
        cv = float(i[:-1])
        cleaned_value = cv * 1000
        cleaned_actual_revenue.append(cleaned_value)        

        
df_analysis_info['revenue_estimate'] = cleaned_revenue_estimate
df_analysis_info['actual_revenue'] = cleaned_actual_revenue

df_analysis_info2 = pd.DataFrame({
'date_ranges' : date_ranges,
'ticker': ticker,
'est_eps': est_eps, 
'actual_eps': actual_eps,
'difference': difference,
'surprise': surprise,
'current_time': datetime.now()    
})

import pygsheets

gc = pygsheets.authorize(service_file= r'C:\Users\kentj\Desktop\scrape\amazon scrape\principal-iris-338314-cb4e85371557.json') # authorize

output = gc.open('Yahoo Finance')

daily_price = output[0]

daily_price.set_dataframe(df,(1,1))

yearly_income = output[1]

yearly_income.set_dataframe(df_yearly_income, (1,1))

quarterly_income = output[2]

quarterly_income.set_dataframe(df_quarterly_income, (1,1))

main_statistic = output[3]

main_statistic.set_dataframe(df_main_statistics_info, (1,1))

analysis_info = output[4]

analysis_info.set_dataframe(df_analysis_info, (1,1))

analysis_info2 = output[5]

analysis_info2.set_dataframe(df_analysis_info2, (1,1))