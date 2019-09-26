from .. import nodes
from .. import tokens

from .constants import (
    EXPRESSION,
    ANONYM_KEY,
    DEFAULT_DOC,
    DEFAULT_FORMAT,
    OBJECT,
    QUERY,
    PATH
)
from .base import (
    BaseParser,
    TokenParser,
    indexed,
    subparser
)

from ..exceptions import KeyNotFoundError


# KEY STRUCT =================================================

class StructParser(BaseParser):
    key_parsers = []

    @indexed
    def parse(self):
        token = self.read_token(self.PrefixToken)
        if not token:
            return
        node = self.build_node()
        self.parse_key(node)
        expressions = self.read_zero_many(EXPRESSION)
        node.add(*expressions)
        self.stream.read(self.SuffixToken)
        return node

    def parse_key(self, node):
        key = self.read_any(*self.key_parsers)
        if not key:
            self.error(KeyNotFoundError)
        node.key = key


# STRUCT KEY ====================================================

@subparser
class AnonymKeyParser(TokenParser):
    id = ANONYM_KEY
    Node = nodes.AnonymKeyNode
    Token = tokens.AnonymKeyToken


@subparser
class DefaultDocKeyParser(TokenParser):
    id = DEFAULT_DOC
    Node = nodes.DefaultDocKeyNode
    Token = tokens.DefaultDocKeyToken


@subparser
class DefaultFormatKeyParser(TokenParser):
    id = DEFAULT_FORMAT
    Node = nodes.DefaultFormatKeyNode
    Token = tokens.DefaultFormatKeyToken


# OBJECT ======================================================

@subparser
class ObjectParser(StructParser):
    id = OBJECT
    Node = nodes.ObjectNode
    PrefixToken = tokens.StartObjectToken
    SuffixToken = tokens.EndObjectToken
    key_parsers = ANONYM_KEY, DEFAULT_DOC, DEFAULT_FORMAT, PATH


# QUERY ======================================================

@subparser
class QueryParser(StructParser):
    id = QUERY
    Node = nodes.QueryNode
    PrefixToken = tokens.StartQueryToken
    SuffixToken = tokens.EndQueryToken
    key_parsers = ANONYM_KEY, PATH
