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


def eval(text, context=Context()):
    try:
        tree = Parser().parse(text)
        context.tree = tree
        context.text = text
        context.evaluators = _evaluators

        return tree.eval(context)
    except DaleError as error:
        message = ErrorFormatter(text, error).format(lines_offset=4)
        raise DaleError(message)
