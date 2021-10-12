from typing import Union

from classes.response import InteractionResponse, InteractionCallbackData, InteractionCallbackType, InteractionCallbackDataFlags

from classes.member import Member
from classes.user import User


class Context:
    def __init__(self, http, interaction):
        self._acked = False

        self.http = http
        self.interaction = interaction
        self.interaction_id = int(interaction['id'])
        self.application_id = int(interaction['application_id'])
        self.interaction_token = interaction['token']

    @property
    def guild_id(self) -> int:
        return int(self.interaction['guild_id']) if 'guild_id' in self.interaction else None

    @property
    def channel_id(self) -> int:
        return int(self.interaction['channel_id']) if 'channel_id' in self.interaction else None

    @property
    def author(self) -> Union[Member, User]:
        return Member(self.interaction['member']) if 'member' in self.interaction else User(self.interaction['user'])

    @property
    def message(self) -> dict:
        return self.interaction['message'] if 'message' in self.interaction else None

    async def respond(self, content=None, embeds=None, ephemeral=False):
        if ephemeral:
            ephemeral = InteractionCallbackDataFlags.EPHEMERAL.value
        else:
            ephemeral = 0
        data = InteractionCallbackData(content=content, embeds=embeds, flags=ephemeral)
        if not self._acked:
            return InteractionResponse(InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE, data)
        else:
            await self.http.request('POST', f'/webhooks/{self.application_id}/{self.interaction_token}', json=data)
