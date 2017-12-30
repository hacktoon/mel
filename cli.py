import sys
from dale.lexing import Lexer, TokenStream
from dale.parsing import Parser
from dale.types.errors import DaleError
from dale.types import tokens


def _read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except IOError:
        sys.exit('The file {!r} doesn\'t exist.'.format(path))


def evaluate(text, context=None):
    tokens = Lexer(text).tokenize()
    stream = TokenStream(tokens)
    tree = Parser(stream).parse(context)
    print(tree)


if __name__ == '__main__':
    try:
        path = sys.argv[1]
        evaluate(_read_file(path))
    except IndexError:
        sys.exit('A source file is required.')
    except DaleError as error:
        sys.exit('File {!r}:\n{}'.format(path, error))
