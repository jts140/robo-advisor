 #this is the "app/robo_advisor.py" file

import os
import requests
import json
import csv

from dotenv import load_dotenv
load_dotenv() #loads contents of dot env file

#usd formatting function
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

#saves time for output
from datetime import datetime
now = datetime.now()


#info inputs

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")


#data validation for ticker
is_valid_ticker = False 

while  is_valid_ticker == False:
   
    ticker = input("Please enter a valid stock ticker (ie 1-5 letter ticker and trades on a US exchange):")
   
    if len(ticker) >= 1 and len(ticker) <=5 and ticker.isnumeric() == False:
        
        ticker = ticker.upper()
        
        #request url and set up dictionary so code can test if stock ticker is supported by API
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"

        response = requests.get(request_url)

        parsed_response = json.loads(response.text)
        
        if parsed_response == {'Error Message': 'Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY.'}:

            print("You have entered a stock ticker that is either invalid or not tracked by the API, please try again")

            is_valid_ticker = False

        else:
            
            is_valid_ticker = True 

    else:

        print("You have entered an invalid stock ticker, please try again")
        
        is_valid_ticker = False

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates =list(tsd.keys()) #assumes first day is on top, but may need to sort if data structure changes

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

# graph done with Joe O'Brien
# max of all the high prices and min of all low prices
high_prices  = []
low_prices = []
close_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    #for graph
    daily_close= (tsd[date]["4. close"])
    
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))
    #for graph
    close_prices.append(float(daily_close))

recent_high = max(high_prices)
recent_low = min(low_prices)

#buy or sell recomendation

discount = (1 - (float(latest_close)/float(recent_high)))
premium = ((float(latest_close)/float(recent_low))-1)

if discount >= .2:
    recomendation = "Buy!"
    reason = f"The stock is trading at a {round(discount*100,2)}% discount compared to its recent high"
else:
    recomendation = "Sell"
    reason = f"The stock is trading at a {round(discount*100,2)}% discount compared to its recent high"

#info outputs
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers =["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames= csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high":daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })


print("-------------------------")
print(f"SELECTED SYMBOL: {ticker}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime("%Y-%m-%d %H:%M:%S")) 
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {recomendation}")
print(f"RECOMMENDATION REASON: {reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#add graph (done with Joe O'Brien)
import plotly
import plotly.graph_objs as go

plotly.offline.plot({
    "data": [go.Scatter(x=dates, y=close_prices)],
    "layout": go.Layout(title=f"{ticker} close prices")
}, auto_open=True)
