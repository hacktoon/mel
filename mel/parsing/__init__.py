from ..exceptions import ParsingError
from .stream import Stream
from .nodes import (
    RootNode,
    RuleNode,
    StringNode,
    PatternNode,
    ZeroManyNode,
    OneManyNode,
    OneOfNode,
    SequenceNode,
    OptionalNode,
)


class Symbol:
    def __init__(self, id, parser):
        self.id = id
        self.parser = parser

    def _skip_symbols(self, context):
        rules = context.skip_symbols.values()
        while True:
            skipped = [True for rule in rules if rule.parse(context)]
            if len(skipped) == 0:
                break


# ZERO MANY SYMBOL ==========================================

class ZeroMany(Symbol):
    def __init__(self, *rules):
        self.rules = rules

    # HELPER FUNCTION
    def _parse_rules(self, context, node):
        index = context.stream.save()
        try:
            for rule in self.rules:
                node.add(rule.parse(context))
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return node

    def parse(self, context):
        node = ZeroManyNode()
        while True:
            try:
                node = self._parse_rules(context, node)
            except ParsingError:
                break
        return node


# SEQUENCE SYMBOL ==========================================

class Seq(Symbol):
    def __init__(self, *rules):
        self.rules = rules

    def parse(self, context):
        node = SequenceNode()
        index = context.stream.save()
        try:
            for rule in self.rules:
                node.add(rule.parse(context))
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return node


# ONE MANY SYMBOL ==========================================

class OneMany(Symbol):
    def __init__(self, *rules):
        self.rules = rules

    def parse(self, context):
        node = OneManyNode()
        while True:
            try:
                for rule in self.rules:
                    node.add(rule.parse(context))
            except ParsingError:
                break
        if len(node):  # TODO: remove this check
            return node
        raise ParsingError


# ONE OF SYMBOL ==========================================

class OneOf(Symbol):
    def __init__(self, *rules):
        self.rules = rules
        # TODO: use `rules` to build error messages

    def parse(self, context):
        node = OneOfNode()
        for rule in self.rules:
            try:
                node.add(rule.parse(context))
                return node
            except ParsingError:
                pass
        raise ParsingError


# OPTIONAL SYMBOL ==========================================

class Opt(Symbol):
    def __init__(self, rule):
        self.rule = rule

    def parse(self, context):
        node = OptionalNode()
        try:
            node.add(self.rule.parse(context))
        except ParsingError:
            pass
        return node


# RULE SYMBOL ==========================================

class Rule(Symbol):
    def __init__(self, id):
        self.id = id

    def parse(self, context):
        rule = context.symbols[self.id]
        node = RuleNode(self.id)
        index = context.stream.save()
        try:
            node.add(rule.parse(context))
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return node


# STRING SYMBOL ==========================================

class Str(Symbol):
    def __init__(self, string):
        self.string = string

    def parse(self, context):
        self._skip_symbols(context)
        text, index = context.stream.read_string(self.string)
        return StringNode(text, index)


# REGEX SYMBOL ==========================================

class Regex(Str):
    def parse(self, context):
        self._skip_symbols(context)
        text, index = context.stream.read_pattern(self.string)
        return PatternNode(text, index)


# SKIP SYMBOL ==========================================

class Skip(Str):
    def parse(self, context):
        try:
            context.stream.read_pattern(self.string)
        except ParsingError:
            return


# GRAMMAR ==========================================

class Context:
    def __init__(self, **kw):
        self.symbols = kw.get('symbols', {})
        self.skip_symbols = kw.get('skip_symbols', {})
        self.stream = kw.get('stream', Stream())


class Grammar(Symbol):
    def __init__(self):
        self.symbols = {}
        self.skip_symbols = {}

    def set(self, id, symbol):
        self.symbols[id] = symbol

    def skip(self, id, string):
        self.skip_symbols[id] = Skip(string)

    def parse(self, text):
        stream = Stream(text)
        symbol = next(iter(self.symbols.values()))
        context = Context(
            skip_symbols=self.skip_symbols,
            symbols=self.symbols,
            stream=stream
        )
        tree = RootNode()
        tree.add(symbol.parse(context))
        self._skip_symbols(context)
        if not stream.eof:
            raise ParsingError
        return tree
