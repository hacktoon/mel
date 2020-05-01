
# class BaseNode:
#     def __bool__(self):
#         return True

#     def __len__(self):
#         return 0

#     def __repr__(self):
#         return f'{self.__class__.__name__}()'


# class StringNode(BaseNode):
#     def __init__(self, text='', index=(0, 0)):
#         self.text = text
#         self.index = index

#     def __len__(self):
#         return len(self.text)

#     def __repr__(self):
#         return f'String({self.text})'


# class PatternNode(StringNode):
#     def __repr__(self):
#         return f'Pattern({self.text})'


# class Node(BaseNode):
#     def __init__(self):
#         self.children = []

#     def __bool__(self):
#         return len(self.children) > 0

#     def __len__(self):
#         return len(self.children)

#     def __repr__(self):
#         name = self.__class__.__name__
#         children = ', '.join(repr(child) for child in self.children)
#         return f'{name}({children})'

#     def __getitem__(self, index):
#         return self.children[index]

#     @property
#     def index(self):
#         if len(self) == 0:
#             return (0, 0)
#         first = self.children[0].index
#         last = self.children[-1].index
#         return (first[0], last[1])

#     def add(self, *children):
#         for child in children:
#             self.children.append(child)


# class RuleNode(Node):
#     def __init__(self, id):
#         super().__init__()
#         self.id = id

#     def __repr__(self):
#         name = self.__class__.__name__
#         children = ', '.join(repr(child) for child in self.children)
#         return f'{name}("{self.id}", {children})'


# class RootNode(Node):
#     pass


# class ZeroManyNode(Node):
#     pass


# class OneManyNode(Node):
#     pass


# class OptionalNode(Node):
#     pass


# class OneOfNode(Node):
#     pass
