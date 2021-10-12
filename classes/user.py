from modules.utils import snowflake_to_datetime


class User:
    def __init__(self, raw_user):
        self.id = int(raw_user['id'])
        self.username = raw_user['username']
        self.discriminator = raw_user['discriminator']
        self.avatar = raw_user['avatar']
        self.bot = raw_user.get('bot', False)
        self.system = raw_user.get('system', False)
        self.created_at = snowflake_to_datetime(self.id)

    def __str__(self):
        return f'{self.username}#{self.discriminator}'

    def __int__(self):
        return self.id