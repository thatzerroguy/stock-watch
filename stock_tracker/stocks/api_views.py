from django.http import JsonResponse
import yfinance as yf
from yahoo_fin import stock_info
import json


def search_stocks(request):
    query = request.GET.get('q', '').upper()
    if not query:
        return JsonResponse([], safe=False)

    try:
        # Search for stocks matching the query
        matches = stock_info.tickers_nasdaq() + stock_info.tickers_sp500() + stock_info.tickers_dow()
        matches = [t for t in matches if query in t.upper()]

        # Limit results to first 5 matches
        matches = matches[:5]

        results = []
        for symbol in matches:
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                results.append({
                    'symbol': symbol,
                    'name': info.get('longName', info.get('shortName', symbol))
                })
            except:
                continue

        return JsonResponse(results, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)