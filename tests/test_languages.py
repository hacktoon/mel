from mel.parsing import Grammar, ZeroMany, Seq, OneMany

# TODO: need build the entire grammar tree to "unparse" example from it


def test_base_rule():
    g = Grammar()
    g.set('root', ZeroMany(g.r('rule')))
    g.set('rule', Seq(
        g.r('name'), g.s('='), g.r('alternative')
    ))
    g.set('alternative', Seq(
        g.r('sequence'),
        ZeroMany(g.s('|'), g.r('sequence'))
    ))
    g.set('sequence', OneMany(g.r('name')))
    g.set('name', g.p(r'[a-z]+'))

    g.skip('space', r'[ \t]+')
    g.skip('comment', r'--[^\n\r]*')

    # node = g.parse('address = end|start about')

    assert g
