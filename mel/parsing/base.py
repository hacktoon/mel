import functools


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
    def __init__(self, stream, subparsers=None):
        self.stream = stream
        self._subparsers = subparsers or {}

    def build_node(self):
        return self.Node()

    def subparse(self, Parser):
        subparser = self.get_subparser(Parser, self.stream)
        return subparser.parse()

    def get_subparser(self, Parser, stream):
        name = Parser.__name__
        if name not in self._subparsers:
            parser = Parser(stream, subparsers=self._subparsers)
            self._subparsers[name] = parser
        return self._subparsers[name]

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
