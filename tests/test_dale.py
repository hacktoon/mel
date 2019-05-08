import pytest

import dale
from dale.exceptions import DaleError


def test_lex():
    stream = dale.lex("33 #")
    assert stream.peek()


def test_invalid_lex():
    with pytest.raises(DaleError):
        dale.lex("~")


def test_create_parser():
    parser = dale.create_parser("answer 42")
    assert parser.parse()


def test_parse():
    tree = dale.parse("answer 42")
    assert len(tree) == 2


def test_invalid_parse():
    with pytest.raises(DaleError):
        dale.parse("answer /")
