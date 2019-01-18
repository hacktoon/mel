import re
import functools


@functools.lru_cache()
def subclasses():
    subclasses = Token.__subclasses__()
    return sorted(subclasses, key=lambda cls: cls.priority, reverse=True)


class Token:
    id = ""
    regex = None
    skip = False
    priority = 0

    def __init__(self, text, index):
        self.text = text
        self.index = index

    @property
    def newline(self):
        return

    @property
    def value(self):
        return str(self)

    def __eq__(self, token):
        return self.id == token.id

    def __hash__(self):
        return super().__hash__()

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        return "TOKEN({!r})".format(str(self))

    def __str__(self):
        start, end = self.index
        return self.text[start:end]


class EOFToken(Token):
    id = "EOF"
    regex = re.compile(r"\0")

    def __init__(self):
        super().__init__("", (0, 0))


class WhitespaceToken(Token):
    id = "whitespace"
    regex = re.compile(r"([^\S\n\r]|;|,)+")
    skip = True


class NewlineToken(Token):
    id = "newline"
    regex = re.compile(r"\r|\r?\n")
    skip = True

    @property
    def newline(self):
        return True


class CommentToken(Token):
    id = "comment"
    regex = re.compile(r"--[^\n\r]*")
    priority = 2
    skip = True


class StringToken(Token):
    id = "string"
    regex = re.compile("{}|{}".format(r"'[^']*'", r'"[^"]*"'))

    @property
    def value(self):
        return str(self)[1:-1]

    @property
    def newline(self):
        return re.search(NewlineToken.regex, self.value)


class FloatToken(Token):
    id = "float"
    regex = re.compile(r"-?\d*\.\d+([eE][-+]?\d+)?\b")
    priority = 1

    @property
    def value(self):
        return float(str(self))


class IntToken(Token):
    id = "int"
    regex = re.compile(r"-?\d+\b")

    @property
    def value(self):
        return int(str(self))


class BooleanToken(Token):
    id = "boolean"
    regex = re.compile(r"(true|false)\b")
    priority = 1

    @property
    def value(self):
        return {"true": True, "false": False}[str(self)]


class NameToken(Token):
    id = "name"
    regex = re.compile(r"[_a-zA-Z]\w*")


class AttributePrefixToken(Token):
    id = "@"
    regex = re.compile("@")


class UIDPrefixToken(Token):
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


class SubOperatorToken(Token):
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
