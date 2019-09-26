from mel.lexing import TokenStream
from mel.parsing import Parser

from mel.utils import Context
from mel.exceptions import MelError, LexingError
from mel.exceptions.formatting import ErrorFormatter


def lex(text):
    try:
        return TokenStream(text)
    except LexingError as error:
        message = ErrorFormatter(error).format()
        raise MelError(message)


def create_parser(text, Parser=Parser):
    stream = lex(text)
    return Parser(stream)


def parse(text, Parser=Parser):
    try:
        return create_parser(text, Parser).parse()
    except LexingError as error:
        message = ErrorFormatter(error).format()
        raise MelError(message)


def eval(text, context=Context()):
    try:
        tree = parse(text)
        context.tree = tree
        context.text = text
        return tree
    except MelError as error:
        raise error
