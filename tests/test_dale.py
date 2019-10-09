import pytest

import mel
from mel.exceptions import MelError


@pytest.mark.skip()
def test_lex():
    stream = mel.lex("33 #")
    assert stream.peek()


@pytest.mark.skip()
def test_invalid_lex():
    with pytest.raises(MelError):
        mel.lex("~")


@pytest.mark.skip()
def test_create_parser():
    parser = mel.create_parser("answer 42")
    assert parser.parse()


@pytest.mark.skip()
def test_parse():
    tree = mel.parse("answer 42")
    assert len(tree) == 2


@pytest.mark.skip()
def test_invalid_parse():
    with pytest.raises(MelError):
        mel.parse("answer /")
