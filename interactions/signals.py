from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LessonComment, Notification
from django.contrib.contenttypes.models import ContentType

def send_notification_to_user(user_id, content):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send.notification",
            "content": content
        }
    )
