import functools


_subparsers = {}


@functools.lru_cache()
def get_subparser(id, stream):
    if id in _subparsers:
        return _subparsers[id](stream)
    raise Exception('Invalid subparser: ' + id)


# decorator - register a Parser class as a subparser
def subparser(cls):
    _subparsers[cls.__name__] = cls
    return cls


# decorator - add stream data to node instance via parser method
def indexed(parse_method):
    @functools.wraps(parse_method)
    def surrogate(self):
        first = self.stream.peek()
        node = parse_method(self)
        if not node:
            return
        last = self.stream.peek(-1)
        node.index = first.index[0], last.index[1]
        node.text = self.stream.text
        return node
    return surrogate


class BaseParser:
    def __init__(self, stream):
        self.stream = stream

    def build_node(self):
        return self.Node()

    def subparse(self, Parser):
        return get_subparser(Parser.__name__, self.stream).parse()

    def error(self, Error, token=None):
        raise Error(token or self.stream.peek())


class MultiParser(BaseParser):
    options = tuple()

    @indexed
    def parse(self):
        for option in self.options:
            node = self.subparse(option)
            if node:
                return node
        return


class TokenParser(BaseParser):
    @indexed
    def parse(self):
        if not self.stream.is_next(self.Token):
            return
        node = self.build_node()
        node.value = self.stream.read().value
        return node
