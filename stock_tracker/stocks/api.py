import requests
from django.conf import settings
import yfinance as yf

def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        return {
            'symbol': symbol,
            'price': info.get('currentPrice', 0),
            'change': info.get('regularMarketChange', 0),
            'change_percent': info.get('regularMarketChangePercent', 0),
            'company_name': info.get('longName', symbol)
        }
    except:
        return None