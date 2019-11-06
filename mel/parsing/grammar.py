from ..nodes import (
    RuleNode,
    StringNode,
    PatternNode,
    EmptyNode
)
from ..exceptions import ParsingError


_ROOT_RULE_ID = '__ROOT_RULE_ID__'


class Grammar:
    def __init__(self, name=''):
        self.name = name
        self._rules = {}
        self._skip_rules = {}

    def parse(self, stream):
        return self._rules[_ROOT_RULE_ID](stream)

    def root(self, parser):
        return self.rule(_ROOT_RULE_ID, parser)

    def rule(self, id, parser):
        def rule_parser(stream):
            index = stream.save()
            try:
                return parser(stream)
            except ParsingError as error:
                stream.restore(index)
                raise error

        self._rules[id] = rule_parser
        return rule_parser

    def skip(self, id, pattern_string):
        def skip_rule_parser(stream):
            try:
                text, index = stream.read_pattern(pattern_string)
                return PatternNode(text, index)
            except ParsingError:
                return EmptyNode()

        self._skip_rules[id] = skip_rule_parser
        return skip_rule_parser

    def zero_many(self, parser):
        def zero_many_parser(stream):
            node = RuleNode()
            while True:
                try:
                    child = parser(stream)
                    node.add(child)
                except ParsingError:
                    break
            return node
        return zero_many_parser

    def one_of(self, *parsers):
        def one_of_parser(stream):
            for parser in parsers:
                try:
                    return parser(stream)
                except ParsingError:
                    pass
            raise ParsingError
        return one_of_parser

    def opt(self, parser):
        def opt_parser(stream):
            try:
                return parser(stream)
            except ParsingError:
                return EmptyNode()
        return opt_parser

    def seq(self, *parsers):
        def seq_parser(stream):
            node = RuleNode()
            for parser in parsers:
                child = parser(stream)
                node.add(child)
            return node
        return seq_parser

    def r(self, id):
        def rule_parser(stream):
            return self._rules[id](stream)
        return rule_parser

    def p(self, string):
        def pattern_parser(stream):
            self._parse_skip_rules(stream)
            text, index = stream.read_pattern(string)
            return PatternNode(text, index)
        return pattern_parser

    def s(self, string):
        def string_parser(stream):
            self._parse_skip_rules(stream)
            text, index = stream.read_string(string)
            return StringNode(text, index)
        return string_parser

    def _parse_skip_rules(self, stream):
        rules = self._skip_rules.values()
        while True:
            count = [True for parser in rules if parser(stream)]
            if len(count) == 0:
                break


# MEL GRAMMAR ===================================================
g = mel_grammar = Grammar('mel')

g.root(g.zero_many(g.r('expression')))

g.skip('space', r'[\s\n\r,]+')
g.skip('comment', r'--[^\n\r]*')

g.rule('expression', g.one_of(g.r('tag'), g.r('relation'), g.r('value')))
g.rule('tag', g.seq(g.s('#'), g.r('name')))
g.rule('relation', g.seq(g.r('path'), g.one_of(
    g.r('equal'), g.r('diff'), g.r('lte'), g.r('lt'),
    g.r('gte'), g.r('gt'), g.r('in'), g.r('out')
)))
g.rule('equal', g.seq(g.s('='), g.r('value')))
g.rule('diff', g.seq(g.s('!='), g.r('value')))
g.rule('lt', g.seq(g.s('<'), g.r('value')))
g.rule('lte', g.seq(g.s('<='), g.r('value')))
g.rule('gt', g.seq(g.s('>'), g.r('value')))
g.rule('gte', g.seq(g.s('>='), g.r('value')))
g.rule('in', g.seq(g.s('><'), g.r('value')))
g.rule('out', g.seq(g.s('<>'), g.r('value')))
g.rule('path', g.seq(
    g.r('keyword'), g.zero_many(g.one_of(g.r('sub-path'), g.r('meta-path')))
))
g.rule('sub-path', g.seq(g.s('/'), g.r('keyword')))
g.rule('meta-path', g.seq(g.s('.'), g.r('keyword')))
g.rule('keyword', g.one_of(
    g.r('name'), g.r('concept'), g.r('log'), g.r('alias'),
    g.r('cache'), g.r('format'), g.r('meta'), g.r('doc')
))
g.rule('log', g.seq(g.s('!'), g.r('name')))
g.rule('alias', g.seq(g.s('@'), g.r('name')))
g.rule('cache', g.seq(g.s('$'), g.r('name')))
g.rule('format', g.seq(g.s('%'), g.r('name')))
g.rule('meta', g.seq(g.s('_'), g.r('name')))
g.rule('doc', g.seq(g.s('?'), g.r('name')))
g.rule('value', g.one_of(
    g.r('reference'), g.r('literal'), g.r('list'), g.r('object'))
)
g.rule('reference', g.seq(
    g.one_of(g.r('query'), g.r('keyword')),
    g.zero_many(g.r('sub-reference'))
))
g.rule('sub-reference', g.seq(g.s('/'), g.one_of(
    g.r('range'), g.r('int'), g.r('tag'), g.r('list'), g.r('object'),
    g.r('query'), g.r('keyword'), g.r('wildcard')
)))
g.rule('literal', g.one_of(g.r('int'), g.r('float'), g.r('string')))
g.rule('list', g.seq(g.s('['), g.zero_many(g.r('value')), g.s(']')))
g.rule('range', g.one_of(
    g.seq(g.s('..'), g.r('int')),
    g.seq(g.r('int'), g.s('..'), g.opt(g.r('int')))
))
g.rule('object', g.seq(
    g.s('('), g.r('object-key'), g.zero_many(g.r('expression')), g.s(')')
))
g.rule('object-key', g.one_of(
    g.r('path'), g.r('default-path'), g.r('default-format'), g.r('default-doc')
))
g.rule('query', g.seq(
    g.s('{'), g.r('query-key'), g.zero_many(g.r('expression')), g.s('}'))
)
g.rule('query-key', g.one_of(g.r('path'), g.r('anonym-path')))
g.rule('default-format', g.s('%:'))
g.rule('default-doc', g.s('?:'))
g.rule('default-path', g.s(':'))
g.rule('wildcard', g.s('*'))
g.rule('string', g.p(r"'[^']*'|\"[^\"]*\""))
g.rule('float', g.p(r'-?\d*\.\d+([eE][-+]?\d+)?\b'))
g.rule('int', g.p(r'-?\d+\b'))
g.rule('name', g.p(r'[a-z]\w*'))
g.rule('concept', g.p(r'[A-Z]\w*'))
