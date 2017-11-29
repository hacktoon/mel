from .lexing import TokenStream
from .types import nodes
from .types.errors import LexingError, ParsingError


class Parser:
    def __init__(self, text):
        self.text = text

    def parse(self):
        try:
            self.stream = TokenStream(self.text)
            return self._parse_root()
        except LexingError as error:
            raise ParsingError(error, self.text)

    def _parse_root(self):
        node = nodes.Node()
        while not self.stream.is_eof():
            node.add(self._parse_value())
        return node

    def _parse_expression(self):
        node = nodes.Expression()
        self.stream.read('StartExpression')
        node.add('keyword', self.stream.read('Name'))
        node.add('parameters', self._parse_parameters())
        self._parse_expression_value(node)
        self._parse_expression_end(node)
        return node

    def _parse_expression_value(self, node):
        while not self.stream.is_current('EndExpression'):
            if self.stream.is_eof():
                break
            node.add(self._parse_value())

    def _parse_expression_end(self, node):
        end = self.stream.read('EndExpression')
        is_named = len(end.value()) > 1
        is_same_keyword = end.value() != node.keyword.value()
        if is_named and is_same_keyword:
            raise ParsingError('expected a matching keyword', self.text)

    def _parse_parameters(self):
        node = nodes.Parameters()
        while self.stream.is_current('Parameter'):
            if self.stream.is_eof():
                break
            parameter = self.stream.read('Parameter')
            node.add(parameter.value(), self._parse_value())
        return node

    def _parse_value(self):
        parser_method = {
            'StartExpression': self._parse_expression,
            'StartList': self._parse_list,
            'Name': self._parse_reference,
            'Boolean': self._parse_boolean,
            'String': self._parse_string,
            'Float': self._parse_float,
            'Query': self._parse_query,
            'File': self._parse_file,
            'Int': self._parse_int
        }
        token = self.stream.current()
        try:
            node = parser_method[token.id]()
        except KeyError:
            message = 'unexpected {!r} while parsing'.format(token.id) #FIX change to str or repr
            raise LexingError(message, token.index)
        return node

    def _parse_list(self):
        node = nodes.List()
        self.stream.read('StartList')
        while not self.stream.is_current('EndList'):
            if self.stream.is_eof():
                break
            node.add(self._parse_value())
        self.stream.read('EndList')
        return node

    def _parse_reference(self):
        node = nodes.Reference()
        node.add(self.stream.read('Name'))
        while self.stream.is_current('Dot'):
            if self.stream.is_eof():
                break
            self.stream.read('Dot')
            node.add(self.stream.read('Name'))
        return node

    def _parse_string(self):
        node = nodes.String()
        node.add(self.stream.read('String'))
        return node

    def _parse_query(self):
        node = nodes.Query()
        node.add(self.stream.read('Query'))
        return node

    def _parse_file(self):
        node = nodes.File()
        node.add(self.stream.read('File'))
        return node

    def _parse_float(self):
        node = nodes.Float()
        node.add(self.stream.read('Float'))
        return node

    def _parse_int(self):
        node = nodes.Int()
        node.add(self.stream.read('Int'))
        return node

    def _parse_boolean(self):
        node = nodes.Boolean()
        node.add(self.stream.read('Boolean'))
        return node
