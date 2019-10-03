import re

from .exceptions import ParsingError

parsers = {}


class Token:
    def __init__(self, id, text, index):
        self.id = id
        self.text = text
        self.index = index

    def __eq__(self, token):
        return self.id == token.id

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return "TOKEN({!r})".format(self.text)

    def __str__(self):
        start, end = self.index
        return self.text[start:end]


def token(id, regex=None, skip=False):
    regex = re.compile(regex or re.escape(id))

    def parser(text, index=0):
        match = regex.match(text, index)
        if match:
            return Token(id, match.string, match.span())
        raise ParsingError
    parsers[id] = parser
    return parser


token("whitespace", r"([^\S\n\r]|;|,)+", skip=True)
token("newline", r"\r?\n|\r", skip=True)
token("comment", r"--[^\n\r]*", skip=True)

token("string", r"'[^']*'")
token("template-string", r'"[^"]*"')
token("float", r"-?\d*\.\d+([eE][-+]?\d+)?\b")
token("int", r"-?\d+\b")
token("boolean", r"([tT]rue|[fF]alse)\b")
token("name", r"[a-z]\w*")
token("concept", r"[A-Z]\w*")
token("!=")
token("!")
token("@")
token("$")
token("#")
token("%:")
token("%")
token("?:")
token("?")
token("/")
token(".")
token("..")
token(":")
token("=")
token("><")
token(">=")
token(">")
token("<>")
token("<=")
token("<")
token("*")
token("(")
token(")")
token("{")
token("}")
token("[")
token("]")
