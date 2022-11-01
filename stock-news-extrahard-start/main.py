STOCK = "TSLA"
COMPANY_NAME = "TESLA"
import requests
import smtplib
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from datetime import date, timedelta

my_email = "vramshesh@gmail.com"
gmailpasswd = os.environ("gmailpasswd")


API_skey= os.environ("API_skey")   #stock market key
API_nkey = os.environ("API_nkey")  #news key
STOCK_Endpoint = "https://www.alphavantage.co/query"
NEWS_Endpoint = "https://newsapi.org/v2/everything"
account_sid = os.environ("AccountSID")  #Twilio account and token
auth_token = os.environ("Authtoken")

parameters_stock ={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":API_skey,
}


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get(STOCK_Endpoint,params=parameters_stock)
response.raise_for_status()
stock_data = response.json()
current_day = date.today()
current_dayofweek = date.today().weekday()
print(current_dayofweek)

if current_dayofweek==0:
    previous_day = current_day - timedelta(days=3)
    previous_day2 = current_day - timedelta(days=4)

elif current_dayofweek==1:
    previous_day = current_day - timedelta(days=1)
    previous_day2 = current_day - timedelta(days=4)

elif current_dayofweek==7:
    previous_day = current_day - timedelta(days=2)
    previous_day2 = current_day - timedelta(days=3)

else:
    previous_day = current_day - timedelta(days=1)
    previous_day2 = current_day - timedelta(days=2)

#print(previous_day2)

prev_close = float(stock_data["Time Series (Daily)"][f"{previous_day}"]["4. close"])
prev_close2 = float(stock_data["Time Series (Daily)"][f"{previous_day2}"]["4. close"])
percent_change = abs((prev_close-prev_close2)/prev_close)*100
percent_change = round(percent_change, 2)
print(percent_change)
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if percent_change>0.1:
    parameters_news ={
    "q":COMPANY_NAME,
     "from":current_day,
     "apikey":API_nkey,
        }
    response = requests.get(NEWS_Endpoint,params=parameters_news)
    response.raise_for_status()
    news_data = response.json()


    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=f"\n\"{STOCK}: 🔺{percent_change}%\nHeadline: {news_data['articles'][0]['title']}\nBrief:{news_data['articles'][0]['description']}\nHeadline: {news_data['articles'][1]['title']}\nBrief:{news_data['articles'][1]['description']}\nHeadline: {news_data['articles'][2]['title']}\nBrief:{news_data['articles'][2]['description']}\n\"\"\"",
                         from_='+twilionumber',
                         to='+myphonenumber'
                     )


