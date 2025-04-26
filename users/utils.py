from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings
from .models import UserActivityLog
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


signer = TimestampSigner()


def generate_verification_token(email):
    return signer.sign(email)


def verify_token(token,duration=3600):
    try:
        email = signer.unsign(token, max_age=duration)
        return email
    except (BadSignature, SignatureExpired):
        return None
    


def log_user_activity(user, request, activity_type):
    ip = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    UserActivityLog.objects.create(
        user=user,
        activity_type=activity_type,
        ip_address=ip,
        user_agent=user_agent
    )







def send_realtime_notification(user_id, title, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "content": {
                "title": title,
                "message": message,
            }
        }
    )    