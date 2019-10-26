from mel.parsing import Stream, Parser

from mel.utils import Context
from mel.exceptions import MelError, ParsingError
from mel.exceptions.formatting import ErrorFormatter


def lex(text):
    try:
        return Stream(text)
    except ParsingError as error:
        message = ErrorFormatter(error).format()
        raise MelError(message)


def create_parser(text, Parser=Parser):
    stream = lex(text)
    return Parser(stream)


def parse(text, Parser=Parser):
    try:
        return create_parser(text, Parser).parse()
    except ParsingError as error:
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
