import functools
from .stream import (
    DIGIT
)


class Match:
    def __init__(self, id, chars):
        self.id = id
        self.error = len(chars) == 0
        self.chars = chars

    def __repr__(self):
        return ''.join(char.value for char in self.chars)


def parser(name):
    def decorator(parser):
        @functools.wraps(parser)
        def real_parser(stream):
            return Match(name, parser(stream))
        return real_parser
    return decorator


# ======================================
def digit():
    @parser('one digit')
    def digit_parser(stream):
        return stream.read_one(DIGIT)
    return digit_parser


# ======================================
def digits():
    @parser('one or more digits')
    def digit_parser(stream):
        return stream.read_one(DIGIT)
    return digit_parser


# ======================================
def quoted(text):
    @parser('a quoted literal')
    def string_parser(stream):
        return stream.read(text)
    return string_parser


# ======================================
def seq(text):
    @parser('a sequence')
    def string_parser(stream):
        return stream.read(text)
    return string_parser


# ======================================
def lit(text):
    @parser('a literal sequence')
    def string_parser(stream):
        return stream.read(text)
    return string_parser


# ======================================
def zeromany(parser):
    @parser('zero or many')
    def parse(self, context):
        nodes = []
        # while True:
        #     nodes.append(parser)
        return nodes


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
