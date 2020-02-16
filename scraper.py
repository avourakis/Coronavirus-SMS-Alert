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
from twilio.rest import Client

URL = "https://arcg.is/0fHmTX"

def send_sms_alert(message):
    """ Send an sms alert using the message variable"""

    client = Client(os.environ.get("TWILIO_SID"), os.environ.get("TWILIO_TOKEN"))
    client.messages.create(body = message, from_ =os.environ.get("TWILIO_NUMBER"),to = os.environ.get("PHONE_NUMBER"))


def get_footer_message(ts):
    """ Create a simple footer message to be sent with every alert"""

    return "For more info: {}\n{}".format(URL, ts)

    
def send_test_alert():
    """ Send a test alert to make sure everything is working properly """
    
    countries_confirmed, ts = scrape_confirmed_countries()
    message = "{} has {} cases.\n{}".format(countries_confirmed[0]["name"], countries_confirmed[0]["confirmed"], get_footer_message(ts))
    #print(message)
    send_sms_alert(message)


def get_confirmed_data(driver):
    """ Gets data of countries with their confirmed number of cases"""

    confirmed_cases_results = driver.find_elements_by_xpath("//*[@id='ember32']")
    
    countries_confirmed = [] 
    for confirmed in confirmed_cases_results:
        countries = confirmed.find_elements_by_class_name("external-html")
        for country in countries:
            country_attr = country.text.split(" ", 1)
            countries_confirmed.append({"name": country_attr[1], "confirmed": country_attr[0]})

    return countries_confirmed


def get_ts_data(driver):
    """ Gets data of when website was last updated """

    # Get last updated time
    last_updated_results = driver.find_element_by_xpath("//*[@id='ember46']/div")
    return last_updated_results.text


def scrape_confirmed_countries():
    """ Scrapes all the data that will be used to send alerts """

    # Request Web Page
    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(5)

    countries_confirmed = get_confirmed_data(driver)
    ts = get_ts_data(driver)
        
    driver.quit()

    return countries_confirmed, ts


if __name__ == '__main__':
    send_test_alert()     
