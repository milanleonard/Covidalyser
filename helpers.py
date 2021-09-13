from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time
import altair as alt

def _get_webdriver():
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    driver = webdriver.Firefox(options=fireFoxOptions)
    return driver

def collect_data(url, archived=True):
    print("Setting up headless browser in background")
    driver = _get_webdriver()
    print("Browser set up, downloading latest COVID exposure site information")
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    current = pd.read_html(html)[0]
    element = driver.find_element(By.ID,"chkArchived1822887")
    element.click()
    time.sleep(1)
    html = driver.page_source
    archived = pd.read_html(html)[0]
    return current, archived


def check_shop(data, shop):
    shop = shop.replace('/','|')
    if "|" in shop:
        print("Operating in OR mode")
        shopping_data  = data[data['Exposure Location'].str.contains(shop, case=False)]
    else:
        print("Finding a specific shop")
        for substr in shop.split(' '):
            shopping_data = data[data['Exposure Location'].str.contains(substr, case=False)]
    if len(shopping_data) == 0:
        print("Shop not found")
    return shopping_data.copy()

def add_times(shopping_data):
    shopping_data['arr_time'] = pd.to_datetime(shopping_data['Arrival Time'])
    shopping_data['dep_time'] = pd.to_datetime(shopping_data['Departure Time'])
    shopping_data['fake_dep_time'] = shopping_data['dep_time'] + pd.to_timedelta(59,'min') # If there's any overlap with an hour show it here.
    df1 = shopping_data.copy()
    df2 = shopping_data.copy()
    df1.index = df1['arr_time']
    df2.index = df2['fake_dep_time']
    df_final = pd.DataFrame(df1.groupby(pd.Grouper(freq='h')).count()['Contact'].fillna(0).subtract(df2.groupby(pd.Grouper(freq='h')).count()['Contact'].fillna(0),fill_value=0).cumsum())
    df_final.reset_index(inplace=True)
    df_final.columns = ["Hour of day", "Number of contacts"]
    df_final['Hour of day'] = df_final['Hour of day'].dt.strftime('%H')
    return df_final

def make_plot(data, shops):
    chart = alt.Chart(data).mark_bar().encode(
    x='Hour of day',
    y='Number of contacts'
    ).properties(
        title=[f'Number of times shops {shops} have been','listed as an exposure location at certain times of day'],
        width=650,
        height=500
    ).interactive()
    return chart
    