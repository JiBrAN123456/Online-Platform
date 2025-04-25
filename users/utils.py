from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings
from .models import UserActivityLog



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