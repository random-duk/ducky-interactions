from classes.command import Command
from classes.command import ApplicationCommandType

from classes.response import InteractionResponse

from quart import current_app


class Invite(Command):
    async def execute(self, context, **kwargs) -> InteractionResponse:
        return await context.respond(content='https://discord.com/oauth2/authorize?client_id=426787835044036610&permissions=0&scope=bot+applications.commands')


def setup():
    current_app.register_command(Invite('invite', 'Sends the invite link', ApplicationCommandType.CHAT_INPUT))
