def _default_evaluator(value, context):
    return value


class Node:
    id = "node"

    def __init__(self):
        self.key = None
        self.expressions = []
        self.text = ""
        self.index = (0, 0)

    def __bool__(self):
        return True

    def __len__(self):
        return len(self.expressions)

    def __str__(self):
        first, last = self.index
        return self.text[first:last]

    def __repr__(self):
        template = "{}('{}')"
        id = self.id.upper()
        return template.format(id, self)

    def __getitem__(self, index):
        return self.expressions[index]

    def __iter__(self):
        for node in self.expressions:
            yield node

    def add(self, node):
        method_name = "_add_" + node.id
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(node)
        self.expressions.append(node)

    def eval(self, context):
        return {
            "id": self.id,
            "nodes": [node.eval(context) for node in self.expressions]
        }


class NullNode(Node):
    id = "null"

    def __bool__(self):
        return False

    def __str__(self):
        return ""

    def eval(self, context):
        return


# EXPRESSSION =================================================

class ExpressionNode(Node):
    id = "expression"


class ObjectExpressionNode(Node):
    id = "object-expression"


# RELATION ========================================================

class RelationNode(Node):
    id = "relation"

    def __init__(self):
        super().__init__()
        self.key = NullNode()
        self.symbol = NullNode()
        self.value = NullNode()


class SymbolNode(Node):
    id = "symbol"


class EqualNode(SymbolNode):
    id = "equal"


class DifferentNode(SymbolNode):
    id = "different"


class GreaterThanNode(SymbolNode):
    id = "greater_than"


class GreaterThanEqualNode(SymbolNode):
    id = "greater_than_equal"


class LessThanNode(SymbolNode):
    id = "less_than"


class LessThanEqualNode(SymbolNode):
    id = "less_than_equal"


class InNode(SymbolNode):
    id = "in"


class NotInNode(SymbolNode):
    id = "not_in"


# VALUE ========================================================

class ValueNode(Node):
    id = "value"


# REFERENCE ========================================================

class ReferenceNode(Node):
    id = "reference"


class HeadReferenceNode(Node):
    id = "head-reference"


class ChildReferenceNode(Node):
    id = "child-reference"


# STRUCT ========================================================

class StructNode(Node):
    def __init__(self):
        super().__init__()
        self.key = NullNode()
        self.expressions = []


class PrototypeNode(StructNode):
    id = "prototype"


class ObjectNode(StructNode):
    id = "object"


class AnonymObjectNode(StructNode):
    id = "anonym-object"


class DefaultFormatNode(StructNode):
    id = "default-fortmat"


class DefaultDocNode(StructNode):
    id = "default-doc"


class QueryNode(StructNode):
    id = "query"


class AnonymQueryNode(StructNode):
    id = "anonym-query"


# LIST ========================================================

class ListNode(Node):
    id = "list"

    def eval(self, context):
        return {
            "id": self.id,
            "nodes": [node.eval(context) for node in self.expressions]
        }


# KEYWORD ========================================================

class KeywordNode(Node):
    id = "keyword"

    def __init__(self):
        super().__init__()
        self.value = ""


class NameNode(KeywordNode):
    id = "name"


class ConceptNode(NameNode):
    id = "concept"


class TagNode(KeywordNode):
    id = "tag"


class LogNode(KeywordNode):
    id = "log"


class AliasNode(KeywordNode):
    id = "alias"


class CacheNode(KeywordNode):
    id = "cache"


class FormatNode(KeywordNode):
    id = "format"


class MetaNode(Node):
    id = "meta"


class DocNode(KeywordNode):
    id = "doc"


# RANGE ========================================================

class RangeNode(Node):
    id = "range"

    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None


# LITERAL ========================================================

class LiteralNode(Node):
    id = "literal"

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


# PATH ========================================================

class PathNode(Node):
    id = "path"


# WILDCARD ========================================================

class WildcardNode(Node):
    id = "wildcard"
