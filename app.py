from quart import Quart, request, g, current_app, abort, jsonify
import asyncio

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from importlib import import_module
import os
import sys
from time import perf_counter

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from modules.http import HTTP
from classes.context import Context

config = json.load(open('config.json'))

TOKEN = config['discord']['token']
CLIENT_ID = config['discord']['client_id']
PUBLIC_KEY = config['discord']['public_key']

app = Quart(__name__)


@app.before_serving
async def on_startup():
    app.http = HTTP(token=TOKEN)
    app.commands = dict()
    app.component_interactions = dict()
    app.register_command = register_command
    app.register_component_interaction = register_component_interaction
    load_commands()
    load_component_interactions()
    await upload_commands()


@app.route('/interactions', methods=['POST'])
async def interaction():
    start_time = perf_counter()
    verify_key((await request.data).decode(), request.headers)
    body = await request.json
    if body['type'] == 1:
        return jsonify({"type": 1})
    elif body['type'] == 2:
        name = body['data']['name']
        command = current_app.commands.get(name)
        context = Context(2, current_app.http, body)
        args = body['data'].get('options', ())
        kwargs = {}
        for arg in args:
            kwargs[arg['name']] = arg['value']
        task = asyncio.create_task(command.execute(context, **kwargs))
        while True:
            if not task.done():
                if perf_counter() - start_time <= 2.5:
                    await asyncio.sleep(.1)
                else:
                    context._acked = True
                    return jsonify(({"type": 5}))
            else:
                if task.exception():
                    raise task.exception()
                return jsonify(task.result().to_json())
    elif body['type'] == 3:
        if not getattr(g, 'received_buttons', None):
            g.received_buttons = list()
        name = body['data']['custom_id']
        component_interaction = current_app.component_interactions.get(name)
        context = Context(3, current_app.http, body)
        task = asyncio.create_task(component_interaction.execute(context))
        while True:
            if not task.done():
                if perf_counter() - start_time <= 2.5:
                    await asyncio.sleep(.1)
                else:
                    context._acked = True
                    return jsonify(({"type": 6}))
            else:
                if task.exception():
                    raise task.exception()
                return jsonify(task.result().to_json())



def verify_key(body, headers):
    key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')
    try:
        key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        abort(401, 'invalid request signature')


def register_command(command):
    current_app.commands[command.name] = command


def register_component_interaction(component_interaction):
    current_app.component_interactions[component_interaction.name] = component_interaction


def load_commands():
    for _, _, files in os.walk('commands'):
        for file in files:
            if file.endswith('.py'):
                file = file.split('.py')[0]
                import_module(f'commands.{file}')
                sys.modules[f'commands.{file}'].setup()


def load_component_interactions():
    for _, _, files in os.walk('component_responses'):
        for file in files:
            if file.endswith('.py'):
                file = file.split('.py')[0]
                import_module(f'component_responses.{file}')
                sys.modules[f'component_responses.{file}'].setup()

async def upload_commands(guild_id=None):
    data = [command.to_json() for command in app.commands.values()]
    if guild_id:
        try:
            x = await app.http.request('PUT', f'/applications/{CLIENT_ID}/guilds/{guild_id}/commands', json=data)
        except Exception as e:
            print(e)
    else:
        try:
            x = await app.http.request('PUT', f'/applications/{CLIENT_ID}/commands', json=data)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app.run(port=9000)