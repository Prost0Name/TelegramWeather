from tortoise.models import Model
from tortoise import fields


class Users(Model):
    telegram_id = fields.IntField(null=False, pk=True, unique=True)
    username = fields.CharField(max_length=255, null=False)
    

    class Meta:
        table = "users"
        app = "models_users"
