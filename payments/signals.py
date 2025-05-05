from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from courses.models import Enrollment
from django.core.exceptions import ObjectDoesNotExist


def enroll_user_on_successful_payment(sender, instance, created, **kwargs):
    if instance.status == "completed":
        try:
           Enrollment.objects.get_or_create(
               student= instance.user,
               course =instance.course,
               defaults= {"status": "Active"},
           )
        except ObjectDoesNotExist:
           pass   