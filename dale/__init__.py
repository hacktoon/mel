from dale.lexing import Lexer, TokenStream
from dale.parsing import Parser

from dale.types import errors
from dale.types.errors import DaleError


def eval(text, context=None):
    try:
        tokens = Lexer(text).tokenize()
        stream = TokenStream(tokens)
        return Parser(stream).parse(context)
    except DaleError as error:
        message = errors.build_message(text, error.index)
        raise DaleError(message)
