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
_ = mel_grammar = Grammar('mel')

_.root(_.zero_many(_.r('expression')))

_.skip('space', r'[\s\n\r,]+')
_.skip('comment', r'--[^\n\r]*')

_.rule('expression', _.one_of(_.r('tag'), _.r('relation'), _.r('value')))
_.rule('tag', _.seq(_.s('#'), _.r('name')))
_.rule('relation', _.seq(_.r('path'), _.one_of(
    _.r('equal'), _.r('diff'), _.r('lte'), _.r('lt'),
    _.r('gte'), _.r('gt'), _.r('in'), _.r('out')
)))
_.rule('equal', _.seq(_.s('='), _.r('value')))
_.rule('diff', _.seq(_.s('!='), _.r('value')))
_.rule('lt', _.seq(_.s('<'), _.r('value')))
_.rule('lte', _.seq(_.s('<='), _.r('value')))
_.rule('gt', _.seq(_.s('>'), _.r('value')))
_.rule('gte', _.seq(_.s('>='), _.r('value')))
_.rule('in', _.seq(_.s('><'), _.r('value')))
_.rule('out', _.seq(_.s('<>'), _.r('value')))
_.rule('path', _.seq(
    _.r('keyword'), _.zero_many(_.one_of(_.r('sub-path'), _.r('meta-path')))
))
_.rule('sub-path', _.seq(_.s('/'), _.r('keyword')))
_.rule('meta-path', _.seq(_.s('.'), _.r('keyword')))
_.rule('keyword', _.one_of(
    _.r('name'), _.r('concept'), _.r('log'), _.r('alias'),
    _.r('cache'), _.r('format'), _.r('meta'), _.r('doc')
))
_.rule('log', _.seq(_.s('!'), _.r('name')))
_.rule('alias', _.seq(_.s('@'), _.r('name')))
_.rule('cache', _.seq(_.s('$'), _.r('name')))
_.rule('format', _.seq(_.s('%'), _.r('name')))
_.rule('meta', _.seq(_.s('_'), _.r('name')))
_.rule('doc', _.seq(_.s('?'), _.r('name')))
_.rule('value', _.one_of(
    _.r('reference'), _.r('literal'), _.r('list'), _.r('object'))
)
_.rule('reference', _.seq(
    _.one_of(_.r('query'), _.r('keyword')),
    _.zero_many(_.r('sub-reference'))
))
_.rule('sub-reference', _.seq(_.s('/'), _.one_of(
    _.r('range'), _.r('int'), _.r('tag'), _.r('list'), _.r('object'),
    _.r('query'), _.r('keyword'), _.r('wildcard')
)))
_.rule('literal', _.one_of(_.r('int'), _.r('float'), _.r('string')))
_.rule('list', _.seq(_.s('['), _.zero_many(_.r('value')), _.s(']')))
_.rule('range', _.one_of(
    _.seq(_.s('..'), _.r('int')),
    _.seq(_.r('int'), _.s('..'), _.opt(_.r('int')))
))
_.rule('object', _.seq(
    _.s('('), _.r('object-key'), _.zero_many(_.r('expression')), _.s(')')
))
_.rule('object-key', _.one_of(
    _.r('path'), _.r('default-path'), _.r('default-format'), _.r('default-doc')
))
_.rule('query', _.seq(
    _.s('{'), _.r('query-key'), _.zero_many(_.r('expression')), _.s('}'))
)
_.rule('query-key', _.one_of(_.r('path'), _.r('anonym-path')))
_.rule('default-format', _.s('%:'))
_.rule('default-doc', _.s('?:'))
_.rule('default-path', _.s(':'))
_.rule('wildcard', _.s('*'))
_.rule('string', _.p(r"'[^']*'|\"[^\"]*\""))
_.rule('float', _.p(r'-?\d*\.\d+([eE][-+]?\d+)?\b'))
_.rule('int', _.p(r'-?\d+\b'))
_.rule('name', _.p(r'[a-z]\w*'))
_.rule('concept', _.p(r'[A-Z]\w*'))
