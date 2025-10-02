from classes.command import Command
from classes.command import ApplicationCommandType, ApplicationCommandOptionType, ApplicationCommandOption, ApplicationCommandOptionChoice

from classes.response import InteractionResponse

from classes.embed import Embed

from quart import current_app


class GetDuck(Command):
    async def execute(self, context, number: int = None, type = None) -> InteractionResponse:
        list = await context.http.request('GET', 'https://random-d.uk/api/list')
        if type == 'jpg':
            if f'{number}.{type}' not in list['images']:
                return await context.respond(content="Sorry, We don't have a picture with this number!", ephemeral=True)
        if type == 'gif':
            if f'{number}.{type}' not in list['gifs']:
                return await context.respond(content="Sorry, We don't have a gif with this number!", ephemeral=True)
        embed = Embed(title=':duck: There you go, just the duck you wanted!', color=3553598)
        embed.set_image(url=f'https://random-d.uk/api/{number}.{type}')
        embed.set_footer('Powered by random-d.uk')
        return await context.respond(embeds=[embed])


def setup():
    option_2 = ApplicationCommandOption(option_type=ApplicationCommandOptionType.STRING, name='type',
                                        description='Choose between gif or image', required=True,
                                        choices=[ApplicationCommandOptionChoice(name='GIF', value='gif'),
                                                 ApplicationCommandOptionChoice(name='Image', value='jpg')])
    option_1 = ApplicationCommandOption(option_type=ApplicationCommandOptionType.INTEGER, name='number',
                                        description='Choose the number of the specific image', required=True)
    current_app.register_command(GetDuck('getduck', 'Get a specific duck', ApplicationCommandType.CHAT_INPUT,
                                         options=[option_1, option_2]))
