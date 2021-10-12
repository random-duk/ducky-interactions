from datetime import datetime


class Embed:
    def __init__(self, title: str = '', embed_type: str = 'rich', description: str = '', url: str = '',
                 timestamp: datetime = None, color: int = 0):
        self.title = title
        self.type = embed_type
        self.description = description
        self.url = url
        self.timestamp: datetime = timestamp
        self.color = color
        self._footer = None
        self._image = None
        self._thumbnail = None
        self._video = None
        self._provider = None
        self._author = None
        self._fields = list()

    def set_thumbnail(self, url):
        self._thumbnail = {"url": url}

    def set_video(self, url):
        self._video = {"url": url}

    def set_image(self, url):
        self._image = {"url": url}

    def set_provider(self, name, url):
        self._provider = {"name": name, "url": url}

    def set_author(self, name, url='', icon_url=''):
        self._author = {"name": name}
        if url:
            self._author['url'] = url
        if icon_url:
            self._author['icon_url'] = icon_url

    def set_footer(self, text, icon_url=''):
        self._footer = {"text": text}
        if icon_url:
            self._footer['icon_url'] = icon_url

    def add_field(self, name, value, inline=False):
        self._fields.append({"name": name, "value": value, "inline": inline})

    def to_json(self):
        data = dict(type=self.type)
        if self.title:
            data['title'] = self.title
        if self.description:
            data['description'] = self.description
        if self.url:
            data['url'] = self.url
        if self.timestamp:
            data['timestamp'] = self.timestamp.timestamp()
        if self.color:
            data['color'] = self.color
        if self._footer:
            data['footer'] = self._footer
        if self._image:
            data['type'] = 'image'
            data['image'] = self._image
        if self._video:
            data['type'] = 'video'
            data['video'] = self._video
        if self._provider:
            data['type'] = 'article'
            data['provider'] = self._provider
        if self._author:
            data['author'] = self._author
        if self._fields and len(self._fields) > 0:
            data['fields'] = self._fields
        return data

