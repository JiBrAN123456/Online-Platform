from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from django.utils import timezone

User = get_user_model()




class Transaction(models.Model):
     
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

    transaction = models.OneToOneField('payments.Transaction', on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES , default= "Crypto")
    payment_reference = models.CharField(max_length=100, unique=True, null=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"{self.transaction.user.email} - {self.payment_method} - {self.payment_reference}"

    
class Coupon(models.Model):
    code = models.CharField(max_length=20 , unique=True)
    discount_percent = models.PositiveBigIntegerField(help_text="Enter discount as a percentage (e.g., 10 for 10%)")
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank for unlimited use")
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()    


    def is_valid(self):
        now = timezone.now()
        return(
            self.active
            and self.valid_from <= now <= self.valid_to
            and (self.usage_limit is None or self.used_count < self.usage_limit)
        )
    
    def __str__(self):
        return self.code