from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from ..core.config import settings

serializer = URLSafeTimedSerializer(settings.JWT_SECRET)


def create_reset_token(user_id: str) -> str:
    return serializer.dumps(user_id)


def verify_reset_token(token: str) -> str | None:
    try:
        return serializer.loads(token, max_age=settings.RESET_TOKEN_TTL_MIN * 60)
    except (BadSignature, SignatureExpired):
        return None
