import random


class Quoted:
    def __init__(self, uid):
        self.uid = uid
        self.aliases = []
        self.quotes = []

    def add_alias(self, alias):
        self.aliases.append(alias)

    def add_quote(self, quote):
        self.quotes.append(quote)

    def remove_alias(self, alias):
        self.aliases.remove(alias)

    def remove_quote(self, quote):
        self.quotes.remove(quote)

    def get_random_quote(self):
        return random.choice(self.quotes)