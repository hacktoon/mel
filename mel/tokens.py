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

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        return "TOKEN({!r})".format(str(self))

    def __str__(self):
        start, end = self.index
        return self.text[start:end]


class NullToken(Token):
    id = "null"
    regex = re.compile(r"\0")

    def __init__(self, text="", index=None):
        super().__init__(text, index or (0, 0))


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
    regex = re.compile(r"'[^']*'")

    @property
    def value(self):
        return str(self)[1:-1]

    @property
    def newline(self):
        return re.search(NewlineToken.regex, self.value)


class TemplateStringToken(Token):
    id = "template-string"
    regex = re.compile(r'"[^"]*"')

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
    regex = re.compile(r"([tT]rue|[fF]alse)\b")
    priority = 1

    @property
    def value(self):
        _map = {"true": True, "false": False}
        return _map[str(self).lower()]


class NameToken(Token):
    id = "name"
    regex = re.compile(r"[a-z]\w*")


class ConceptToken(Token):
    id = "concept"
    regex = re.compile(r"[A-Z]\w*")


class LogPrefixToken(Token):
    id = "!"
    regex = re.compile(r"!")


class AliasPrefixToken(Token):
    id = "@"
    regex = re.compile(r"@")


class CachePrefixToken(Token):
    id = "$"
    regex = re.compile(r"\$")


class TagPrefixToken(Token):
    id = "#"
    regex = re.compile(r"#")


class FormatPrefixToken(Token):
    id = "%"
    regex = re.compile(r"%")


class DefaultFormatKeyToken(Token):
    id = "%:"
    regex = re.compile(r"%:")
    priority = 1


class DocPrefixToken(Token):
    id = "?"
    regex = re.compile(r"\?")


class DefaultDocKeyToken(Token):
    id = "?:"
    regex = re.compile(r"\?:")
    priority = 1


class ChildPathToken(Token):
    id = "/"
    regex = re.compile(r"/")


class MetaNodeToken(Token):
    id = "."
    regex = re.compile(r"\.")


class RangeToken(Token):
    id = ".."
    regex = re.compile(r"\.\.")
    priority = 1


class AnonymKeyToken(Token):
    id = ":"
    regex = re.compile(r":")


class EqualToken(Token):
    id = "="
    regex = re.compile(r"=")


class DifferentToken(Token):
    id = "!="
    regex = re.compile(r"!=")
    priority = 1


class GreaterThanToken(Token):
    id = ">"
    regex = re.compile(r">")


class GreaterThanEqualToken(Token):
    id = ">="
    regex = re.compile(r">=")
    priority = 1


class LessThanToken(Token):
    id = "<"
    regex = re.compile(r"<")


class LessThanEqualToken(Token):
    id = "<="
    regex = re.compile(r"<=")
    priority = 1


class InToken(Token):
    id = "><"
    regex = re.compile(r"><")
    priority = 1


class NotInToken(Token):
    id = "<>"
    regex = re.compile(r"<>")
    priority = 1


class WildcardToken(Token):
    id = "*"
    regex = re.compile(r"\*")


class StartObjectToken(Token):
    id = "("
    regex = re.compile(r"\(")


class EndObjectToken(Token):
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
