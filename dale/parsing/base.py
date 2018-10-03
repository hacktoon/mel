class BaseParser:
    def __init__(self, stream):
        self.stream = stream

    def _create_node(self, node_class):
        node = node_class()
        node.text = self.stream.text
        return node
