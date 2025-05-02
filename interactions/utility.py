from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None, description=None, url=None):
 
    content_type = ContentType.objects.get_for_model(target) if target else None
    object_id = target.id if target else None


    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=object_id,
        description =description,
        url= url
    )
