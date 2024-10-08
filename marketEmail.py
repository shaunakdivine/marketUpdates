import requests
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText

# Load the API key from environment variables
API_KEY = os.getenv('RAPIDAPI_KEY')

def get_yahoo_finance_data(symbol):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes?symbols={symbol}&region=US"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "quoteResponse" in data and len(data["quoteResponse"]["result"]) > 0:
        return data["quoteResponse"]["result"][0]
    else:
        return None

def print_yahoo_finance_data(symbol, data):
    if data:
        return (f"{symbol} Data:\n"
                f"Price: ${data['regularMarketPrice']}\n"
                f"Previous Close: ${data['regularMarketPreviousClose']}\n"
                f"Change: {data['regularMarketChange']} ({data['regularMarketChangePercent']}%)\n"
                f"Volume: {data['regularMarketVolume']}\n\n")
    else:
        return f"No data found for {symbol}.\n\n"

def fetch_and_print_data():
    result = f"Good morning, market update time! Fetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CT\n\n"
    
    symbols = ['^DJI', '^GSPC', '^IXIC', '^VIX', 'GC=F', 'CL=F', 'BTC-USD', '^TNX']
    result += """
    Symbol Definitions:
    -------------------
    Dow Jones Industrial Average:  ^DJI
    S&P 500 Index:                 ^GSPC
    NASDAQ Composite Index:        ^IXIC
    Volatility Index (VIX):        ^VIX
    Gold Futures:                  GC=F
    WTI Crude Oil Futures:         CL=F
    Bitcoin (BTC) to USD:          BTC-USD
    10-Year Treasury Yield:        ^TNX
    -------------------
    \n\n
    """
    
    for symbol in symbols:
        data = get_yahoo_finance_data(symbol)
        
        result += print_yahoo_finance_data(symbol, data)
    
    return result

def send_email(body):
    # Set up your email server and login credentials
    sender_email = "shaunakmarketupdate@gmail.com"
    receiver_email = "shaunak.divine@gmail.com"
    # password = os.getenv('APP_PASS')
    password = #PUT IN PASSWORD

    # Create the email
    msg = MIMEText(body)
    msg['Subject'] = "Daily Market Update"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Fetch market data
    data = fetch_and_print_data()
    
    # Send the data via email
    send_email(data)
