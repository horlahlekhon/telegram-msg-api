from app import app
from quart import (
     request, Blueprint, json, Response, session, )
from .request import Connection
from .controller import (get_all_messages, get_all_users, login)
from .models import Users, Messages


deep = Blueprint('telegram', __name__, url_prefix='/telegram')
neutral = Blueprint('retrieve',__name__, url_prefix='/data')


@deep.before_app_first_request
async def start_up():
    global client
    api_hash = session.get("api_hash")
    phone = session.get("phone")
    api_id = session.get("api_id")
    client = Connection(api_hash=api_hash, api_id=api_id, phone=phone)
    await client.connect()


@app.after_serving
async def cleanup():
    await client.disconnect()

@neutral.route('/get-data', strict_slashes=False, methods=['POST'])
async def get_data():
    data = await request.get_json()
    session["api_id"] = data.get("api_id")
    session["api_hash"] = data.get("api_hash")
    session["phone"] = data.get("phone")
    return Response(status=200, response="")


@deep.route('/sign-in', strict_slashes=False, methods=['POST', 'GET'])
async def sign_in():
    data = await request.get_json()
    if not data:
        resp, _, stat_code = await login(client=client, phone=session.get("phone"))
        return Response(status=stat_code, response=resp)
    resp, mee, stat_code = await login(client=client, code=data.get("code"))
    if isinstance(mee, Users):
        usrs = await get_all_users(user_id=mee.id)
        session["me"] = usrs.user_id
        return Response(status=stat_code, response=resp)
    else:
        return Response(status=stat_code, response=resp)


@deep.route('/get-messages', strict_slashes=False, methods=['GET'])
async def get_messages():
    data = await request.get_json()
    if data.get("to_user") and data.get("from_user"):
        msgs = await get_all_messages(to_user=data.get("to_user"), from_user=data.get("from_user"))
        return Response(status=200, response=json.dumps(msgs))
    elif data.get("user") and data.get("limit"):
        msgs = await get_all_messages(me=data.get("user"), limit=data.get("limit"))
        return Response(status=200, response=json.dumps(msgs))
    resp = {"status": "failed", "message" : "You will need at least a user and limit to be able to get messages. "}
    return Response(status=400, response=json.dumps(resp))


@deep.route('/who-am-i', strict_slashes=False, methods=['GET'])
async def me():
    mee = await client.get_me()
    return Response(status=200, response=json.dumps(mee.to_dict()))

@deep.route('/messages/fetch', strict_slashes=False, methods=['GET'])
async def fetch():
    await client.connect()
    msgs = await client.messages(limit=500)
    return Response(status=200, response=json.dumps({"status" : "success", "message" : "{} messages pulled".format(msgs)}))