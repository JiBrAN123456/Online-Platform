from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings



signer = TimestampSigner()


def generate_verification_token(email):
    return signer.sign(email)


def verify_token(token,duration=3600):
    try:
        email = signer.unsign(token, max_age=duration)
        return email
    except (BadSignature, SignatureExpired):
        return None