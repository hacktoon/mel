from infiniscribe.parsing import Language


# HELPER FUNCTIONS ==================================

def create_base_lang():
    lang = Language('foo')

    @lang.start(lambda stream: 'start')
    def parse_start(parsed):
        return f'{parsed} node'

    return lang


# TESTS ==================================

def test_line_comment():
    lang = create_base_lang()
    assert lang.parse('') == 'start node'
