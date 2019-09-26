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


# decorator - register parsing classes as subparsers in ParserMap
def subparser(cls):
    ParserMap.set(cls)
    return cls


# references parser classes by its id
class ParserMap:
    _map = {}

    @classmethod
    def set(cls, _parser):
        cls._map[_parser.id] = _parser

    @classmethod
    def get(cls, _id):
        return cls._map.get(_id)


# BASE PARSER =============================================

class BaseParser:
    def __init__(self, stream, subparsers=None):
        self.stream = stream
        # TODO: convert to parsing_context?
        self.subparsers = subparsers or {}

    def parse(self):
        raise NotImplementedError

    def build_node(self):
        return self.Node()

    def read(self, _id):
        parser = self._get_parser(_id, self.stream)
        return parser.parse()

    def read_optional(self, _id):
        parser = self._get_parser(_id, self.stream)
        return parser.parse()

    def read_any(self, ids):
        for _id in ids:
            node = self.read(_id)
            if node:
                return node
        return

    def read_token(self, Token):
        if not self.stream.is_next(Token):
            return
        return self.stream.read()

    def error(self, Error, token=None):
        raise Error(token or self.stream.peek())

    def _get_parser(self, _id, stream):
        if _id not in self.subparsers:
            Parser = ParserMap.get(_id)

            self.subparsers[_id] = Parser(stream, subparsers=self.subparsers)
        return self.subparsers[_id]


class TokenParser(BaseParser):
    @indexed
    def parse(self):
        token = self.read_token(self.Token)
        if not token:
            return
        node = self.build_node()
        node.value = token.value
        return node
