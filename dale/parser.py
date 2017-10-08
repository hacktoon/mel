from .lexer import Lexer
from .token import TokenStream, TokenType
from . import node
from .error import SyntaxError, ParserError


def build_error_message(error, text):
    line_index = error.line
    message = str(error)
    line = text.split('\n')[line_index]
    template = 'Syntax error: {} at line {}:\n{}\n{}^'
    return template.format(message, line_index + 1, line, ' ' * error.column)


class Parser:
    def __init__(self, text):
        self.text = text

    def parse(self):
        try:
            self.tokens = TokenStream(Lexer(self.text).tokenize())
            return self._parse_root()
        except SyntaxError as error:
            message = build_error_message(error, self.text)
            raise ParserError(message)

    def _parse_root(self):
        content_node = node.Content()
        while not self.tokens.is_eof():
            content_node.add(self._parse_content())
        return content_node

    def _parse_content(self):
        if self.tokens.get().type == TokenType.OPEN_EXP:
            return self._parse_expression()
        if self.tokens.get().type == TokenType.COMMENT:
            self.tokens.consume(TokenType.COMMENT)
        return self._parse_value()

    def _parse_expression(self):
        token = self.tokens.consume(TokenType.OPEN_EXP)
        expression_node = node.Expression(token)
        expression_node.identifier = self._parse_identifier()
        if self.tokens.get().type == TokenType.OPEN_PARAM:
            expression_node.parameter_list = self._parse_parameter_list()
        while self.tokens.get().type != TokenType.CLOSE_EXP:
            expression_node.add(self._parse_content())
        self.tokens.consume(TokenType.CLOSE_EXP)
        return expression_node

    def _parse_identifier(self):
        token = self.tokens.consume(TokenType.IDENTIFIER)
        identifier_node = node.Identifier(token)
        identifier_node.add(token.value)
        while self.tokens.get().type == TokenType.DOT:
            self.tokens.consume(TokenType.DOT)
            token = self.tokens.consume(TokenType.IDENTIFIER)
            identifier_node.add(token.value)
        return identifier_node

    def _parse_parameter_list(self):
        token = self.tokens.consume(TokenType.OPEN_PARAM)
        param_list = node.ParameterList(token)
        while self.tokens.get().type != TokenType.CLOSE_PARAM:
            param_list.add(self._parse_parameter())
            if self.tokens.get().type == TokenType.COMMA:
                self.tokens.consume(TokenType.COMMA)
            else:
                break
        self.tokens.consume(TokenType.CLOSE_PARAM)
        return param_list

    def _parse_parameter(self):
        identifier = self._parse_identifier()
        self.tokens.consume(TokenType.COLON)
        return node.Parameter(identifier, self._parse_value())

    def _parse_value(self):
        value_parser_function = {
            TokenType.IDENTIFIER: self._parse_identifier,
            TokenType.OPEN_LIST: self._parse_list,
            TokenType.BOOLEAN: self._parse_boolean,
            TokenType.STRING: self._parse_string,
            TokenType.FLOAT: self._parse_float,
            TokenType.QUERY: self._parse_query,
            TokenType.INT: self._parse_int
        }
        token = self.tokens.get()
        try:
            value_node = value_parser_function[token.type]()
        except KeyError:
            message = 'unexpected {!r} while parsing'.format(token.type.value)
            raise SyntaxError(message, token.line, token.column)
        return value_node

    def _parse_string(self):
        token = self.tokens.consume(TokenType.STRING)
        return node.String(token)

    def _parse_query(self):
        token = self.tokens.consume(TokenType.QUERY)
        return node.Query(token)

    def _parse_float(self):
        token = self.tokens.consume(TokenType.FLOAT)
        return node.Float(token)

    def _parse_int(self):
        token = self.tokens.consume(TokenType.INT)
        return node.Int(token)

    def _parse_boolean(self):
        token = self.tokens.consume(TokenType.BOOLEAN)
        return node.Boolean(token)

    def _parse_list(self):
        token = self.tokens.consume(TokenType.OPEN_LIST)
        list_node = node.List(token)
        is_eof = self.tokens.is_eof()
        while self.tokens.get().type != TokenType.CLOSE_LIST:
            list_node.add(self._parse_value())
            if self.tokens.get().type == TokenType.COMMA:
                self.tokens.consume(TokenType.COMMA)
            else:
                break
        self.tokens.consume(TokenType.CLOSE_LIST)
        return list_node
