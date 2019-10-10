import re

from .nodes import Node
from .exceptions import ParsingError


_parsers = {}


# CLASSES =======================================

class Parser:
    def __init__(self, source, grammar):
        self.source = source
        self.grammar = grammar

    def parse(self):
        pass


class TokenStream:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.index_cache = 0

    def save(self):
        self.index_cache = self.index
        return self.index

    def restore(self, index):
        index = self.index_cache if index is None else index
        self.index = index

    def read(self, id):
        parser = _parsers[id]
        token = parser(self.text, self.index)
        self.index += len(token)
        return token


class Token:
    def __init__(self, id, text, index):
        self.id = id
        self.text = text
        self.index = index

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return "TOKEN({!r})".format(self.text)

    def __str__(self):
        start, end = self.index
        return self.text[start:end]


# PARSERS =======================================

def rule(id, parser):
    def _parser(stream):
        index = stream.save()
        try:
            return parser(stream)
        except ParsingError as error:
            stream.restore(index)
            raise error
    _parsers[id] = _parser
    return _parser


def token(id, string):
    pattern = re.compile(string)

    def parser(text, index=0):
        match = pattern.match(text, index)
        if match:
            return Token(id, match.group(0), match.span())
        raise ParsingError
    _parsers[id] = parser
    return parser


def zero_many(rule):
    def parser(stream):
        nodes = []
        while True:
            try:
                node = rule(stream)
                nodes.append(node)
            except ParsingError:
                break
        return nodes
    return parser


def one_of(*rules):
    def parser(stream):
        for rule in rules:
            try:
                node = r(rule)
                return node
            except ParsingError:
                pass
        raise ParsingError
    return parser


def seq(*rules):
    pass


def group(*rules):
    pass


def r(id):
    def parser(stream):
        return _parsers[id](stream)
    return parser


def t(id):
    def parser(stream):
        token = stream.read(id)
        return Node(token.text)
    return parser


# GRAMMAR TOKENS ===================================

token("space", r"(\s|;|,)*")
token("comment", r"--[^\n\r]*")
token("string", r"'[^']*'")
token("template-string", r'"[^"]*"')
token("float", r"-?\d*\.\d+([eE][-+]?\d+)?\b")
token("int", r"-?\d+\b")
token("name", r"[a-z]\w*")
token("concept", r"[A-Z]\w*")
token("equal", r"=")
token("different", r"!=")
token("log", r"!")
token("alias", r"@")
token("cache", r"\$")
token("tag", r"#")
token("default-format", r"%:")
token("format", r"%")
token("default-doc", r"\?:")
token("doc", r"\?")
token("sub-path", r"/")
token("meta-path", r"\.")
token("range", r"\.\.")
token("anonym", r":")
token("in", r"><")
token("gte", r">=")
token("gt", r">")
token("not-in", r"<>")
token("lte", r"<=")
token("lt", r"<")
token("wildcard", r"\*")
token("open_list", r"\[")
token("close_list", r"\]")
token("open_object", r"\(")
token("close_object", r"\)")
token("open_query", r"\{")
token("close_query", r"\}")


# GRAMMAR RULES ===================================

rule('root', zero_many(r('expression')))

rule('expression', one_of(r('tag'), r('relation'), r('value')))

rule('relation', seq(r('path'), r('sign'), r('value')))

rule('tag', seq(t('#'), t('name')))

rule('path', seq(r('keyword'), zero_many(seq(r('separator'), r('keyword')))))
rule('keyword', one_of(
    t('name'), t('concept'), r('log'), r('alias'),
    r('cache'), r('format'), r('meta'), r('doc')
))
rule('log', seq(t('!'), t('name')))
rule('alias', seq(t('@'), t('name')))
rule('cache', seq(t('$'), t('name')))
rule('format', seq(t('%'), t('name')))
rule('meta', seq(t('_'), t('name')))
rule('doc', seq(t('?'), t('name')))

rule('separator', one_of(t('sub-path'), t('meta-path')))

rule('sign', one_of(
    t('equal'), t('different'),
    t('lt'), t('lte'),
    t('gt'), t('gte'),
    t('in'), t('not-in')
))

rule('value', one_of(r('reference'), r('literal'), r('list'), r('object')))

rule('reference', seq(
    r('head-ref'),
    zero_many(seq(r('separator'), r('sub-ref')))
))
rule('head-ref', one_of(r('query'), r('keyword')))
rule('sub-ref', one_of(
    t('range'), t('int'), r('tag'), r('list'), r('object'),
    r('query'), r('keyword'), t('wildcard')
))

rule('literal', one_of(t('int'), t('float'), t('string'), t('boolean')))

rule('list', seq(t('['), zero_many(r('value')), t(']')))

rule('object', seq(
    t('('), r('object-key'), zero_many(r('expression')), t(')')
))
rule('object-key', one_of(
    t('anonym-path'), t('default-format'), t('default-doc'), r('path')
))

rule('query', seq(t('{'), r('query-key'), zero_many(r('expression')), t('}')))
rule('query-key', one_of(t('anonym-path'), r('path')))
