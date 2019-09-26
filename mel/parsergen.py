import re


EQUALS = r'='
RULE = r'[a-z_-]+[*?+]?'
REGEX = r'[A-Z_-]+[*?+]?'
OR = r'\|'
OPEN_GROUP = r'\('
CLOSE_GROUP = r'\)'
STRING = r"'[^']+'"
ZERO_MANY = r'\*'
ONE_MANY = r'\+'
OPTIONAL = r'\?'
SPACE = r'[ \t]*'
NEWLINE = r'\s+'


class Parser:
    def __init__(self, text):
        self.text = text
        self.index = 0

    def read(self, pattern):
        match = self._read_lexeme(pattern)
        if not match:
            self.error('Error reading token')
        self.index += len(match.string)
        return match.string

    def read_optional(self, pattern):
        match = self._read_lexeme(pattern)
        if match:
            self.index += len(match.string)
            return match.string

    def read_space(self):
        self.read_optional(SPACE)

    def read_newline(self):
        self.read_rule(NEWLINE)

    def _read_lexeme(self, pattern):
        return re.match(pattern, self.text[self.index:])

    def parse_rule(self, text):
        self.read_space()
        self.read_rule(RULE)
        self.read_space()
        self.read_rule(EQUALS)
        self.read_space()
        self.parse_rule_body()
        self.read_newline()

    def parse_rule_body(self):
        self.read_any(RULE, REGEX, STRING)

    def error(self, msg):
        raise Exception(msg)

    def parse(self):
        pass


class AnyParser:
    pass
