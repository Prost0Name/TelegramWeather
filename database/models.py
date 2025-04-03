from tortoise.models import Model
from tortoise import fields


class Users(Model):
    telegram_id = fields.IntField(null=False, pk=True, unique=True)
    username = fields.CharField(max_length=255, null=True)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    city = fields.CharField(max_length=255, null=True)
    notification_time = fields.CharField(max_length=5, null=True)  # Формат "HH:MM"
    notifications_enabled = fields.BooleanField(default=False)

    class Meta:
        table = "users"
        app = "models_users"
