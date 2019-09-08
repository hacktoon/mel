from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    TokenParser,
    indexed
)

from ..exceptions import NameNotFoundError


class NameParser(TokenParser):
    Node = nodes.NameKeywordNode
    Token = tokens.NameToken


class ConceptParser(TokenParser):
    Node = nodes.ConceptKeywordNode
    Token = tokens.ConceptToken


class PrefixedNameParser(BaseParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        prefix = self.stream.read()
        node = self.build_node()
        if self.stream.is_next(tokens.NameToken):
            node.value = self.stream.read().value
            return node
        self.error(NameNotFoundError, prefix)


class TagParser(PrefixedNameParser):
    Node = nodes.TagKeywordNode
    Token = tokens.TagPrefixToken


class LogParser(PrefixedNameParser):
    Node = nodes.LogKeywordNode
    Token = tokens.LogPrefixToken


class AliasParser(PrefixedNameParser):
    Node = nodes.AliasKeywordNode
    Token = tokens.AliasPrefixToken


class CacheParser(PrefixedNameParser):
    Node = nodes.CacheKeywordNode
    Token = tokens.CachePrefixToken


class FormatParser(PrefixedNameParser):
    Node = nodes.FormatKeywordNode
    Token = tokens.FormatPrefixToken


class DocParser(PrefixedNameParser):
    Node = nodes.DocKeywordNode
    Token = tokens.DocPrefixToken


class KeywordParser(BaseParser):
    def parse(self):
        return self.read_any([
            NameParser,
            ConceptParser,
            LogParser,
            AliasParser,
            CacheParser,
            FormatParser,
            DocParser
        ])
