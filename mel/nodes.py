
class Node:
    def __init__(self, id=None, text='', index=(0, 0)):
        self.id = id
        self.text = text
        self.index = index
        self.children = []

    def __bool__(self):
        return True

    def __str__(self):
        return self.text

    def __repr__(self):
        template = "{}"
        return template.format(self)

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        for node in self.children:
            yield node

    def __getitem__(self, index):
        return self.children[index]

    def add(self, node):
        self.children.append(node)

    def eval(self):
        pass
