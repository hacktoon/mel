from ..scanning.char import NewlineChar, SpaceChar
from ..scanning.parser.base import Parser
from ..scanning.parser.single import (
    OneManyParser,
    ZeroManyParser,
    OptionalParser,
)
from ..scanning.parser.multi import (
    SeqParser,
    OneOfParser
)
from ..scanning.parser.char import (
    CharParser,
    DigitParser,
    LowerParser,
    UpperParser,
    AlphaNumParser,
)


_TOKEN_TYPE_MAP = {}


class Token:
    PARSER = Parser
    HINTS = ''

    def __init__(self, id, chars):
        self.id = id
        self.chars = chars

    @staticmethod
    def parsers(hint_str: str):
        return _TOKEN_TYPE_MAP[hint_str]

    def __repr__(self):
        classname = self.__class__.__name__
        text = ''.join(c.value for c in self.chars)
        return f'{classname}({text})'

    def __bool__(self):
        return len(self.chars)


def _register_token(TokenClass: Token) -> Token:
    '''Build a {char_str: parsers} dict for tokens'''
    for hint_str in TokenClass.HINTS:
        if hint_str not in _TOKEN_TYPE_MAP:
            _TOKEN_TYPE_MAP[hint_str] = []
        _TOKEN_TYPE_MAP[hint_str].append(TokenClass.PARSER)
    return TokenClass


class EOFToken(Token):
    def __init__(self):
        super().__init__('null', None)

    def __bool__(self):
        return False


@_register_token
class FloatToken(Token):
    ID = 'float'
    PARSER = SeqParser(
        OptionalParser(CharParser('-')),
        OneManyParser(DigitParser()),
        CharParser('.'),
        OneManyParser(DigitParser()),
    )


@_register_token
class IntToken(Token):
    ID = 'int'
    PARSER = SeqParser(
        OptionalParser(CharParser('-')),
        DigitParser(),
        ZeroManyParser(DigitParser())
    )


@_register_token
class NameToken(Token):
    ID = 'name'
    PARSER = SeqParser(
        LowerParser(),
        ZeroManyParser(
            OneOfParser(CharParser('_'), AlphaNumParser())
        )
    )


@_register_token
class ConceptToken(Token):
    ID = 'concept'
    PARSER = SeqParser(
        UpperParser(),
        ZeroManyParser(
            OneOfParser(CharParser('_'), AlphaNumParser())
        )
    )


@_register_token
class WhitespaceToken(Token):
    ID = 'whitespace'
    PARSER = ZeroManyParser(
        OneOfParser(NewlineChar(), SpaceChar())
    )
