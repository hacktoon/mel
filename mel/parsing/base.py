import functools

from ..exceptions import ParsingError


_rules = {}


# decorator - add stream data to node instance via parser method
def indexed(parse_method):
    @functools.wraps(parse_method)
    def surrogate(self):
        first = self.stream.peek()
        node = parse_method(self)
        last = self.stream.peek(-1)
        node.index = first.index[0], last.index[1]
        node.text = self.stream.text
        return node
    return surrogate


# decorator - register parsing classes as subparsers in ParserMap
def subparser(cls):
    ParserMap.set(cls)
    return cls


# references parser classes by its id
class ParserMap:
    _map = {}

    @classmethod
    def set(cls, _parser):
        cls._map[_parser.id] = _parser

    @classmethod
    def get(cls, _id):
        return cls._map.get(_id)


# BASE PARSER =============================================

class BaseParser:
    def __init__(self, stream, subparsers=None):
        self.stream = stream
        # TODO: convert to parsing_context?
        self.subparsers = subparsers or {}

    def _get_parser(self, _id, stream):
        if _id not in self.subparsers:
            Parser = ParserMap.get(_id)
            self.subparsers[_id] = Parser(stream, subparsers=self.subparsers)
        return self.subparsers[_id]

    def build_node(self):
        return self.Node()

    def parse_rule(self, rule):
        parser = self._get_parser(rule, self.stream)
        index = self.stream.save()
        try:
            return parser.parse()
        except ParsingError as error:
            self.stream.restore(index)
            raise error

    def parse_alternative(self, *rules):
        for rule in rules:
            try:
                node = self.parse_rule(rule)
                if isinstance(node, list):
                    for n in node:
                        return n
                else:
                    return node
            except ParsingError:
                pass
        raise ParsingError

    # TODO: read_once_repeat

    def parse_zero_many(self, rule):
        nodes = []
        while True:
            try:
                node = self.parse_rule(rule)
                if isinstance(node, list):
                    for n in node:
                        nodes.append(n)
                else:
                    nodes.append(node)
            except ParsingError:
                break
        return nodes

    # TODO: remove later
    def parse_zero_many_alternative(self, *rules):
        nodes = []
        while True:
            try:
                node = self.parse_alternative(*rules)
                if isinstance(node, list):
                    for n in node:
                        nodes.append(n)
                else:
                    nodes.append(node)
            except ParsingError:
                break
        return nodes

    def parse_token(self, Token):
        token = self.stream.read(Token)
        if not token:
            raise ParsingError
        return token.value

    def parse_token_optional(self, Token):
        try:
            return self.parse_token(Token)
        except ParsingError:
            return

    def parse(self):
        raise NotImplementedError


class TokenParser(BaseParser):
    @indexed
    def parse(self):
        node = self.build_node()
        node.value = self.parse_token(self.Token)
        return node


def root(alternatives):
    _rules['root'] = alternatives


def rule(id, alternatives):
    _rules[id] = alternatives


def zero_many(rule):
    _rules[id] = rule


def option(rules):
    _rules[id] = rule


def sequence(rules):
    _rules[id] = rule


# PARSING GRAMMAR
# TODO: merge with token grammar

# root(zero_many('expression'))

# rule('expression', option('tag', 'relation', 'value'))

# rule('relation', sequence('path', 'sign', 'value'))

# rule('path', sequence('keyword',
#   zero_many(sequence('separator', 'keyword'))
# ))
# rule('keyword', option('NAME', 'CONCEPT', 'meta-keyword'))
# rule('meta-keyword', sequence(
#     option('LOG', 'ALIAS', 'CACHE', 'FORMAT', 'META', 'DOC'),
#     'NAME'
# ))

# rule('separator', option('SUB-PATH', 'META-PATH'))

# rule('sign', option('EQUAL', 'DIFFERENT', 'LT',
# 'LTE', 'GT', 'GTE', 'IN', 'NOT-IN'))

# rule('value', option('reference', 'literal', 'list', 'object'))

# rule('reference', sequence(
#     'head-ref',
#     zero_many(sequence('separator', 'sub-ref'))
# ))
# rule('head-ref', option('query', 'keyword'))
# rule('sub-ref',
#   option('RANGE', 'INT', 'tag', 'list',
#   'object', 'query', 'keyword', 'wildcard'))

# rule('literal', option('INT', 'FLOAT', 'STRING',
#   'TEMPLATE-STRING', 'BOOLEAN'))

# rule('list', sequence('[', zero_many('value'), ']'))

# rule('object', sequence('(', 'object-key', zero_many('expression'), ')'))
# rule('object-key',
#   option('ANONYM-PATH', 'DEFAULT-FORMAT', 'DEFAULT-DOC', 'path'))

# rule('query', sequence('{', 'query-key', zero_many('expression'), '}'))
# rule('query-key', option('ANONYM-PATH', 'path'))
