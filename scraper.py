from bs4 import BeautifulSoup as bs
import requests
import re
import numpy as np
import datetime
import pandas as pd
from urllib.parse import urljoin
from collections import defaultdict
from selenium import webdriver
import time
import pickle
import os

def scrape_confirmed_data(driver):
    """ Scrapes data of confimed countries"""

    confirmed_cases_results = driver.find_elements_by_xpath("//*[@id='ember32']")
    
    countries_confirmed = [] 
    for confirmed in confirmed_cases_results:
        countries = confirmed.find_elements_by_class_name("external-html")
        for country in countries:
            country_attr = country.text.split(" ")
            countries_confirmed.append({"name": country_attr[1], "confirmed": country_attr[0]})

    return countries_confirmed

def scrape_ts_data(driver):
    """ Scrapes data of when website was last updated """

    # Get last updated time
    last_updated_results = driver.find_element_by_xpath("//*[@id='ember46']/div")
    return last_updated_results.text

def scrape(url):
    """ Scrapes all the data that will be used to send alerts """

    # Request Web Page
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    countries_confirmed = scrape_confirmed_data(driver)
    ts = scrape_ts_data(driver)
        
    print(countries_confirmed)
    print(ts)
    
    driver.quit()

if __name__ == '__main__':
    url = "https://arcg.is/0fHmTX"
    scrape(url)
    
    
