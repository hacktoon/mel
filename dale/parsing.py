from . import nodes


def text_range(first, last=None):
    if last:
        return first.index[0], last.index[1]
    return first.index[0], first.index[1]


class Parser:
    def __init__(self, stream):
        self.stream = stream

    def parse(self):
        node = self._create_node(nodes.Node)
        while not self.stream.is_eof():
            reference = self._parse_reference()
            if reference:
                node.add(reference)
        node.index = 0, len(self.stream.text)
        return node

    def _parse_reference(self):
        first = last = self._parse_value()
        if not first:
            return
        node = self._create_node(nodes.ReferenceNode)
        while self.stream.is_current('/'):
            self.stream.read('/')
            last = self._parse_value()
            node.add(last)
        node.index = text_range(first, last)
        return node

    def _parse_value(self):
        methods = [
            self._parse_literal,
            self._parse_scope,
            self._parse_prefixed_property,
            self._parse_property,
            self._parse_query,
            self._parse_list
        ]
        for method in methods:
            node = method()
            if node:
                return node
        return

    def _parse_literal(self):
        node_map = {
            'boolean': nodes.BooleanNode,
            'string': nodes.StringNode,
            'float': nodes.FloatNode,
            'int': nodes.IntNode
        }
        token = self.stream.current()
        if token.id not in node_map:
            return
        node = self._create_node(node_map[token.id])
        node.token = token
        node.index = text_range(token)
        return node

    def _parse_prefixed_property(self):
        node_map = {
            '#': nodes.UIDNode,
            '!': nodes.FlagNode,
            '@': nodes.AttributeNode,
            '%': nodes.FormatNode,
            '~': nodes.AliasNode,
            '?': nodes.DocNode
        }
        prefix = self.stream.current()
        if prefix.id not in node_map:
            return
        self.stream.read(prefix.id)
        node = self._create_node(node_map[prefix.id])
        node.name = self.stream.read('name')
        node.index = text_range(prefix, node.name)
        return node

    def _parse_property(self):
        if not self.stream.is_current('name'):
            return
        node = self._create_node(nodes.PropertyNode)
        node.name = self.stream.read('name')
        node.text_range = text_range(node.name)
        return node

    def _parse_scope(self):
        node = self._create_node(nodes.ScopeNode)
        if not self.stream.is_current('('):
            return
        first = self.stream.read('(')
        if not self.stream.is_current(')'):
            node.key = self._parse_reference()
        while not self.stream.is_current(')'):
            reference = self._parse_reference()
            if reference:
                node.add(reference)
        last = self.stream.read(')')
        node.index = text_range(first, last)
        return node

    def _parse_query(self):
        node = self._create_node(nodes.QueryNode)
        if not self.stream.is_current('{'):
            return
        first = self.stream.read('{')
        if not self.stream.is_current('}'):
            node.key = self._parse_reference()
        while not self.stream.is_current('}'):
            reference = self._parse_reference()
            if reference:
                node.add(reference)
        last = self.stream.read('}')
        node.index = text_range(first, last)
        return node

    def _parse_list(self):
        node = self._create_node(nodes.ListNode)
        if not self.stream.is_current('['):
            return
        first = self.stream.read('[')
        while not self.stream.is_current(']'):
            reference = self._parse_reference()
            if reference:
                node.add(reference)
        last = self.stream.read(']')
        node.index = text_range(first, last)
        return node

    def _create_node(self, node_class):
        node = node_class()
        node.text = self.stream.text
        return node
