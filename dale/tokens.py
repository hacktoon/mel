import re


def classes():
    token_types = []
    for cls in Token.__subclasses__():
        token_types.append(cls)
    return sorted(token_types, key=lambda cls: cls.priority, reverse=True)


class Token:
    id = ""
    regex = None
    skip = False
    priority = 0

    def __init__(self, match="", index=None):
        self.match = match
        self.index = index or (0, 0)

    @property
    def value(self):
        return self.match

    def __repr__(self):
        return self.match


class StringToken(Token):
    id = "string"
    regex = re.compile("{}|{}".format(r"'[^']*'", r'"[^"]*"'))

    @property
    def value(self):
        return self.match[1:-1]


class FloatToken(Token):
    id = "float"
    regex = re.compile(r"[-+]?\d*\.\d+([eE][-+]?\d+)?\b")
    priority = 2

    @property
    def value(self):
        return float(self.match)


class IntToken(Token):
    id = "int"
    regex = re.compile(r"[-+]?\d+\b")
    priority = 1

    @property
    def value(self):
        return int(self.match)


class BooleanToken(Token):
    id = "boolean"
    regex = re.compile(r"(true|false)\b")
    priority = 3

    @property
    def value(self):
        return {"true": True, "false": False}[self.match]


class WhitespaceToken(Token):
    id = "whitespace"
    regex = re.compile(r"[\s,\x0b\x0c]+")
    skip = True


class CommentToken(Token):
    id = "comment"
    regex = re.compile(r"--[^\n\r]*")
    skip = True


class NameToken(Token):
    id = "name"
    regex = re.compile(r"[_a-zA-Z]\w*(-\w+)*")


class HashToken(Token):
    id = "#"
    regex = re.compile("#")


class PercentToken(Token):
    id = "%"
    regex = re.compile("%")


class DollarToken(Token):
    id = "$"
    regex = re.compile(r"\$")


class ExclamationMarkToken(Token):
    id = "!"
    regex = re.compile("!")


class QuestionMarkToken(Token):
    id = "?"
    regex = re.compile(r"\?")


class ColonToken(Token):
    id = ":"
    regex = re.compile(":")


class AsteriskToken(Token):
    id = "*"
    regex = re.compile(r"\*")


class SlashToken(Token):
    id = "/"
    regex = re.compile("/")


class LeftParenthesisToken(Token):
    id = "("
    regex = re.compile(r"\(")


class RightParenthesisToken(Token):
    id = ")"
    regex = re.compile(r"\)")


class LeftBracesToken(Token):
    id = "{"
    regex = re.compile(r"\{")


class RightBracesToken(Token):
    id = "}"
    regex = re.compile(r"\}")


class LeftBracketToken(Token):
    id = "["
    regex = re.compile(r"\[")


class RightBracketToken(Token):
    id = "]"
    regex = re.compile(r"\]")


class EOFToken(Token):
    id = "EOF"
    regex = re.compile(r"\0")
