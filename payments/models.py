from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):

    PAYMENT_GATEWAY_OPTION = (("PAYPAL","Paypal"),
                              ("RAZORPAY","Razorpay"))
    
    STATUS_CHOICES = (("Initiated","INITIATED"),
                      ("completed","COMPLETED"),
                      ("Failed","FAILED"))
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gateway = models.CharField(max_length=20 , choices= PAYMENT_GATEWAY_OPTION)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10 , default="INR")
    status = models.CharField(max_length=100 , blank=True , null = True)
    transaction_id = models.CharField(max_length=100 , blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
          return f"{self.user.email} - {self.gateway} - {self.status}"