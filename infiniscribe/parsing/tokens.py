# from ...exceptions import ParsingError, LexingError
# from dataclasses import dataclass


# class TokenStream:
#     def __init__(self, text):
#         # self.tokens = tokenize(text)
#         self.index = 0

#     def read(self, id):
#         token = self.peek()
#         if self.has(id):
#             self.index += 1
#             return token
#         msg = f'Expected token "{id}" but found "{token.id}"'
#         raise LexingError(msg)

#     def has(self, id):
#         return self.peek().id == id

#     def peek(self):
#         try:
#             return self.tokens[self.index]
#         except IndexError:
#             return Token('eof', '\0')

#     def __getitem__(self, index):
#         return self.tokens[index]

#     def __len__(self):
#         return len(self.tokens)


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


# @dataclass
# class Token:
#     id: int
#     text: str


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


# class TokenSpecItem:
#     def __init__(self, id, pattern, skip, hints):
#         self.id = id
#         self.pattern = pattern
#         self.skip = skip
#         self.hints = hints


# class TokenSpec:
#     '''
#     FIXME: Currently supports only one token per hint
#     '''

#     def __init__(self, spec_data):
#         self.map = self._build(spec_data)
#         self.spec = spec_data

#     def _build(self, spec_data):
#         hint_map = {}

#         def _build_symbols():
#             for sym in spec_data['symbols']:
#                 item = TokenSpecItem(sym, pattern=sym, skip=False, hints=sym)
#                 hint_map[sym] = item

#         def _build_hints(index, id, hints):
#             for symbol in spec_data['symbols']:
#                 hint_map[symbol] = index

#         for index, (id, _, _, hints) in enumerate(spec_data):
#             _build_hints(index, id, hints)
#         return hint_map

#     def get(self, hint):
#         try:
#             index = self.map[hint]
#         except KeyError:
#             raise LexingError(f'Unrecognized hint: "{hint}"')
#         return self.spec[index]
