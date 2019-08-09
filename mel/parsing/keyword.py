from .. import nodes
from .. import tokens

from .base import (
    BaseParser,
    MultiParser,
    TokenParser,
    subparser,
    indexed
)

from ..exceptions import NameNotFoundError


@subparser
class NameParser(TokenParser):
    Node = nodes.NameKeywordNode
    Token = tokens.NameToken


@subparser
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


@subparser
class TagParser(PrefixedNameParser):
    Node = nodes.TagKeywordNode
    Token = tokens.TagPrefixToken


@subparser
class LogParser(PrefixedNameParser):
    Node = nodes.LogKeywordNode
    Token = tokens.LogPrefixToken


@subparser
class AliasParser(PrefixedNameParser):
    Node = nodes.AliasKeywordNode
    Token = tokens.AliasPrefixToken


@subparser
class CacheParser(PrefixedNameParser):
    Node = nodes.CacheKeywordNode
    Token = tokens.CachePrefixToken


@subparser
class FormatParser(PrefixedNameParser):
    Node = nodes.FormatKeywordNode
    Token = tokens.FormatPrefixToken


@subparser
class DocParser(PrefixedNameParser):
    Node = nodes.DocKeywordNode
    Token = tokens.DocPrefixToken


@subparser
class MetaParser(PrefixedNameParser):
    Node = nodes.MetaKeywordNode
    Token = tokens.MetaPrefixToken


@subparser
class KeywordParser(MultiParser):
    options = (
        NameParser,
        ConceptParser,
        LogParser,
        AliasParser,
        CacheParser,
        FormatParser,
        MetaParser,
        DocParser
    )
