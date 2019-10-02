import re

from .exceptions import ParsingError

_parsers = {}


def token(id, regex=None):
    regex = re.compile(regex or re.escape(id))

    def parser(text, index):
        match = regex.match(text, index)
        if match:
            return match.string
        raise ParsingError
    _parsers[id] = parser


# special tokens
token("whitespace", r"([^\S\n\r]|;|,)+")
token("newline", r"\r?\n|\r")
token("comment", r"--[^\n\r]*")

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
