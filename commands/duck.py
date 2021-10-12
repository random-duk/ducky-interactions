from classes.command import Command
from classes.command import ApplicationCommandType

from classes.response import InteractionResponse

from classes.embed import Embed

from time import time

from quart import current_app


class Duck(Command):
    async def execute(self, context, **kwargs) -> InteractionResponse:
        em = Embed(title=':duck: QUACK! A random duck for you!', color=3553598)
        em.set_image(url=f'https://random-d.uk/api/v2/randomimg?t={int(time())}')
        em.set_footer('Powered by random-d.uk')
        return await context.respond(embeds=[em])


def setup():
    current_app.register_command(Duck('duck', 'Show you a cute duck', ApplicationCommandType.CHAT_INPUT))
