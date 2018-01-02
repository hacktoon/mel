from dale.lexing import Lexer, TokenStream
from dale.parsing import Parser

from dale.types.errors import ErrorMessage, DaleError


def eval(text, context=None):
    try:
        tokens = Lexer(text).tokenize()
        stream = TokenStream(tokens)
        return Parser(stream).parse(context)
    except DaleError as error:
        message = ErrorMessage(text, error).build(line_range=4)
        raise DaleError(message)
