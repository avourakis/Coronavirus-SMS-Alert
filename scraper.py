import requests
from urllib.parse import urljoin
from collections import defaultdict
from selenium import webdriver
import time
import os
from twilio.rest import Client

URL = "https://arcg.is/0fHmTX"
URL_MOBILE = "https://arcg.is/1DPOWm0"

# Settings used to trigger an SMS alert
COUNTRIES = ["US", "Sweden"]
THRESHOLDS = [12, 1]

def send_sms_alert(message):
    """ Send an sms alert using the message variable"""

    #print(message)
    client = Client(os.environ.get("TWILIO_SID"), os.environ.get("TWILIO_TOKEN"))
    client.messages.create(body = message, from_ =os.environ.get("TWILIO_NUMBER"),to = os.environ.get("PHONE_NUMBER"))
        
    time.sleep(2)


def get_footer_message(ts):
    """ Create a simple footer message to be sent with every alert"""

    return "For more info: {}\n{}".format(URL_MOBILE, ts)

    
def send_test_alert():
    """ Send a test alert to make sure everything is working properly """
    
    countries_confirmed, ts = scrape_confirmed_countries()
    message = "{} has {} cases.\n{}".format(list(countries_confirmed.keys())[0], list(countries_confirmed.values())[0], get_footer_message(ts))
    #print(message)
    send_sms_alert(message)


def get_confirmed_data(driver):
    """ Gets data of countries with their confirmed number of cases"""

    confirmed_cases_results = driver.find_elements_by_xpath("//*[@id='ember32']")
    
    countries_confirmed = defaultdict(int)
    for confirmed in confirmed_cases_results:
        countries = confirmed.find_elements_by_class_name("external-html")
        for country in countries:
            country_attr = country.text.split(" ", 1)
            countries_confirmed[country_attr[1]] = int(country_attr[0].replace(",", ""))

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

    # Call Helper functions to scrape data
    countries_confirmed = get_confirmed_data(driver)
    ts = get_ts_data(driver)
        
    driver.quit()

    return countries_confirmed, ts

def get_alert_message(country, confirmed, ts):
    footer = get_footer_message(ts)
    return "Alert Triggered!\n{} has {} confirmed cases.\n{}".format(country, confirmed, footer)
    

def check_status():
    """ Scrapes website and checks weather an alert should be sent """    
    
    countries_confirmed, ts = scrape_confirmed_countries()
    
    for country, threshold in zip(COUNTRIES, THRESHOLDS):
        if countries_confirmed[country] >= threshold:
            print("{} triggered an alert!".format(country))
            send_sms_alert(get_alert_message(country, countries_confirmed[country], ts))
        else:
            print("{} didn't trigger an alert.".format(country))


if __name__ == '__main__':
    #send_test_alert()     
    check_status()
