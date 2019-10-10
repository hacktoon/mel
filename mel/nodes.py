
class Node:
    def __init__(self, value):
        self.value = value
        self.subnodes = []

    def __bool__(self):
        return True

    def __str__(self):
        # first, last = self.index
        return ''  # self.text[first:last]

    def __repr__(self):
        template = "{}('{}')"
        id = self.id.upper()
        return template.format(id, self)

    def __len__(self):
        return len(self.subnodes)

    def __iter__(self):
        for node in self.subnodes:
            yield node

    def __getitem__(self, index):
        return self.subnodes[index]

    def add(self, node):
        self.subnodes.append(node)

    def eval(self):
        pass
