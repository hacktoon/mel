
class Node:
    def __init__(self):
        self.text = ""
        self.index = (0, 0)

    def __bool__(self):
        return True

    def __str__(self):
        first, last = self.index
        return self.text[first:last]

    def __repr__(self):
        template = "{}('{}')"
        id = self.id.upper()
        return template.format(id, self)

    def eval(self):
        return str(self)


class CompoundNode(Node):
    def __init__(self):
        super().__init__()
        self.expressions = []

    def __len__(self):
        return len(self.expressions)

    def __iter__(self):
        for node in self.expressions:
            yield node

    def __getitem__(self, index):
        return self.expressions[index]

    def add(self, node):
        self.expressions.append(node)

    def eval(self):
        return [expr.eval() for expr in self.expressions]


# STRUCT =================================================

class StructNode(CompoundNode):
    def eval(self):
        return [expr.eval() for expr in self.expressions]


class RootNode(StructNode):
    id = "root"


class KeyStructNode(StructNode):
    def __init__(self):
        super().__init__()
        self.key = None


class ObjectNode(KeyStructNode):
    id = "object"


class AnonymObjectNode(KeyStructNode):
    id = "anonym-object"


class DefaultFormatNode(KeyStructNode):
    id = "default-format"


class DefaultDocNode(KeyStructNode):
    id = "default-doc"


class QueryNode(KeyStructNode):
    id = "query"


class AnonymQueryNode(KeyStructNode):
    id = "anonym-query"


# EXPRESSION =================================================

class ExpressionNode(Node):
    id = "expression"


class ObjectExpressionNode(Node):
    id = "object-expression"


# RELATION ========================================================

class RelationNode(Node):
    id = "relation"

    def __init__(self):
        super().__init__()
        self.key = None
        self.sign = None
        self.value = None


class SignNode(Node):
    id = "sign"


class EqualNode(SignNode):
    id = "equal"


class DifferentNode(SignNode):
    id = "different"


class GreaterThanNode(SignNode):
    id = "greater_than"


class GreaterThanEqualNode(SignNode):
    id = "greater_than_equal"


class LessThanNode(SignNode):
    id = "less_than"


class LessThanEqualNode(SignNode):
    id = "less_than_equal"


class InNode(SignNode):
    id = "in"


class NotInNode(SignNode):
    id = "not_in"


# VALUE ========================================================

class ValueNode(Node):
    id = "value"


# REFERENCE ========================================================

class ReferenceNode(CompoundNode):
    id = "reference"


class HeadReferenceNode(Node):
    id = "head-reference"


class ChildReferenceNode(Node):
    id = "child-reference"


# LIST ========================================================

class ListNode(CompoundNode):
    id = "list"


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


class MetaNode(KeywordNode):
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

    def eval(self):
        return self.value


class IntNode(LiteralNode):
    id = "int"


class FloatNode(LiteralNode):
    id = "float"


class BooleanNode(LiteralNode):
    id = "boolean"


class StringNode(LiteralNode):
    id = "string"


class TemplateStringNode(LiteralNode):
    id = "template-string"


# PATH ========================================================

class PathNode(CompoundNode):
    id = "path"


# WILDCARD ========================================================

class WildcardNode(Node):
    id = "wildcard"
