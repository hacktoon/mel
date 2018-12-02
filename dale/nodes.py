def _default_evaluator(value, context):
    return value


class Node:
    id = "node"

    def __init__(self):
        self.text = ""
        self.index = (0, 0)
        self._chain = []

    def __bool__(self):
        return True

    def __str__(self):
        first, last = self.index
        return self.text[first:last]

    def __repr__(self):
        return "{}('{}')".format(self.id.upper(), self)

    def chain(self, node):
        self._chain.append(node)

    def eval(self, context):
        return None


class WildcardNode(Node):
    id = "wildcard"


class ScopeNode(Node):
    id = "scope"

    def __init__(self):
        super().__init__()
        self.key = None
        self.values = []
        self.flags = {}
        self.uids = {}
        self.properties = {}
        self.variables = {}
        self.formats = {}
        self.docs = {}
        self.children = {}

    def __getitem__(self, index):
        return self.values[index]

    def __len__(self):
        return len(self.values)

    def add(self, node):
        self.values.append(node)
        if node.id == "flag":
            self.flags[node.name] = node
        if node.id == "scope":
            self._add_scope(node)

    def _add_scope(self, node):
        key_map = {
            "property": self.children,
            "flag": self.flags,
            "uid": self.uids,
            "doc": self.docs,
            "variable": self.variables,
            "format": self.formats,
        }
        key_id = node.key.id if node.key else ''
        if key_id in key_map:
            key_map[key_id][node.key.name] = node

    def eval(self, context):
        return {
            "key": self.key.eval(context) if self.key else None,
            "values": [value.eval(context) for value in self.values]
        }


class RootNode(ScopeNode):
    id = "root"


class QueryNode(ScopeNode):
    id = "query"


class ListNode(Node):
    id = "list"

    def __init__(self):
        super().__init__()
        self.values = []

    def __getitem__(self, index):
        return self.values[index]

    def __len__(self):
        return len(self.values)

    def add(self, node):
        self.values.append(node)

    def eval(self, context):
        return [value.eval(context) for value in self.values]


class PropertyNode(Node):
    id = "property"

    def __init__(self):
        super().__init__()
        self.name = ""

    def eval(self, context):
        return self.name


class FlagNode(PropertyNode):
    id = "flag"


class UIDNode(PropertyNode):
    id = "uid"


class AttributeNode(PropertyNode):
    id = "attribute"


class FormatNode(PropertyNode):
    id = "format"


class VariableNode(PropertyNode):
    id = "variable"


class DocNode(PropertyNode):
    id = "doc"


class LiteralNode(Node):
    def __init__(self):
        super().__init__()
        self.value = None

    def eval(self, context):
        return self.value


class IntNode(LiteralNode):
    id = "int"


class FloatNode(LiteralNode):
    id = "float"


class BooleanNode(LiteralNode):
    id = "boolean"


class StringNode(LiteralNode):
    id = "string"
