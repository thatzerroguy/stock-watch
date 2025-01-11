from django.shortcuts import render
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
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            messages.success(request, 'Stock added to watchlist!')
            return redirect('watchlist')
    else:
        form = StockForm()

    stocks = Stock.objects.filter(user=request.user)
    return render(request, 'stocks/watchlist.html', {'form': form, 'stocks': stocks})


@login_required
def delete_stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id, user=request.user)
    stock.delete()
    messages.success(request, 'Stock removed from watchlist!')
    return redirect('watchlist')