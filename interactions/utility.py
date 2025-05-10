# interactions/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

def create_notification(recipient, actor, verb, target=None, description=None, url=None):
 
    content_type = ContentType.objects.get_for_model(target) if target else None
    object_id = target.id if target else None


    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=object_id,
        description =description,
        url= url
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}",  # group name
        {
            "type": "send_notification",
            "notification": {
                "id": notification.id,
                "actor": actor.username,
                "verb": verb,
                "description": description,
                "timestamp": str(notification.timestamp),
                "url": url,
            }
        }
    )
