import random


class Quoted:
    def __init__(self, uid):
        self.uid = uid
        self.aliases = []
        self.quotes = []

    def add_alias(self, alias):
        self.aliases += alias

    def add_quote(self, quote):
        self.quotes += quote

    def remove_alias(self, alias):
        self.aliases.remove(alias)

    def get_random_quote(self):
        return random.choice(self.quotes)