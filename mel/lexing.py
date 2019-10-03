from . import tokens


class TokenStream:
    def __init__(self, text):
        self.text = text
        self.index = 0

    def save(self):
        return self.index

    def restore(self, index):
        self.index = index

    def parse(self, token_id):
        parser = tokens.parsers[token_id]
        token = parser(self.text, self.index)
        self.index += len(token.text)
        return token

    def is_eof(self):
        return self.index >= len(self.tokens)
