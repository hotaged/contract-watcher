from tortoise import models, fields
from passlib.context import CryptContext

pwd = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)


class User(models.Model):
    id = fields.IntField(pk=True)

    username = fields.CharField(max_length=256, null=False, unique=True)
    password = fields.CharField(max_length=64, null=False)

    webhooks: fields.ReverseRelation['Webhook']
    history: fields.ReverseRelation['History']

    @staticmethod
    async def create_with_encrypted_password(username: str, password: str) -> 'User':
        return await User.create(username=username, password=pwd.hash(password))

    async def change_password(self, password: str) -> 'User':
        self.password = pwd.hash(password)
        await self.save()
        return self

    def verify_password(self, password: str) -> bool:
        return pwd.verify(password, self.password)


class Webhook(models.Model):
    id = fields.IntField(pk=True)

    address = fields.CharField(max_length=256, null=False)
    event = fields.CharField(max_length=256, null=False)
    url = fields.CharField(max_length=2048, null=False)
    label = fields.CharField(max_length=64, null=False)
    active = fields.BooleanField(default=True)

    abi = fields.JSONField(null=False)

    user = fields.ForeignKeyField(
        'models.User',
        related_name='webhooks',
        null=False,
        on_delete=fields.CASCADE
    )

    history: fields.ReverseRelation['History']

    async def create_log_history(self, log: dict, sent: bool):
        await self.fetch_related('user')
        return await History.create(
            log=log,
            transaction_hash=log['transactionHash'],
            user=self.user,
            webhook=self,
            sent=sent
        )


class History(models.Model):
    id = fields.IntField(pk=True)
    log = fields.JSONField(null=False)

    transaction_hash = fields.CharField(max_length=256, null=False)

    user = fields.ForeignKeyField(
        'models.User',
        related_name='history',
        null=False,
        on_delete=fields.CASCADE)

    webhook = fields.ForeignKeyField(
        'models.Webhook',
        related_name='history',
        null=False,
        on_delete=fields.CASCADE)

    created_at = fields.DatetimeField(auto_now_add=True)

    sent = fields.BooleanField(default=False)
