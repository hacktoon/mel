from dale.lexing import Lexer, TokenStream
from dale.parsing import Parser

from dale.exceptions import DaleError
from dale.exceptions.formatting import ErrorFormatter


def eval(text, context={}):
    try:
        tokens = Lexer(text).tokenize()
        stream = TokenStream(tokens)
        return Parser(stream).parse(context)
    except DaleError as error:
        message = ErrorFormatter(text, error).format(lines_offset=4)
        raise DaleError(message)
