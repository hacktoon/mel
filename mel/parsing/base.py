import functools

from ..exceptions import ParsingError


# decorator - add stream data to node instance via parser method
def indexed(parse_method):
    @functools.wraps(parse_method)
    def surrogate(self):
        first = self.stream.peek()
        node = parse_method(self)
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

    def _get_parser(self, _id, stream):
        if _id not in self.subparsers:
            Parser = ParserMap.get(_id)
            self.subparsers[_id] = Parser(stream, subparsers=self.subparsers)
        return self.subparsers[_id]

    def build_node(self):
        return self.Node()

    def read_rule(self, rule):
        parser = self._get_parser(rule, self.stream)
        index = self.stream.save()
        try:
            return parser.parse()
        except ParsingError as error:
            self.stream.restore(index)
            raise error

    def parse_alternative(self, *rules):
        for rule in rules:
            try:
                node = self.read_rule(rule)
                if isinstance(node, list):
                    for n in node:
                        return n
                else:
                    return node
            except ParsingError:
                pass
        raise ParsingError

    # TODO: read_once_repeat

    def parse_zero_many(self, rule):
        nodes = []
        while True:
            try:
                node = self.read_rule(rule)
                if isinstance(node, list):
                    for n in node:
                        nodes.append(n)
                else:
                    nodes.append(node)
            except ParsingError:
                break
        return nodes

    # TODO: remove later
    def parse_zero_many_alternative(self, *rules):
        nodes = []
        while True:
            try:
                node = self.parse_alternative(*rules)
                if isinstance(node, list):
                    for n in node:
                        nodes.append(n)
                else:
                    nodes.append(node)
            except ParsingError:
                break
        return nodes

    def parse_token(self, Token):
        token = self.stream.read(Token)
        if not token:
            raise ParsingError
        return token

    def error(self, Error, token=None):
        raise Error(token or self.stream.peek())

    def parse(self):
        raise NotImplementedError


class TokenParser(BaseParser):
    @indexed
    def parse(self):
        token = self.parse_token(self.Token)
        node = self.build_node()
        node.value = token.value
        return node
