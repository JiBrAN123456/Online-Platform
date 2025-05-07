from django.urls import path
from .views import CreatePaymentView , CreatePaymentIntentView , StripeWebhookView
from . import views

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create-payment'),
    path('create-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('start/', views.create_payment_view, name='create-payment'),
]
