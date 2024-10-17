import requests
import feedparser
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

def format_finance_data(symbol, data):
    if data:
        return (f"{symbol} Data:\n"
                f"  Price: ${data['regularMarketPrice']:,.2f}\n"
                f"  Previous Close: ${data['regularMarketPreviousClose']:,.2f}\n"
                f"  Change: {data['regularMarketChange']:.2f} ({data['regularMarketChangePercent']:.2f}%)\n"
                f"  Volume: {data['regularMarketVolume']:,}\n")
    else:
        return f"{symbol} Data: No data available.\n"


        

def fetch_and_format_data():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = f"Good afternoon, market update time! Fetching data at {timestamp} CT\n\n"
    
    symbols = ['^DJI', '^GSPC', '^IXIC', '^VIX', 'GC=F', 'CL=F', 'BTC-USD', '^TNX']
    #symbols = ['^DJI']
    result += (
        "****************************************\n"
        "*            Market Overview            *\n"
        "****************************************\n"
        "Symbol Definitions:\n"
        "-------------------\n"
        "  Dow Jones Industrial Average:  ^DJI\n"
        "  S&P 500 Index:                 ^GSPC\n"
        "  NASDAQ Composite Index:        ^IXIC\n"
        "  Volatility Index (VIX):        ^VIX\n"
        "  Gold Futures:                  GC=F\n"
        "  WTI Crude Oil Futures:         CL=F\n"
        "  Bitcoin (BTC) to USD:          BTC-USD\n"
        "  10-Year Treasury Yield:        ^TNX\n"
        "-------------------\n\n"
    )
    
    for symbol in symbols:
        data = get_yahoo_finance_data(symbol)
        result += format_finance_data(symbol, data) + "\n"
    
    return result

def get_financial_news_from_rss():
    rss_feed_url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"  # CNBC Financial News RSS feed
    feed = feedparser.parse(rss_feed_url)

    if 'entries' in feed and len(feed.entries) > 0:
        headlines = "\n".join([f"- {entry.title}" for entry in feed.entries[:6]])  # Get top 5 headlines
        return (
            "****************************************\n"
            "*    Top Financial Headlines from CNBC   *\n"
            "****************************************\n"
            f"{headlines}\n\n\n"
        )
    else:
        return (
            "****************************************\n"
            "*    Top Financial Headlines from CNBC   *\n"
            "****************************************\n"
            "\nNo financial news available at the moment.\n"
        )
    
# Function to fetch financial news from WSJ RSS Feed
def get_wsj_headlines():
    wsj_rss_url = "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"  # WSJ Markets RSS feed
    feed = feedparser.parse(wsj_rss_url)

    if 'entries' in feed and len(feed.entries) > 0:
        headlines = "\n".join([f"- {entry.title}" for entry in feed.entries[:6]])  # Get top 5 headlines
        return (
            "****************************************\n"
            "*    Top Financial Headlines from WSJ    *\n"
            "****************************************\n"
            f"{headlines}\n\n\n"
        )
    else:
        return (
            "****************************************\n"
            "*    Top Financial Headlines from WSJ    *\n"
            "****************************************\n"
            "\nNo financial news available at the moment.\n"
        )

def send_email(body):
    # Set up your email server and login credentials
    sender_email = "shaunakmarketupdate@gmail.com"
    receiver_email = [
        "shaunak.divine@gmail.com", "eshaanarora99@gmail.com", 
        "graysonmerritt@gmail.com", "oliversgault@gmail.com", 
        "maggiekleman@utexas.edu", "ahattendorf@utexas.edu",
        "destin.blanchard@utexas.edu", "sdstempak14@gmail.com"
    ]
    #receiver_email = ["shaunak.divine@gmail.com", "eshaanarora99@gmail.com"]
    # password = os.getenv('APP_PASS')
    password = test

    recipients_str = ", ".join(receiver_email)

    # Create the email
    msg = MIMEText(body)
    msg['Subject'] = "Daily Market Update"
    msg['From'] = sender_email
    msg['To'] = recipients_str

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    #data = fetch_and_format_data()
    cnbc_news = get_financial_news_from_rss()
    wsj_news = get_wsj_headlines()
    
    full_body = cnbc_news + wsj_news
    
    send_email(full_body)
