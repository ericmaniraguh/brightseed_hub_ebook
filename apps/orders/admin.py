from django.contrib import admin
from .models import Purchase

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'payment_status', 'payment_method', 'purchased_at')
    list_filter = ('payment_status', 'payment_method')
