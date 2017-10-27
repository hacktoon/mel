import sys
from dale.parsing import Parser
from dale.data.errors import ParsingError


def _read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except IOError:
        sys.exit('The file {!r} doesn\'t exist.'.format(path))


def run(path):
    source = _read_file(path)
    try:
        tree = Parser(source).parse()
        print(tree)
    except ParsingError as error:
        sys.exit('File {!r}:\n{}'.format(path, error))


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit('A source file is required.')
    run(path)
