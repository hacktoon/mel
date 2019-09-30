from .. import nodes
from .. import tokens

from .constants import (
    KEYWORD,
    NAME,
    CONCEPT,
    LOG,
    ALIAS,
    CACHE,
    FORMAT,
    DOC,
    TAG
)
from .base import (
    BaseParser,
    TokenParser,
    indexed,
    subparser
)


@subparser
class NameParser(TokenParser):
    id = NAME
    Node = nodes.NameKeywordNode
    Token = tokens.NameToken


@subparser
class ConceptParser(TokenParser):
    id = CONCEPT
    Node = nodes.ConceptKeywordNode
    Token = tokens.ConceptToken


class PrefixedNameParser(BaseParser):
    @indexed
    def parse(self):
        self.parse_token(self.Token)
        node = self.build_node()
        node.value = self.parse_token(tokens.NameToken)
        return node


@subparser
class TagParser(PrefixedNameParser):
    id = TAG
    Node = nodes.TagKeywordNode
    Token = tokens.TagPrefixToken


@subparser
class LogParser(PrefixedNameParser):
    id = LOG
    Node = nodes.LogKeywordNode
    Token = tokens.LogPrefixToken


@subparser
class AliasParser(PrefixedNameParser):
    id = ALIAS
    Node = nodes.AliasKeywordNode
    Token = tokens.AliasPrefixToken


@subparser
class CacheParser(PrefixedNameParser):
    id = CACHE
    Node = nodes.CacheKeywordNode
    Token = tokens.CachePrefixToken


@subparser
class FormatParser(PrefixedNameParser):
    id = FORMAT
    Node = nodes.FormatKeywordNode
    Token = tokens.FormatPrefixToken


@subparser
class DocParser(PrefixedNameParser):
    id = DOC
    Node = nodes.DocKeywordNode
    Token = tokens.DocPrefixToken


@subparser
class KeywordParser(BaseParser):
    id = KEYWORD

    def parse(self):
        return self.parse_alternative(
            NAME,
            CONCEPT,
            LOG,
            ALIAS,
            CACHE,
            FORMAT,
            DOC,
        )
