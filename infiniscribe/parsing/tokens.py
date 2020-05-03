from .chars import CharStream
from dataclasses import dataclass


def tok(id):
    def token_parser(stream):
        return stream.read(id)
    return token_parser


# default TokenStream, can be exchanged in Language build
class TokenStream:
    def __init__(self, text):
        self.index = 0
        self.chars = CharStream(text.rstrip())
        # self.tokens = tokenize()

    def read(self, id):
        pass


# # Helper reading methods =====================================
#     def read_whitespace(self):
#         return self.read_many([SPACE, NEWLINE])

#     def read_integers(self):
#         return self.read_many([DIGIT])

#     def read_letters(self):
#         return self.read_many([LOWER, UPPER])

#     def read_lower_letters(self):
#         return self.read_many([LOWER])

#     def read_upper_letters(self):
#         return self.read_many([UPPER])

#     def read_lower_name(self):
#         first = self.read_many([LOWER])
#         if not first:
#             return []
#         rest = self.read_letters()
#         return first + rest

#     def read_capital_name(self):
#         first = self.read_many([UPPER])
#         if not first:
#             return []
#         rest = self.read_letters()
#         return first + rest

# def tokenize(text):
#     tokens = []
#     token_spec = TokenSpec(LEXING_TABLE)
#     char_stream = CharStream(text)
#     while not char_stream.eof:
#         (id, skip, pattern, _) = token_spec.get(char_stream.head_char)
#         match_text, index = char_stream.read_pattern(pattern)
#         if skip:
#             continue
#         token = Token(id, match_text)
#         tokens.append(token)
#     return tokens


@dataclass
class Token:
    id: int
    text: str


# LEXING_TABLE = {
#     # Symbols are simple strings
#     # Symbol priority is defined by order
#     'symbols': (
#         '..',
#         '.', '/', '*',
#         ':', '?:', '%:',
#         '(', ')', '[', ']', '{', '}',
#         '=', '!=', '<>', '><', '<=', '>=', '>', '<',
#         '!', '@', '#', '$', '%', '?',
#     ),

#     # Patterns are regular expressions
#     # Skip patterns are ignored on stream
#     # Defines hints string to prefetch patterns on parsing
#     # Pattern priority is defined by order
#     'patterns': (
#         # ID          PATTERN                SKIP  HINTS
#         ('space',     r'[,\s]+',             1,    string.whitespace + ','),
#         ('comment',   r'--[^\r\n]*',         1,    '-'),
#         ('concept',   r'[A-Z][_A-Za-z]+',    0,    string.ascii_uppercase),
#         ('name',      r'[a-z][_a-z]+',       0,    string.ascii_lowercase),
#         ('float',     r'-?[0-9](.[0-9]+)?',  0,    string.digits + '-'),
#         ('int',       r'-?[0-9]+',           0,    string.digits + '-'),
#         ('string',    r"'[^']*'",            0,    "'"),
#         ('template',  r'"[^"]*"',            0,    '"'),
#     )
# }
