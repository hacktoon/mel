import sys
import dale
from dale.types.errors import DaleError


def _read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except IOError:
        sys.exit('The file {!r} doesn\'t exist.'.format(path))


def _read_path():
    try:
        return sys.argv[1]
    except IndexError:
        sys.exit('A source file is required.')


def main():
    path = _read_path()
    text = _read_file(path)
    try:
        print(dale.eval(text))
    except DaleError as error:
        sys.exit('File {!r}: \n\n{}'.format(path, error))


if __name__ == '__main__':
    main()
