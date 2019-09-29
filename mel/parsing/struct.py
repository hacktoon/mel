from .. import nodes
from .. import tokens

from .constants import (
    ANONYM_KEY,
    DEFAULT_DOC,
    DEFAULT_FORMAT,
    OBJECT,
    QUERY,
    PATH,
    TAG,
    RELATION,
    VALUE
)
from .base import (
    BaseParser,
    TokenParser,
    indexed,
    subparser
)


# KEY STRUCT =================================================

class StructParser(BaseParser):
    key_parsers = []

    @indexed
    def parse(self):
        self.parse_token(self.PrefixToken)
        node = self.build_node()
        node.key = self.parse_alternative(*self.key_parsers)
        node.add(*self.parse_zero_many_alternative(TAG, RELATION, VALUE))
        self.parse_token(self.SuffixToken)
        return node


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
