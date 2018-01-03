import pytest

import dale

from dale.exceptions.formatting import ErrorFormatter
from dale.exceptions import DaleError


def test_single_line_error_message_building():
    with pytest.raises(DaleError) as error:
        dale.eval('%')
    assert str(error.value) == (
        'Error at line 1, column 1.\n'
        'Invalid syntax.\n\n'
        '1 |    %\n'
        '-------^\n'
    )


def test_multiple_lines_error_message_building():
    with pytest.raises(DaleError) as error:
        dale.eval('(x 2)\n4$4\n33')
    assert str(error.value) == (
        'Error at line 2, column 2.\n'
        'Invalid syntax.\n\n'
        '1 |    (x 2)\n'
        '2 |    4$4\n'
        '--------^\n'
        '3 |    33\n'
    )
