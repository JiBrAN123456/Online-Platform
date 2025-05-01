from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification_to_user(user_id, content):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send.notification",
            "content": content
        }
    )
