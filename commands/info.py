from classes.command import Command
from classes.command import ApplicationCommandType

from classes.response import InteractionResponse

from classes.embed import Embed

from quart import current_app

from sys import version_info


class Info(Command):
    async def execute(self, context, **kwargs) -> InteractionResponse:
        owner = 'Auxim#0001'
        website = 'https://random-d.uk'
        embed = Embed(title='Statistics')
        embed.set_author(name='Ducky', icon_url='https://cdn.discordapp.com/avatars/426787835044036610/795ed0c0b2da8d6c37c071dc61e0c77f.png', url=website)
        embed.set_footer(text=f'My ID: {context.application_id}')
        embed.add_field(name='Python Version', value=f'{version_info[0]}.{version_info[1]}.{version_info[2]}', inline=True)
        embed.add_field('Interactions Version', '1.0', True)
        embed.add_field('Owner', owner, True)
        embed.add_field('Website', website, True)
        return await context.respond(embeds=[embed])


def setup():
    current_app.register_command(Info('info', 'Gives info about the bot', ApplicationCommandType.CHAT_INPUT))
