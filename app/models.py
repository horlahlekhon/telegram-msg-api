from tortoise import Model, fields
from tortoise.exceptions import DoesNotExist
from tortoise.queryset import Q


class Users(Model):
    
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    first_name = fields.CharField(max_length=100)

    @classmethod
    async def save_user(cls, user_id, first_name):
        """
        Args:
            user_id:
            first_name:
        """
        user = await Users.get_or_create(first_name=first_name, user_id=user_id)
        return user

    @classmethod
    async def get_users(cls, user_id=None):
        """
        Args:
            user_id:
        """
        if user_id:
            try:
                user = await Users.filter(Q(user_id=user_id)).first()
            except DoesNotExist:
                raise DoesNotExist
        return await Users.all()


class Messages(Model):
    id = fields.IntField(pk=True)
    message_id = fields.IntField(unique=True)
    from_user = fields.IntField()
    ts_created = fields.DatetimeField()
    message = fields.TextField(null=True)
    to_user = fields.IntField()

    @classmethod
    async def save_message(cls, message_id, from_user, ts_created, message, to_user):

        """
        Args:
            message_id:
            from_user:
            ts_created:
            message:
            to_user:
        """
        messg = Messages.filter(Q(message_id=message_id)).first()
        if isinstance(messg, Messages):
            return messg
        else:
            message = await Messages.get_or_create(message_id=message_id,
                                                   from_user=from_user.user_id,
                                                   ts_created=ts_created,
                                                   message=message.message,
                                                   to_user=to_user.user_id)
            return message

    @classmethod
    async def get_messages(cls, me: str, message_id=None, to_user=None, from_user=None, limit=100):

        """
        Args:
            me (str):
            message_id:
            to_user:
            from_user:
            limit:
        """
        if message_id:
            message = await Messages.filter(Q(message_id=message_id)).first()
            if message:
                return message
            else:
                return None
        elif from_user and to_user:
            messages = await Messages.filter(Q(to_user=to_user) | Q(from_user=from_user))
            return messages
        return await Messages.filter(Q(to_user=int(me)) | Q(from_user=int(me))).limit(limit=limit)

    # def update_message(self):
    #     return Messages.query.where(self.message_id).update(message=self.message)
