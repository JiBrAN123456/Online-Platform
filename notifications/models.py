from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


# notifications/models.py

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_from_ws'  # changed this line
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"To: {self.user.username} - {self.message[:30]}"
