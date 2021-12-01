from datetime import datetime, timedelta
from django.conf import settings
import jwt


def generate_confirmation_token(pk):
    payload = {
        'confirm': pk,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=3)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return token


def generate_password_token(pk):
    payload = {
        'confirm': pk,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=3)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return token
