from enum import Enum
from typing import Union, List

from classes.response import InteractionResponse

class ComponentType(Enum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3


class Component:
    def __init__(self, component_type):
        self.type = component_type.value


class ButtonStyle(Enum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class Button(Component):
    def __init__(self, custom_id: str, style: ButtonStyle, label: str, emoji: str = None, url: str = None, disabled: bool = False):
        super().__init__(ComponentType.BUTTON)
        self.custom_id = custom_id
        self.disabled = disabled
        self.style = style.value
        self.label = label
        self.emoji = emoji
        self.url = url

    def to_json(self):
        d = dict(type=self.type)
        d['custom_id'] = self.custom_id
        d['disabled'] = self.disabled
        d['style'] = self.style
        if not self.label and not self.emoji:
            return 'ERROR'  # TODO WRITE EXCEPTION
        if self.label:
            d['label'] = self.label
        if self.emoji:
            d['emoji'] = self.emoji
        if self.url:
            d['url'] = self.url
        return d


class SelectMenu(Component):
    def __init__(self, custom_id, disabled):
        super().__init__(ComponentType.SELECT_MENU)
        self.custom_id = custom_id
        self.disabled = disabled


class ActionRow(Component):
    def __init__(self):
        super().__init__(ComponentType.ACTION_ROW)
        self.components = []

    def add_components(self, components: Union[List[Union[Button, SelectMenu]], Button, SelectMenu] ):
        if len(self.components) >= 5:
            return 'ERROR'  # TODO WRITE EXCEPTION
        if isinstance(components, list):
            self.components += components
        elif isinstance(components, Button) or isinstance(components, SelectMenu):
            self.components.append(components)

    def to_json(self):
        return {"type": self.type, "components": [component.to_json() for component in self.components]}


class ComponentInteraction:
    def __init__(self, name: str):
        self.name = name

    async def execute(self, context, **kwargs) -> InteractionResponse:
        pass





