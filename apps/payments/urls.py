from django.urls import path
from .views import MockPaymentProcessView

urlpatterns = [
    path('process/', MockPaymentProcessView.as_view(), name='payment-process'),
]
