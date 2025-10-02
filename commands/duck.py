from classes.command import Command
from classes.command import ApplicationCommandType

from classes.response import InteractionResponse

from classes.embed import Embed
from classes.components import Button, ButtonStyle

from time import time

from quart import current_app
from aiohttp import ClientSession


class Duck(Command):
    async def execute(self, context, **kwargs) -> InteractionResponse:
        async with ClientSession() as session:
            async with session.get("https://random-d.uk/api/quack", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0"}) as resp:
                j = await resp.json()
        em = Embed(title=':duck: QUACK! A random duck for you!', color=3553598)
        em.set_image(url=f'{j["url"]}')
        em.set_footer('Powered by random-d.uk')
        button = Button(style=ButtonStyle.PRIMARY, label='Get me another duck', emoji={"id": None, "name": "🦆"}, custom_id='duck-button')
        return await context.respond(embeds=[em], components=button)


def setup():
    current_app.register_command(Duck('duck', 'Show you a cute duck', ApplicationCommandType.CHAT_INPUT))
