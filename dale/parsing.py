from dale.lexing import TokenStream
from .types import nodes
from .types.errors import ParsingError


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        node = self._create_node()
        while not self.stream.is_eof():
            node.add(self._parse_value())
        return node

    def _create_node(self, node_id=None):
        return nodes.create(node_id or 'Node', self.stream)

    def _parse_expression(self):
        node = self._create_node('Expression')
        self.stream.read('LeftParen')
        node.add('keyword', self.stream.read('Name'))
        node.add('parameters', self._parse_parameters())
        self._parse_expression_value(node)
        self._parse_expression_end(node)
        return node

    def _parse_expression_value(self, node):
        while not self.stream.is_current('RightParen'):
            if self.stream.is_eof():
                break
            node.add(self._parse_value())

    def _parse_expression_end(self, node):
        self.stream.read('RightParen')
        if self.stream.is_current('Name') and self.stream.is_next('RightParen'):
            self.stream.read('Name', value=node.keyword.value)
            self.stream.read('RightParen')

    def _parse_parameters(self):
        node = self._create_node('Parameters')
        while self.stream.is_current('Parameter'):
            parameter = self.stream.read('Parameter')
            node.add(parameter.value, self._parse_value())
        return node

    def _parse_value(self):
        parser_method = {
            'LeftParen': self._parse_expression,
            'Boolean': self._parse_boolean,
            'LeftBracket': self._parse_list,
            'Name': self._parse_reference,
            'String': self._parse_string,
            'Float': self._parse_float,
            'Query': self._parse_query,
            'Int': self._parse_int
        }
        token = self.stream.current()
        try:
            node = parser_method[token.id]()
        except KeyError:
            message = 'unexpected {!r} while parsing'.format(token.id) #FIX change to str or repr
            raise ParsingError(message)
        return node

    def _parse_list(self):
        node = self._create_node('List')
        self.stream.read('LeftBracket')
        while not self.stream.is_current('RightBracket'):
            if self.stream.is_eof():
                token = self.stream.current()
                raise ParsingError('unexpected EOF while parsing list')
            node.add(self._parse_value())
        self.stream.read('RightBracket')
        return node

    def _parse_reference(self):
        node = self._create_node('Reference')
        node.add(self.stream.read('Name'))
        while self.stream.is_current('Dot'):
            self.stream.read('Dot')
            node.add(self.stream.read('Name'))
        return node

    def _parse_string(self):
        node = self._create_node('String')
        node.add(self.stream.read('String'))
        return node

    def _parse_query(self):
        node = self._create_node('Query')
        self.stream.read('Query')
        if self.stream.is_current('Name'):
            node.add('source', self.stream.read('Name').value)
        else:
            node.add('source', '')
        node.add('content', self.stream.read('String'))
        return node

    def _parse_float(self):
        node = self._create_node('Float')
        node.add(self.stream.read('Float'))
        return node

    def _parse_int(self):
        node = self._create_node('Int')
        node.add(self.stream.read('Int'))
        return node

    def _parse_boolean(self):
        node = self._create_node('Boolean')
        node.add(self.stream.read('Boolean'))
        return node
