# Generated by Django 5.2 on 2025-05-07 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("courses", "0003_enrollment_progress_enrollment_status_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=8)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Initiated", "INITIATED"),
                            ("completed", "COMPLETED"),
                            ("Failed", "FAILED"),
                            ("refunded", "Refunded"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="courses.course"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transaction",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("card", "Card"),
                            ("paypal", "PayPal"),
                            ("stripe", "Stripe"),
                            ("crypto", "Crypto"),
                            ("razorpay", "Razorpay"),
                        ],
                        default="Crypto",
                        max_length=20,
                    ),
                ),
                (
                    "payment_reference",
                    models.CharField(max_length=100, null=True, unique=True),
                ),
                ("paid_at", models.DateTimeField(auto_now_add=True)),
                (
                    "transaction",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment",
                        to="payments.transaction",
                    ),
                ),
            ],
        ),
    ]
