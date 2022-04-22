from ..scanning.parser.base import Parser
from ..scanning.parser.single import (
    ZeroManyParser,
    OptionalParser,
)
from ..scanning.parser.multi import (
    SeqParser,
)
from ..scanning.parser.char import (
    CharParser,
    DigitParser,
)


class Token:
    PARSER = Parser

    def __init__(self, id, chars):
        self.id = id
        self.chars = chars

    def hints(self):
        return

    def __repr__(self):
        classname = self.__class__.__name__
        text = ''.join(c.value for c in self.chars)
        return f'{classname}({text})'

    def __bool__(self):
        return len(self.chars)


class EOFToken(Token):
    def __init__(self):
        super().__init__('null', None)

    def __bool__(self):
        return False


class IntToken:
    PARSER = SeqParser(
        OptionalParser(CharParser('-')),
        DigitParser(),
        ZeroManyParser(
            DigitParser()
        )
    )
