from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
import base64

fernet = Fernet(settings.FIELD_ENCRYPTION_KEY)

class EncryptedCharField(models.CharField):
    def get_prep_value(self, value):
        if value is None:
            return value
        return fernet.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return fernet.decrypt(value.encode()).decode()
        except Exception:
            return value  # fallback if decrypt fails

    def to_python(self, value):
        if value is None:
            return value
        try:
            return fernet.decrypt(value.encode()).decode()
        except Exception:
            return value  # used when editing in admin, etc.
