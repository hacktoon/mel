from dale.lexing import TokenStream
from dale.parsing import Parser

from dale.utils import Context
from dale.exceptions import DaleError, BaseError
from dale.exceptions.formatting import ErrorFormatter


def lex(text):
    try:
        return TokenStream(text)
    except BaseError as error:
        message = ErrorFormatter(error).format()
        raise DaleError(message)


def create_parser(text):
    stream = lex(text)
    return Parser(stream)


def parse(text):
    try:
        return create_parser(text).parse()
    except BaseError as error:
        message = ErrorFormatter(error).format()
        raise DaleError(message)


def eval(text, context=Context()):
    try:
        tree = parse(text)
        context.tree = tree
        context.text = text
        return tree.eval(context)
    except DaleError as error:
        raise error
