from django.urls import path
from .views import CreatePaymentView , CreatePaymentIntentView

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create-payment'),
    path('create-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
]
