def _default_evaluator(value, context):
    return value


class Node:
    id = "node"

    def __init__(self):
        self.text = ""
        self.index = (0, 0)
        self.value = None
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
        self.attributes = {}
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
            self.flags[node.value] = node
        if node.id == "scope":
            self._add_scope(node)

    def _add_scope(self, node):
        """
            Handle adding a scope as a value of a scope node.
            Verify the type of the key node.
            (a (b 2)) -- 'b' will be set as an attribute of 'a'
        """
        key_map = {
            "property": self.children,
            "flag": self.flags,
            "uid": self.uids,
            "doc": self.docs,
            "attribute": self.attributes,
            "variable": self.variables,
            "format": self.formats,
        }
        key_id = node.key.id if node.key else ''
        if key_id in key_map:
            key_map[key_id][node.key.value] = node

    def eval(self, context):
        return {
            "id": self.id,
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
        self.value = []

    def __getitem__(self, index):
        return self.value[index]

    def __len__(self):
        return len(self.value)

    def add(self, node):
        self.value.append(node)

    def eval(self, context):
        return {
            "id": self.id,
            "value": [value.eval(context) for value in self.value]
        }


class PropertyNode(Node):
    id = "property"


class FlagNode(Node):
    id = "flag"


class UIDNode(Node):
    id = "uid"


class AttributeNode(Node):
    id = "attribute"


class FormatNode(Node):
    id = "format"


class VariableNode(Node):
    id = "variable"


class DocNode(Node):
    id = "doc"


class RangeNode(Node):
    id = "range"

    def __init__(self):
        super().__init__()
        self.value = (0, 0)

    def __getitem__(self, index):
        return self.value[index]


class IntNode(Node):
    id = "int"


class FloatNode(Node):
    id = "float"


class BooleanNode(Node):
    id = "boolean"


class StringNode(Node):
    id = "string"
