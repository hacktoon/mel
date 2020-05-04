import functools
from .stream import (
    DIGIT
)


class ParseResult:
    def __init__(self, chars):
        self.error = len(chars) == 0
        self.chars


def parser(name):
    def decorator(generator):
        @functools.wraps(generator)
        def real_generator():
            return generator()
        return real_generator
    return decorator


@parser('Digit')
def digit():
    def digit_parser(stream):
        return stream.read_many(DIGIT)
    return digit_parser


def char(id):
    def char_parser(stream):
        return stream.read(id)
    return char_parser


# class Symbol:
#     def __init__(self, *symbols):
#         self.symbols = symbols

#     def parse(self, _):
#         raise NotImplementedError

#     def list_parse(self, symbols, context):
#         nodes = []
#         index = context.stream.save()
#         try:
#             for symbol in symbols:
#                 nodes.append(symbol.parse(context))
#         except ParsingError as error:
#             context.stream.restore(index)
#             raise error
#         return nodes

#     def skip_parse(self, context):
#         skip_rules = context.skip_rules.values()

#         def skipped():
#             return len([r for r in skip_rules if skip(context, r)])

#         def skip(context, rule):
#             try:
#                 for symbol in rule.symbols:
#                     symbol.parse(context, skip=False)  # TODO: remove skip
#             except ParsingError:
#                 return False
#             return True

#         while skipped():
#             pass

#     def __repr__(self):
#         children = ', '.join([repr(s) for s in self.symbols])
#         return f"{self.__class__.__name__}({children})"


# class Start(Symbol):
#     def parse(self, context):
#         node = RootNode()
#         symbols = context.start_rule.symbols
#         children = self.list_parse(symbols, context)
#         node.add(*children)
#         self.skip_parse(context)
#         context.stream.close()
#         return node


# class Sym(Symbol):
#     def __init__(self, id):
#         self.id = id

#     def parse(self, context):
#         symbols = context.rules[self.id].symbols
#         node = RuleNode(self.id)
#         index = context.stream.save()
#         try:
#             children = self.list_parse(symbols, context)
#             node.add(*children)
#         except ParsingError as error:
#             context.stream.restore(index)
#             raise error
#         return node

#     def __repr__(self):
#         classname = self.__class__.__name__
#         return f'{classname}("{self.id}")'


# class ZeroMany(Symbol):
#     def parse(self, context):
#         node = ZeroManyNode()
#         while True:
#             try:
#                 children = self.list_parse(self.symbols, context)
#                 node.add(*children)
#             except ParsingError:
#                 break
#         return node


# class OneMany(Symbol):
#     def parse(self, context):
#         node = OneManyNode()
#         node.add(*self.list_parse(self.symbols, context))
#         while True:
#             try:
#                 children = self.list_parse(self.symbols, context)
#                 node.add(*children)
#             except ParsingError:
#                 break
#         return node


# class Opt(Symbol):
#     def parse(self, context):
#         node = OptionalNode()
#         try:
#             children = self.list_parse(self.symbols, context)
#             node.add(*children)
#         except ParsingError:
#             pass
#         return node


# class OneOf(Symbol):
#     def parse(self, context):
#         node = OneOfNode()
#         for symbol in self.symbols:
#             try:
#                 node.add(*symbol.parse(context))
#                 return node
#             except ParsingError:
#                 pass
#         raise ParsingError


# class Str(Symbol):
#     def __init__(self, string):
#         self.string = string

#     def parse(self, context, skip=True):
#         if skip:
#             self.skip_parse(context)
#         text, index = context.stream.read_string(self.string)
#         return StringNode(text, index)

#     def __repr__(self):
#         classname = self.__class__.__name__
#         return f'{classname}("{self.string}")'


# class Regex(Str):
#     def parse(self, context, skip=True):
#         if skip:
#             self.skip_parse(context)
#         text, index = context.stream.read_pattern(self.string)
#         return PatternNode(text, index)
