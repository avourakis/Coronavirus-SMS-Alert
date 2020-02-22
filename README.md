# Coronavirus SMS Alert!

A script that sends you an SMS alert when a number of confirmed cases in a country reaches a certain level.

## Motivation:
Due to the recent coronavirus outbreak in Asia, people from the rest of the world are growing concerned that the virus
will continue to spread and eventually reach their country; therefore this script is meant to help people set up alert
triggers for when their country reaches a certain number of confirmed cases. This way, they can begin to prepare by
taking necessary action.

The Coronavirus global data is scraped from this dashboard provided by Johns Hopkins CSSE: https://arcg.is/0fHmTX

This article explains step by step how to build this project: https://towardsdatascience.com/building-a-coronavirus-outbreak-sms-alert-system-d80f4d648eea

## Requirements:
* Python 3 or higher
* Selenium
* Twilio

## Future Improvements:
* Define alert triggers via SMS
* Support triggers on other types of data such as "Total Deaths"
* Support multiple SMS recipients
* Add more error handling

