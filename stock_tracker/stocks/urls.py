from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # This imports views from the stocks app

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'),
    path('login/', auth_views.LoginView.as_view(template_name='stocks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]