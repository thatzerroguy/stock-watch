from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, StockForm
from .models import Stock
from .api import fetch_stock_data

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'stocks/register.html', {'form': form})


@login_required
def dashboard(request):
    stocks = Stock.objects.filter(user=request.user)
    stock_data = []

    for stock in stocks:
        data = fetch_stock_data(stock.symbol)
        if data:
            stock_data.append(data)

    return render(request, 'stocks/dashboard.html', {'stocks': stock_data})


@login_required
def watchlist(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol', '').upper()
        if symbol:
            # Fetch stock data first to validate and get company name
            stock_data = fetch_stock_data(symbol)
            if stock_data:
                stock, created = Stock.objects.get_or_create(
                    user=request.user,
                    symbol=symbol,
                    defaults={
                        'company_name': stock_data['company_name'],
                        'last_price': stock_data['price']
                    }
                )
                if created:
                    messages.success(request, f'Added {symbol} to your watchlist!')
                else:
                    messages.info(request, f'{symbol} is already in your watchlist!')
            else:
                messages.error(request, f'Could not find stock with symbol {symbol}')
        return redirect('watchlist')

    stocks = Stock.objects.filter(user=request.user)
    return render(request, 'stocks/watchlist.html', {
        'stocks': stocks,
    })


@login_required
def delete_stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id, user=request.user)
    stock.delete()
    messages.success(request, 'Stock removed from watchlist!')
    return redirect('watchlist')