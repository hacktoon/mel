def _default_evaluator(value, context):
    return value


class Node:
    id = "node"
    relation_key = False

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

    def _add_scope(self, node):
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

    def _add_relation(self, node):
        pass

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

    def __init__(self):
        super().__init__()
        self.criteria = []

    def _add_relation(self, node):
        pass


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
    relation_key = True


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


class RelationNode(Node):
    id = "relation"

    def __init__(self):
        super().__init__()
        self.target = None
        self.relationship = None
