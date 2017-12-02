from dale.types import tokens
from dale.types.nodes import Node


def test_addition_of_children_to_node():
    node = Node()
    node.add(5)
    node.add(8)
    assert node[0] == 5
    assert node[1] == 8


def test_node_size_is_determined_by_the_number_of_children():
    node = Node()
    assert len(node) == 0
    node.add(5)
    node.add(8)
    assert len(node) == 2


def test_adding_and_retrieving_properties():
    node = Node()
    node.add('five', 5)
    node.add('six', 6)
    assert node.five == 5
    assert node.six == 6


def test_retrieving_child_properties_as_dict_keys():
    node = Node()
    node.add('fruit', 'apple')
    node.add('name', 'Mary')
    assert node['fruit'] == 'apple'
    assert node['name'] == 'Mary'


def test_getting_node_value_returns_a_list_of_children_values():
    node = Node()
    node.add(tokens.Token('Inception'))
    node.add(tokens.Token('Jurassic Park'))
    assert node.value == ['Inception', 'Jurassic Park']