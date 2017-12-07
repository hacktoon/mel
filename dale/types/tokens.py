rules = [
    {
        'id': '.',
        'regex': r'\.'
    },
    {
        'id': '@',
        'regex': '@'
    },
    {
        'id': ':',
        'regex': ':'
    },
    {
        'id': '(',
        'regex': r'\('
    },
    {
        'id': ')',
        'regex': r'\)'
    },
    {
        'id': '[',
        'regex': r'\['
    },
    {
        'id': ']',
        'regex': r'\]'
    },
    {
        'id': 'whitespace',
        'skip': True,
        'regex': r'[ ,\t\x0b\x0c]+'
    },
    {
        'id': 'newline',
        'skip': True,
        'regex': r'[\r\n]+'
    },
    {
        'id': 'comment',
        'skip': True,
        'regex': r'#[^\n\r]*'
    },
    {
        'id': 'boolean',
        'priority': 2,
        'regex': r'(true|false)\b'
    },
    {
        'id': 'name',
        'priority': 1,
        'regex': r'[_a-zA-Z]\w*(-[_a-zA-Z]\w*)?'
    },
    {
        'id': 'float',
        'priority': 2,
        'regex': r'[-+]?\d*\.\d+([eE][-+]?\d+)?\b'
    },
    {
        'id': 'int',
        'priority': 1,
        'regex': r'[-+]?\d+\b'
    },
    {
        'id': 'string',
        'regex': r'|'.join([r"'(?:\\'|[^'])*'", r'"(?:\\"|[^"])*"'])
    }
]