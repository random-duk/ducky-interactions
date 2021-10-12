from enum import Enum
from typing import Union, List, Set, Tuple


class InteractionCallbackType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7


class InteractionCallbackDataFlags(Enum):
    EPHEMERAL = 64


class InteractionCallbackData:
    def __init__(self,  content: str = '', embeds: Union[List, Set, Tuple] = None,
                 allowed_mentions: Union[List, Set, Tuple] = None, flags: int = 0,
                 components: Union[List, Set, Tuple] = None, tts: bool = False):

        self.tts = tts
        self.content = content
        self.embeds = embeds
        self.allowed_mentions = allowed_mentions
        self.flags = flags
        self.components = components

    def to_json(self):
        data = {"tts": self.tts}
        if self.content:
            data['content'] = self.content
        if self.embeds:
            data['embeds'] = [embed.to_json() for embed in self.embeds]
        if self.allowed_mentions:
            data['allowed_mentions'] = [allowed_mention.to_json() for allowed_mention in self.allowed_mentions]
        if self.flags:
            data['flags'] = self.flags
        if self.components:
            data['components'] = [component.to_json() for component in self.components]
        return data


class InteractionResponse:
    def __init__(self, callback_type: InteractionCallbackType, data: InteractionCallbackData = None):
        self.type = callback_type.value
        self.data = data

    def to_json(self):
        data = {"type": self.type}
        if self.data:
            data['data'] = self.data.to_json()
        return data
