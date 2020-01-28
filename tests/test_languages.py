from mel.parsing import Grammar, ZeroMany, Str  # , Seq, OneMany, Rule, Regex,

# TODO: need build the entire grammar tree to "unparse" example from it


def test_base_rule():
    g = Grammar()
    g.set('root', ZeroMany(Str('a')))
    # g.set('rule', Seq(
    #     Rule('name'), Str('='), Rule('alternative')
    # ))
    # g.set('alternative', Seq(
    #     Rule('sequence'),
    #     ZeroMany(Str('|'), Rule('sequence'))
    # ))
    # g.set('sequence', OneMany(Rule('name')))
    # g.set('name', Regex(r'[a-z]+'))

    # g.skip('space', r'[ \t]+')
    # g.skip('comment', r'--[^\n\r]*')

    node = g.parse('aa')

    assert node
