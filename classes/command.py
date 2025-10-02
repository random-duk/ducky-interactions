from decimal import Decimal
from enum import Enum
from typing import Union, List, Set, Tuple

from classes.response import InteractionResponse


class ApplicationCommandType(Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class ApplicationCommandOptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10


class ApplicationCommandOptionChoice:
    def __init__(self, name: str, value: Union[str, int, Decimal, float]):
        self.name = name
        self.value = value

    def to_json(self):
        return {"name": self.name, "value": self.value}


class ApplicationCommandOption:
    def __init__(self, option_type: ApplicationCommandOptionType, name: str, description: str = None, required: bool = False,
                 choices: Union[List[ApplicationCommandOptionChoice], Set[ApplicationCommandOptionChoice],
                                Tuple[ApplicationCommandOptionChoice]] = None, options: Union[List, Set, Tuple] = None):
        self.type = option_type
        self.name = name
        self.description = description
        self.required = required
        self.choices = choices
        self.options = options

    def to_json(self):
        data = {"type": self.type.value, "name": self.name, "required": self.required}
        if self.description:
            data['description'] = self.description
        if self.choices:
            data["choices"] = [choice.to_json() for choice in self.choices]
        if self.options:
            data["options"] = [option.to_json() for option in self.options]
        return data


class Command:
    def __init__(self, name: str, description: str = None, command_type: ApplicationCommandType = 1,
                 options: Union[List[ApplicationCommandOption], Set[ApplicationCommandOption],
                                Tuple[ApplicationCommandOption]] = None):
        self.type = command_type
        self.name = name

        self.description = description
        self.options = options

    async def execute(self, context, **kwargs) -> InteractionResponse:
        pass

    def to_json(self):
        data = {"type": self.type.value, "name": self.name, "contexts": [0,1,2],"integration_types": [0,1]}
        if self.description:
            data['description'] = self.description
        if self.options:
            data['options'] = [option.to_json() for option in self.options]
        return data
