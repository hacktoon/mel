from dale.lexing import TokenStream
from dale.parsing import Parser

from dale.utils.context import Context
from dale.exceptions import DaleError
from dale.exceptions.formatting import ErrorFormatter


_evaluators = {}


def evaluator(name):
    def decorator(func):
        _evaluators[name] = func
    return decorator


def lex(text):
    try:
        return TokenStream(text)
    except DaleError as error:
        message = ErrorFormatter(text, error).format()
        raise DaleError(message)


def create_parser(text):
    stream = lex(text)
    return Parser(stream)


def parse(text):
    try:
        return create_parser(text).parse()
    except DaleError as error:
        message = ErrorFormatter(text, error).format()
        raise DaleError(message)


def eval(text, context=Context()):
    try:
        tree = parse(text)
        context.tree = tree
        context.text = text
        context.evaluators = _evaluators
        return tree.eval(context)
    except DaleError as error:
        raise error
