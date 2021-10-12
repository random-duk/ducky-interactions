import aiohttp

try:
    import ujson as json
except ModuleNotFoundError:
    import json


class HTTP:
    def __init__(self, token):
        self.token = token

        config = json.load(open('config.json'))

        CLIENT_ID = config['discord']['client_id']
        CLIENT_SECRET = config['discord']['client_secret']

        TOKEN = config['discord']['token']
        USER_AGENT = "DuckyBot/aiohttp/python"

        self.base_url = 'https://discordapp.com/api'

        headers = {"User-Agent": USER_AGENT, "Authorization": f"Bot {TOKEN}"}

        self.session = aiohttp.ClientSession(headers=headers, json_serialize=json.dumps, )

    async def request(self, method, uri, **kwargs):
        request = await self.session.request(method, self.base_url + uri, **kwargs)
        if request.status == 200 and request.headers.get('content-type') == 'application/json':
            return await request.json()
        elif request.status == 400 and request.headers.get('content-type') == 'application/json':
            return await request.json()
        else:
            return request


