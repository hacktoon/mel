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

from ..exceptions import NameNotFoundError


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
        prefix = self.read_token(self.Token)
        if not prefix:
            return
        node = self.build_node()
        token = self.read_token(tokens.NameToken)
        if token:
            node.value = token.value
            return node
        self.error(NameNotFoundError, prefix)


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
        return self.read_one(
            NAME,
            CONCEPT,
            LOG,
            ALIAS,
            CACHE,
            FORMAT,
            DOC,
        )
