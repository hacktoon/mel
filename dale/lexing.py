import re
from .types import tokens
from .types.errors import LexingError, UnexpectedValueError
from collections import namedtuple


TokenRule = namedtuple('TokenRule', 'id, regex, skip')
Token = namedtuple('Token', 'id, value, position, skip')
Position = namedtuple('Position', 'start, end, line, column')

NEWLINE_RE = r'[\r\n]+'


class Lexer:
    def __init__(self, text, rules):
        self.token_rules = self._build_rules(rules)
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

    def _build_rules(self, rules):
        _tokens = []
        priority_function = lambda rule: rule.get('priority', 0)
        prioritized_rules = sorted(rules, key=priority_function, reverse=True)
        for rule in prioritized_rules:
            regex = re.compile(rule['regex'])
            skip = rule.get('skip', False)
            token_rule = TokenRule(rule['id'], regex, skip)
            _tokens.append(token_rule)
        return _tokens

    def _build_token(self, rule, match):
        id, value, skip = rule.id, match.group(0), rule.skip
        position = Position(
            start  = match.start(),
            end    = match.end(),
            line   = self.line,
            column = self.column
        )
        self._update_counters(value)
        return Token(id, value, position, skip)

    def _emit_token(self):
        for rule in self.token_rules:
            match = rule.regex.match(self.text, self.index)
            if not match:
                continue
            return self._build_token(rule, match)
        else:
            raise LexingError('invalid syntax')

    def _update_counters(self, value):
        length = len(value)
        self.index += length
        newlines = re.findall(NEWLINE_RE, value)
        if newlines:
            self.line += len(newlines)
            self.column = 1
        else:
            self.column += length


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
