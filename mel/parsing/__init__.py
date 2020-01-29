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
    def parse(self, _):
        raise NotImplementedError

    def skip_parse(self, context):
        symbols = context.skip_symbols.values()
        while True:
            skipped = [True for sym in symbols if sym.parse(context)]
            if len(skipped) == 0:
                break


# ZERO MANY SYMBOL ==========================================

class ZeroMany(Symbol):
    def __init__(self, symbol):
        self.symbol = symbol

    def parse(self, context):
        node = ZeroManyNode()
        while True:
            try:
                node.add(self.symbol.parse(context))
            except ParsingError:
                break
        return node


# SEQUENCE SYMBOL ==========================================

class Seq(Symbol):
    def __init__(self, *symbols):
        self.symbols = symbols

    def parse(self, context):
        node = SequenceNode()
        index = context.stream.save()
        try:
            for symbol in self.symbols:
                node.add(symbol.parse(context))
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return node


# ONE MANY SYMBOL ==========================================

class OneMany(Symbol):
    def __init__(self, symbol):
        self.symbol = symbol

    def parse(self, context):
        node = OneManyNode()
        node.add(self.symbol.parse(context))
        while True:
            try:
                node.add(self.symbol.parse(context))
            except ParsingError:
                break
        return node


# ONE OF SYMBOL ==========================================

class OneOf(Symbol):
    def __init__(self, *symbols):
        self.symbols = symbols

    def parse(self, context):
        node = OneOfNode()
        for symbol in self.symbols:
            try:
                node.add(symbol.parse(context))
                return node
            except ParsingError:
                pass
        raise ParsingError


# OPTIONAL SYMBOL ==========================================

class Opt(Symbol):
    def __init__(self, symbol):
        self.symbol = symbol

    def parse(self, context):
        node = OptionalNode()
        try:
            node.add(self.symbol.parse(context))
        except ParsingError:
            pass
        return node


# RULE SYMBOL ==========================================

class Rule(Symbol):
    def __init__(self, id):
        self.id = id

    def parse(self, context):
        symbol = context.symbols[self.id]
        node = RuleNode(self.id)
        index = context.stream.save()
        try:
            node.add(symbol.parse(context))
        except ParsingError as error:
            context.stream.restore(index)
            raise error
        return node


# STRING SYMBOL ==========================================

class Str(Symbol):
    def __init__(self, string):
        self.string = string

    def parse(self, context):
        self.skip_parse(context)
        text, index = context.stream.read_string(self.string)
        return StringNode(text, index)


# REGEX SYMBOL ==========================================

class Regex(Str):
    def parse(self, context):
        self.skip_parse(context)
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
# TODO: need build the entire grammar tree to "unparse" example from it

class Context:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class Grammar(Symbol):
    def __init__(self):
        self.symbols = {}
        self.skip_symbols = {}

    def rule(self, id, symbol):
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
        self.skip_parse(context)
        stream.read_eof()
        return tree
