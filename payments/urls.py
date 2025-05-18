# payments/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CreateStripePaymentIntentView,
    StripeWebhookView,
    create_paypal_payment,
    capture_paypal_order,
    TransactionViewSet,
    
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('stripe/create-intent/', CreateStripePaymentIntentView.as_view(), name='create-stripe-intent'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('paypal/create-payment/', create_paypal_payment, name='create-paypal-payment'),
    path('paypal/capture/', capture_paypal_order, name='capture-paypal-order'),
    path('create-razorpay-order/', CreateRazorpayOrderView.as_view()),
    path('webhook/razorpay/', razorpay_webhook),
]

urlpatterns += router.urls
