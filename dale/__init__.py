from dale.lexing import TokenStream
from dale.parsing import Parser

from dale.utils.context import Context
from dale.exceptions import Error
from dale.exceptions.formatting import ErrorFormatter


_evaluators = {}


def evaluator(name):
    def decorator(func):
        _evaluators[name] = func
    return decorator


def parse(text):
    try:
        stream = TokenStream(text)
        return Parser(stream).parse()
    except Error as error:
        message = ErrorFormatter(text, error).format(lines_offset=4)
        raise Error(message)


def eval(text, context=Context()):
    try:
        stream = TokenStream(text)
        tree = Parser(stream).parse()
        context.tree = tree
        context.text = text
        context.evaluators = _evaluators

        return tree.eval(context)
    except Error as error:
        message = ErrorFormatter(text, error).format(lines_offset=4)
        raise Error(message)
