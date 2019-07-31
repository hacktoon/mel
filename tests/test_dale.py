import pytest

import mel
from mel.exceptions import MelError


def test_lex():
    stream = mel.lex("33 #")
    assert stream.peek()


def test_invalid_lex():
    with pytest.raises(MelError):
        mel.lex("~")


def test_create_parser():
    parser = mel.create_parser("answer 42")
    assert parser.parse()


def test_parse():
    tree = mel.parse("answer 42")
    assert len(tree) == 2


def test_invalid_parse():
    with pytest.raises(MelError):
        mel.parse("answer /")
