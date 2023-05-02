import re


class Message:
    def __init__(self, data, chat_type, friend, group, user, msg, wx=None):
        self.data = data
        self.chat_type = chat_type
        self.friend = friend
        self.group = group
        self.user = user
        self.msg = msg
        self.wx = wx

    def get_message(self):
        return self.msg

    def get_arg_message(self):
        if isinstance(self.msg, str):
            return self.msg.split(' ')
        return list()

    def strip(self, state):
        args = str(self.msg).lstrip(state['_prefix']['raw_command']).strip()
        if args:
            return re.split(r'[\s]+', args)
        return []
