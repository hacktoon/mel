import re
from .types import tokens
from .types.errors import LexingError, ParsingError
from collections import namedtuple


TokenRule = namedtuple('TokenRule', 'id, regex, skip')
Token = namedtuple('Token', 'id, value, line, column, skip')


def build_token_rules(rules):
    _tokens = []
    priority_function = lambda rule: rule.get('priority', 0)
    prioritized_rules = sorted(rules, key=priority_function, reverse=True)
    for rule in prioritized_rules:
        regex = re.compile(rule['regex'])
        skip = rule.get('skip', False)
        token_rule = TokenRule(rule['id'], regex, skip)
        _tokens.append(token_rule)
    return _tokens


class Lexer:
    def __init__(self, text):
        self.token_rules = build_token_rules(tokens.rules)
        self.text = text
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        _tokens = []
        while self.index < len(self.text):
            token = self._emit_token()
            if not token.skip:
                _tokens.append(token)
        return _tokens

    def _emit_token(self):
        for rule in self.token_rules:
            match = rule.regex.match(self.text, self.index)
            if not match:
                continue
            id, value, skip = rule.id, match.group(0), rule.skip
            token = Token(id, value, self.line, self.column, skip)
            self._update_counters(value)
            return token
        else:
            raise LexingError('invalid syntax', self.index)

    def _update_counters(self, value):
        length = len(value)
        self.index += length
        newlines = re.findall(r'[\r\n]+', value)
        if newlines:
            self.line += len(newlines)
            self.column = 1
        else:
            self.column += length


class TokenStream:
    def __init__(self, text):
        self.tokens = Lexer(text).tokenize()
        self.index = 0

    def read(self, token_id, value=None):
        token = self.current()
        if self.is_current(token_id):
            if value:
                if value == token.value:
                    self.index += 1
                    return token
            else:
                self.index += 1
                return token

        template = 'expected a token of type {!r}, but found {!r}'
        message = template.format(token_id, token.id)
        raise ParsingError(message)

    def is_eof(self):
        return self.index >= len(self.tokens)

    def is_current(self, token_id):
        return self.current().id == token_id

    def is_next(self, token_id):
        return self.current(offset=1).id == token_id

    def current(self, offset=0):
        try:
            return self.tokens[self.index + offset]
        except IndexError:
            return Token('eof', '', -1, -1, True)
