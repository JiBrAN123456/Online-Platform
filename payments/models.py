from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()




class Transaction:
     
    STATUS_CHOICES = (("Initiated","INITIATED"),
                      ("completed","COMPLETED"),
                      ("Failed","FAILED"),
                      ("refunded","Refunded"))
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "transaction")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20 , choices= STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (f"{self.user.email} -{self.amount} is {self.status}")


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('crypto', 'Crypto'),
        ("razorpay", "Razorpay")
    ]

    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_reference = models.CharField(max_length=100, unique=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction.user.email} - {self.payment_method} - {self.payment_reference}"

    