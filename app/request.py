from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import Channel, Chat, User, PeerUser

from .models import Users, Messages


class Connection(TelegramClient):
    def __init__(self, api_hash, api_id, phone):
        super(Connection, self).__init__(session=phone, api_hash=api_hash, api_id=api_id)
        self.phone = phone
        self.me = None

    async def get_code(self):
        return await self.send_code_request(self.phone)

    async def login(self, code=None, password=None):
        await self.connect()
        if not self.is_user_authorized():
            try:
                await self.sign_in(phone=self.phone, code=code)
            except SessionPasswordNeededError:
                await self.sign_in(phone=self.phone, code=code, password=password)
        me = await self.get_me()

        # me = Users.get_users(me.id)

        me = Users.save_user(user_id=me.id, first_name=me.first_name)
        self.me = me
        return self

    async def messages(self, limit=100):
        dialogs = await self.get_dialogs(limit=limit)
        messages = None
        mssgs = []
        for dialog in dialogs:
            user = dialog.entity
            if (not isinstance(user, (Channel, Chat))) and user.first_name.find("bot") < 0 and (not user.is_self):

                new_user = await Users.save_user(user.id, user.first_name)

                messages = await self.get_messages(user, limit=limit)
                for message in messages:
                    mssgs.append(message)
        for message in mssgs:
            fro_user = None
            to_user = None
            fro_entity = await self.get_entity(entity=PeerUser(user_id=message.from_id))
            print("from user:{}, message :{}".format(fro_entity.username, message.message))
            if isinstance(fro_entity, User):
                fro_user = await Users.save_user(user_id=fro_entity.id, first_name=fro_entity.first_name)
            t_entity = await self.get_entity(entity=message.to_id)
            if isinstance(t_entity, User):
                to_user = await Users.save_user(user_id=t_entity.id, first_name=t_entity.first_name)
            print("to user:{}".format(t_entity.username))
            msg = await Messages.save_message(message_id=message.id, from_user=fro_user[0], to_user=to_user[0],
                                              ts_created=message.date, message=message)
        return len(mssgs)
