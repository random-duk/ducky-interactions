from typing import Union

from classes.response import InteractionResponse, InteractionCallbackData, InteractionCallbackType, InteractionCallbackDataFlags

from classes.member import Member
from classes.user import User

from classes.components import ActionRow, Button, SelectMenu


class Context:
    def __init__(self, interaction_type, http, interaction):
        self._acked = False

        self.type = interaction_type

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

    async def respond(self, content=None, embeds=None, ephemeral=False, components=None):
        if ephemeral:
            ephemeral = InteractionCallbackDataFlags.EPHEMERAL.value
        else:
            ephemeral = 0
        if components:
            if isinstance(components, ActionRow):
                components = [components.to_json()]
            elif isinstance(components, Button) or isinstance(components, SelectMenu):
                row = ActionRow()
                row.add_components(components)
                components = [row]
            else:
                rows = []
                row = ActionRow()
                for i, component in enumerate(components):
                    if i % 5 == 0 and i != 0:
                        rows.append(row)
                        row = ActionRow()
                    row.add_components(component)
                components = rows
        data = InteractionCallbackData(content=content, embeds=embeds, flags=ephemeral, components=components)
        if self.type == 2:
            if not self._acked:
                return InteractionResponse(InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE, data)
            else:
                await self.http.request('POST', f'/webhooks/{self.application_id}/{self.interaction_token}', json=data)
        elif self.type == 3:
            if not self._acked:
                return InteractionResponse(InteractionCallbackType.UPDATE_MESSAGE, data)
            else:
                await self.http.request('PATCH', f'/webhooks/{self.application_id}/{self.interaction_token}/messages/@original', json=data.to_json())
