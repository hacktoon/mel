from .. import nodes
from .. import tokens

from .constants import (
    ROOT,
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


# BASE STRUCT ===============================================

class StructParser(BaseParser):
    def parse_expressions(self, node):
        while True:
            expression = self.read_rule(EXPRESSION)
            if not expression:
                break
            node.add(expression)


# KEY STRUCT =================================================

class KeyStructParser(StructParser):
    key_parsers = []

    @indexed
    def parse(self):
        if not self.stream.is_next(self.PrefixToken):
            return
        node = self.build_node()
        self.stream.read()
        self.parse_key(node)
        self.parse_expressions(node)
        self.stream.read(self.SuffixToken)
        return node

    def parse_key(self, node):
        key = self.read_any(*self.key_parsers)
        if not key:
            self.error(KeyNotFoundError)
        node.key = key


# ROOT STRUCT ================================================

@subparser
class RootParser(StructParser):
    id = ROOT
    Node = nodes.RootNode

    @indexed
    def parse(self):
        node = self.build_node()
        self.parse_expressions(node)
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
class ObjectParser(KeyStructParser):
    id = OBJECT
    Node = nodes.ObjectNode
    PrefixToken = tokens.StartObjectToken
    SuffixToken = tokens.EndObjectToken
    key_parsers = ANONYM_KEY, DEFAULT_DOC, DEFAULT_FORMAT, PATH


# QUERY ======================================================

@subparser
class QueryParser(KeyStructParser):
    id = QUERY
    Node = nodes.QueryNode
    PrefixToken = tokens.StartQueryToken
    SuffixToken = tokens.EndQueryToken
    key_parsers = ANONYM_KEY, PATH
