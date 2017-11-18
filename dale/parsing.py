from .lexing import TokenStream
from .data import nodes
from .data import tokens
from .data.errors import LexingError, ParsingError


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
        content_node = nodes.Content()
        while not self.stream.is_eof():
            content_node.add(self._parse_content())
        return content_node

    def _parse_content(self):
        token = self.stream.get()
        if token == tokens.OpenExpressionToken:
            return self._parse_expression()
        else:
            return self._parse_value()

    def _parse_expression(self):
        token = self.stream.consume(tokens.OpenExpressionToken)
        node = nodes.Expression(token)
        node.keyword = self.stream.consume(tokens.KeywordToken)
        node.parameters = self._parse_parameter_list()
        while self.stream.get() != tokens.CloseExpressionToken:
            if self.stream.is_eof():
                break
            node.add(self._parse_content())
        self.stream.consume(tokens.CloseExpressionToken)
        return node

    def _parse_parameter_list(self):
        node = nodes.ParameterList()
        while self.stream.get() == tokens.ParameterToken:
            if self.stream.is_eof():
                break
            key = self.stream.consume(tokens.ParameterToken)
            value = self._parse_value()
            parameter = nodes.Parameter(key, value)
            node.add(parameter)
        return node

    def _parse_value(self):
        value_parser_function = {
            tokens.ReferenceToken: self._parse_reference,
            tokens.BooleanToken: self._parse_boolean,
            tokens.StringToken: self._parse_string,
            tokens.FloatToken: self._parse_float,
            tokens.QueryToken: self._parse_query,
            tokens.IntToken: self._parse_int
        }
        token = self.stream.get()
        try:
            node = value_parser_function[token.__class__]()
        except KeyError:
            message = 'unexpected {!r} while parsing'.format(token.name)
            raise LexingError(message, token.index)
        return node

    def _parse_reference(self):
        token = self.stream.consume(tokens.ReferenceToken)
        return nodes.Reference(token)

    def _parse_string(self):
        token = self.stream.consume(tokens.StringToken)
        return nodes.String(token)

    def _parse_query(self):
        token = self.stream.consume(tokens.QueryToken)
        return nodes.Query(token)

    def _parse_float(self):
        token = self.stream.consume(tokens.FloatToken)
        return nodes.Float(token)

    def _parse_int(self):
        token = self.stream.consume(tokens.IntToken)
        return nodes.Int(token)

    def _parse_boolean(self):
        token = self.stream.consume(tokens.BooleanToken)
        return nodes.Boolean(token)
