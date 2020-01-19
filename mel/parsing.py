import re

from .exceptions import ParsingError


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, text):
        stream = Stream(text)
        return self.grammar.match(stream)


class Stream:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self._index_cache = 0

    def save(self):
        self._index_cache = self.index
        return self.index

    def restore(self, _index):
        self.index = self._index_cache if _index is None else _index

    def read_pattern(self, pattern_string):
        match = re.match(pattern_string, self.text[self.index:])
        if not match:
            raise ParsingError
        start, end = [offset + self.index for offset in match.span()]
        return self._read(match.group(0), (start, end))

    def read_string(self, string):
        text = self.text[self.index:]
        if not text.startswith(string):
            raise ParsingError
        index = self.index, self.index + len(string)
        return self._read(string, index)

    def _read(self, string, index):
        self.index += len(string)
        return string, index

    @property
    def eof(self):
        return self.index >= len(self.text)


class Rule:
    def __init__(self, id, parser):
        self.id = id
        self.parser = parser


class Grammar:
    def __init__(self):
        self._rules = {}
        self._skip_rules = {}

    def match(self, stream):
        rule_parsers = iter(self._rules.values())
        rule = next(rule_parsers)
        tree = rule.parser(stream)
        self._parse_skip_rules(stream)
        if not stream.eof:
            raise ParsingError
        return tree

    def rule(self, id, rule):
        def rule_parser(stream):
            index = stream.save()
            try:
                return rule.parser(stream)
            except ParsingError as error:
                stream.restore(index)
                raise error

        self._rules[id] = Rule(id, rule_parser)

    def skip(self, id, string):
        def skip_rule_parser(stream):
            try:
                stream.read_pattern(string)
            except ParsingError:
                return

        self._skip_rules[id] = Rule(id, skip_rule_parser)

    def zero_many(self, rule):
        def zero_many_parser(stream):
            nodes = []
            while True:
                try:
                    nodes.append(rule.parser(stream))
                except ParsingError:
                    break
            return nodes
        return Rule('id', zero_many_parser)

    def one_many(self, rule):
        def one_many_parser(stream):
            nodes = [rule.parser(stream)]
            while True:
                try:
                    nodes.append(rule.parser(stream))
                except ParsingError:
                    break
            return nodes
        return Rule('id', one_many_parser)

    def seq(self, *rules):
        def seq_parser(stream):
            nodes = []
            for rule in rules:
                nodes.append(rule.parser(stream))
            return nodes
        return Rule('Sequence', seq_parser)

    def one_of(self, *rules):
        def one_of_parser(stream):
            for rule in rules:
                try:
                    return rule.parser(stream)
                except ParsingError:
                    pass
            raise ParsingError
        return Rule('One of', one_of_parser)

    def opt(self, rule):
        def opt_parser(stream):
            try:
                return rule.parser(stream)
            except ParsingError:
                return []
        return Rule('Optional', opt_parser)

    def r(self, id):
        def rule_parser(stream):
            rule = self._rules[id]
            return rule.parser(stream)
        return Rule(id, rule_parser)

    def p(self, string):
        def pattern_parser(stream):
            self._parse_skip_rules(stream)
            text, _ = stream.read_pattern(string)
            return text
        return Rule(string, pattern_parser)

    def s(self, string):
        def string_parser(stream):
            self._parse_skip_rules(stream)
            text, _ = stream.read_string(string)
            return text
        return Rule(string, string_parser)

    def _parse_skip_rules(self, stream):
        rules = self._skip_rules.values()
        while True:
            skipped = [True for rule in rules if rule.parser(stream)]
            if len(skipped) == 0:
                break

    @property
    def NEWLINE(self):
        return self.p(r'[\r\n]+')

    @property
    def INT(self):
        return self.p(r'[0-9]+')

    @property
    def FLOAT(self):
        return self.p(r'-?\d*\.\d+([eE][-+]?\d+)?')

    @property
    def STRING(self):
        return self.p(r'"[^\"]*"|\'[^\']*\'')
