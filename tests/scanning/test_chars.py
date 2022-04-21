from mel.scanning.char import Char


# HELPER FUNCTIONS ==================================


# BEGIN  TESTS ==================================

def test_char():
    ch = Char.build('a')
    assert repr(ch) == 'LowerChar(a)'


def test_empty_base_char():
    ch = Char()
    assert ch.value == ''


def test_char_type():
    ch = Char.build('4')
    assert ch.is_digit()
