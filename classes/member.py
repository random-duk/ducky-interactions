from classes.user import User
from ciso8601 import parse_datetime


class Member(User):
    def __init__(self, raw_member):
        super().__init__(raw_member['user'])
        self.nick = raw_member.get('nick', '')
        self.joined_at = parse_datetime(raw_member.get('joined_at')) if 'joined_at' in raw_member else None
        self.premium_since = parse_datetime(raw_member.get('premium_since')) if raw_member.get('premium_since', None) else None
        self.deaf = raw_member.get('deaf', False)
        self.mute = raw_member.get('mute', False)
        self.pending = raw_member.get('pending', None)
