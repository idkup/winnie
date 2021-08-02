from quoted import Quoted


class QuoteDB:
    def __init__(self):
        self.quoted = []
        self.taken_aliases = []

    def add_user(self, user):
        self.quoted.append(user)

    def add_taken_alias(self, alias):
        self.taken_aliases.append(alias)