from mel.parsing import Grammar, ZeroMany, Seq, OneMany, Rule

# TODO: need build the entire grammar tree to "unparse" example from it


def test_base_rule():
    g = Grammar()
    g.set('root', ZeroMany(Rule('rule')))
    g.set('rule', Seq(
        Rule('name'), g.s('='), Rule('alternative')
    ))
    g.set('alternative', Seq(
        Rule('sequence'),
        ZeroMany(g.s('|'), Rule('sequence'))
    ))
    g.set('sequence', OneMany(Rule('name')))
    g.set('name', g.p(r'[a-z]+'))

    g.skip('space', r'[ \t]+')
    g.skip('comment', r'--[^\n\r]*')

    # node = g.parse('address = end|start about')

    assert g
