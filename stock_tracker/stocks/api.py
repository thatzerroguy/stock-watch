import requests
from django.conf import settings


def fetch_stock_data(symbol):
    # Using Alpha Vantage API as an example
    api_key = settings.ALPHA_VANTAGE_API_KEY
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'symbol': symbol,
            'price': data['Global Quote']['05. price'],
            'change': data['Global Quote']['09. change'],
            'change_percent': data['Global Quote']['10. change percent'],
        }
    return None