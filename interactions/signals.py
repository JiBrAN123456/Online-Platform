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

@receiver(post_save, sender=LessonComment)
def notify_on_comment_reply(sender, instance, created, **kwargs):
    if created and instance.parent:
        parent_user = instance.parent.user
        if parent_user == instance.user:
            return  # Don't notify if user replies to their own comment

        # Create notification
        notif = Notification.objects.create(
            recipient=parent_user,
            actor=instance.user,
            verb="replied to your comment",
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            description=instance.comment,
            url=f"/lessons/{instance.lesson.id}/",  # adjust to your frontend URL pattern
            target="LessonComment"
        )

        # Send real-time WebSocket message
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{parent_user.id}",
            {
                "type": "notify",
                "message": f"{instance.user.username} replied: {instance.comment[:50]}...",
                "url": notif.url
            }
        )
