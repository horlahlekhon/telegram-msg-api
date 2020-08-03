from .request import Connection
import json
from tortoise.exceptions import DoesNotExist
from .models import Messages, Users
from telethon.errors.rpcbaseerrors import FloodError
from .request import Connection


async def get_all_messages(me: Users = None, message_id=None, to_user=None, from_user=None, limit=200):
    msgs = await Messages.get_messages(me=me, message_id=message_id, to_user=to_user, from_user=from_user, limit=limit)
    print("leeeeeeeeeeeeeeeeeeeen", len(msgs))
    return [i.__dict__ for i in msgs]

async def get_all_users(user_id=None):
    if user_id:
        try:
            user = await Users.get_users(user_id=user_id)
        except DoesNotExist:
            return {"status" : "failed", "message": "User does not exist"}
    usrs = await Users.get_users()
    return usrs

async def login(client: Connection, code=None, phone=None):
    if not code and phone:
        try:
            await client.send_code_request(phone)
            resp = json.dumps({"status" : "incompleted", "message": "Kindly call this endpoint again with the sms code "})
            return resp, _, 200
        except FloodError as e:
            resp = json.dumps({"status":"failed", "message" : "You are requesting for code too frequently", "traceback" : e.message})
            return resp, _, e.code
    await client.sign_in(code=code)
    messages = []
    if await client.is_user_authorized():
        dialog = (await client.get_dialogs())[0]
        async for m in client.iter_messages(dialog, 10):
            messages.append(m.to_dict())
        resp = json.dumps(messages)
        me = await client.get_entity(entity='me')
        return resp, me, 200
    else:
        return json.dumps({"status":"failure", "message":"Invalid code"}), _, 400



