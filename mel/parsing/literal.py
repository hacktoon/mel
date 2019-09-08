from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    TokenParser
)


class IntParser(TokenParser):
    Node = nodes.IntNode
    Token = tokens.IntToken


class FloatParser(TokenParser):
    Node = nodes.FloatNode
    Token = tokens.FloatToken


class BooleanParser(TokenParser):
    Node = nodes.BooleanNode
    Token = tokens.BooleanToken


class StringParser(TokenParser):
    Node = nodes.StringNode
    Token = tokens.StringToken


class TemplateStringParser(TokenParser):
    Node = nodes.TemplateStringNode
    Token = tokens.TemplateStringToken


class LiteralParser(BaseParser):
    def parse(self):
        return self.read_any([
            IntParser,
            FloatParser,
            StringParser,
            TemplateStringParser,
            BooleanParser
        ])
