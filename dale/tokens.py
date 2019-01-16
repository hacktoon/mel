import re
import functools


@functools.lru_cache()
def classes():
    subclasses = Token.__subclasses__()
    return sorted(subclasses, key=lambda cls: cls.priority, reverse=True)


class Token:
    id = ""
    regex = None
    skip = False
    priority = 0

    def __init__(self, text="", index=None):
        self.text = text
        self.index = index or (0, 0)

    @property
    def value(self):
        return self.text

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return self.text


class StringToken(Token):
    id = "string"
    regex = re.compile("{}|{}".format(r"'[^']*'", r'"[^"]*"'))

    @property
    def value(self):
        return self.text[1:-1]


class FloatToken(Token):
    id = "float"
    regex = re.compile(r"-?\d*\.\d+([eE][-+]?\d+)?\b")
    priority = 2

    @property
    def value(self):
        return float(self.text)


class IntToken(Token):
    id = "int"
    regex = re.compile(r"-?\d+\b")
    priority = 1

    @property
    def value(self):
        return int(self.text)


class BooleanToken(Token):
    id = "boolean"
    regex = re.compile(r"(true|false)\b")
    priority = 2

    @property
    def value(self):
        return {"true": True, "false": False}[self.text]


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
    regex = re.compile(r"[_a-zA-Z]\w*")


class AttributePrefixToken(Token):
    id = "@"
    regex = re.compile("@")


class UidPrefixToken(Token):
    id = "#"
    regex = re.compile("#")


class FormatPrefixToken(Token):
    id = "%"
    regex = re.compile("%")


class VariablePrefixToken(Token):
    id = "$"
    regex = re.compile(r"\$")


class FlagPrefixToken(Token):
    id = "!"
    regex = re.compile("!")


class DocPrefixToken(Token):
    id = "?"
    regex = re.compile(r"\?")


class EqualsToken(Token):
    id = "="
    regex = re.compile("=")


class DifferentToken(Token):
    id = "!="
    regex = re.compile("!=")
    priority = 1


class GreaterThanToken(Token):
    id = ">"
    regex = re.compile(">")


class GreaterThanEqualToken(Token):
    id = ">="
    regex = re.compile(">=")
    priority = 1


class LessThanToken(Token):
    id = "<"
    regex = re.compile("<")


class LessThanEqualToken(Token):
    id = "<="
    regex = re.compile("<=")
    priority = 1


class NullKeyToken(Token):
    id = ":"
    regex = re.compile(":")


class WildcardToken(Token):
    id = "*"
    regex = re.compile(r"\*")


class RangeToken(Token):
    id = ".."
    regex = re.compile(r"\.\.")


class ChainToken(Token):
    id = "/"
    regex = re.compile("/")


class StartScopeToken(Token):
    id = "("
    regex = re.compile(r"\(")


class EndScopeToken(Token):
    id = ")"
    regex = re.compile(r"\)")


class StartQueryToken(Token):
    id = "{"
    regex = re.compile(r"\{")


class EndQueryToken(Token):
    id = "}"
    regex = re.compile(r"\}")


class StartListToken(Token):
    id = "["
    regex = re.compile(r"\[")


class EndListToken(Token):
    id = "]"
    regex = re.compile(r"\]")


class EOFToken(Token):
    id = "EOF"
    regex = re.compile(r"\0")
