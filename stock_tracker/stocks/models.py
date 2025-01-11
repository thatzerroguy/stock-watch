from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)
    last_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'symbol')

    def __str__(self):
        return f"{self.symbol} - {self.company_name}"