from classes.command import Command
from classes.command import ApplicationCommandType, ApplicationCommandOptionType, ApplicationCommandOption, ApplicationCommandOptionChoice

from classes.response import InteractionResponse

from classes.embed import Embed

from quart import current_app


class HTTPDuck(Command):
    async def execute(self, context, http_code: int = None) -> InteractionResponse:
        codes = {100: "Continue", 200: "OK", 301: "Moved Permanently", 302: "Found", 400: "Bad Request",
                 403: "Forbidden", 404: "Not Found", 409: "Conflict", 413: "Request Entity Too Large",
                 418: "I'm a teapot", 420: "Enhance your calm", 426: "Upgrade Required", 429: "Too Many Requests",
                 451: "Unavailable for legal reasons", 500: "Internal Server Error"}
        embed = Embed(title=f'{http_code}: {codes[http_code]}', color=3553598)
        embed.set_image(url=f'https://random-d.uk/api/http/{http_code}')
        embed.set_footer('Powered by random-d.uk')
        return await context.respond(embeds=[embed])


def setup():
    choices = []
    for code in ('100', '200', '301', '302', '400', '403', '404', '409', '413', '418', '420', '426', '429', '451',
                 '500'):
        choices.append(ApplicationCommandOptionChoice(name=code, value=int(code)))
    option = ApplicationCommandOption(option_type=ApplicationCommandOptionType.NUMBER, name='http_code',
                                      description='Choose the HTTP code of the duck you want!',
                                      required=True, choices=choices)
    current_app.register_command(HTTPDuck('httpduck', 'Show you a cute duck', ApplicationCommandType.CHAT_INPUT, options=[option]))
