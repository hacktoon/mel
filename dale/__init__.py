from dale.lexing import TokenStream
from dale.parsing import Parser

from dale.utils.context import Context
from dale.exceptions import DaleError
from dale.exceptions.formatting import ErrorFormatter


def eval(text, context=Context()):
    try:
        stream = TokenStream(text)
        tree = Parser(stream).parse()

        # put AST in global context
        context.var('tree', tree)

        return tree.eval(context)
    except DaleError as error:
        message = ErrorFormatter(text, error).format(lines_offset=4)
        raise DaleError(message)
