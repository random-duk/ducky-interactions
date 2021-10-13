from quart import current_app

from time import time

from classes.components import ComponentInteraction, Button, ButtonStyle

from classes.response import InteractionResponse
from classes.embed import Embed
import asyncio


class NewDuck(ComponentInteraction):
    async def execute(self, context, **kwargs) -> InteractionResponse:
        em = Embed(title=':duck: QUACK! A random duck for you!', color=3553598)
        em.set_image(url=f'https://random-d.uk/api/v2/randomimg?t={int(time())}')
        em.set_footer('Powered by random-d.uk')
        button = Button(style=ButtonStyle.PRIMARY, label='Get me another duck', emoji={"id": None, "name": "🦆"}, custom_id='duck-button')
        return await context.respond(embeds=[em], components=button)


def setup():
    current_app.register_component_interaction(NewDuck('duck-button'))