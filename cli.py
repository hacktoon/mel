import sys
from dale.lexing import TokenStream
from dale.parsing import Parser
from dale.types.errors import ParsingError


def _read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except IOError:
        sys.exit('The file {!r} doesn\'t exist.'.format(path))


def evaluate(text, context=None):
    stream = TokenStream(text)
    tree = Parser(stream).parse()
    print(tree)


if __name__ == '__main__':
    try:
        path = sys.argv[1]
        evaluate(_read_file(path))
    except IndexError:
        sys.exit('A source file is required.')
    except ParsingError as error:
        sys.exit('File {!r}:\n{}'.format(path, error))
