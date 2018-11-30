from .base import BaseParser
from ..nodes import ListNode


class ListParser(BaseParser):
    def __init__(self, parser):
        super().__init__(parser.stream)
        self.parser = parser
        self.delimiter_tokens = ("[", "]")

    def parse(self):
        start_token, end_token = self.delimiter_tokens
        if not self.stream.is_current(start_token):
            return
        node = self._create_node(ListNode)
        self.stream.read(start_token)
        self._parse_values(node)
        self.stream.read(end_token)
        return node

    def _parse_values(self, node):
        end_token = self.delimiter_tokens[1]
        inside_list = not self.stream.is_current(end_token)
        not_eof = not self.stream.is_eof()
        while inside_list and not_eof:
            value = self.parser.parse_value()
            if not value:
                break
            node.add(value)
