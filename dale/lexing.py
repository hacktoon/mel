import re
from .types import tokens
from .types.errors import LexingError, UnexpectedValueError
from collections import namedtuple


TokenRule = namedtuple('TokenRule', 'id, regex, skip')


class Token:
    def __init__(self, id, value, index, skip=False):
        self.id = id
        self.index = index
        self.value = value
        self.skip = skip


class TokenRules:
    def __init__(self, rules):
        self.rules = self._build(rules)

    def __iter__(self):
        for rule in self.rules:
            yield rule

    def _build(self, rules):
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
    def __init__(self, text, rules):
        self.token_rules = TokenRules(rules)
        self.text = text
        self.index = 0

    def tokenize(self):
        _tokens = []
        while self.index < len(self.text):
            token = self._emit_token()
            if not token.skip:
                _tokens.append(token)
        return _tokens

    def _build_token(self, rule, match):
        id, value, skip = rule.id, match.group(0), rule.skip
        token = Token(id, value, self.index, skip)
        self.index += len(value)
        return token

    def _emit_token(self):
        for rule in self.token_rules:
            match = rule.regex.match(self.text, self.index)
            if not match:
                continue
            return self._build_token(rule, match)
        else:
            raise LexingError('invalid syntax')


class TokenStream:
    def __init__(self, text, rules):
        self.tokens = Lexer(text, rules).tokenize()
        self.text = text
        self.index = 0

    def read(self, expected_token_id, value=None):
        token = self.current()
        if self.is_current(expected_token_id):
            if value:
                if value == token.value:
                    self.index += 1
                    return token
            else:
                self.index += 1
                return token
        raise UnexpectedValueError(expected_token_id, token.id)

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
            return Token('eof', '', None, True)
