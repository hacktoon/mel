import dale


def test_html_tag_evaluator():
    @dale.evaluator('expression')
    def eval_expression(exp, context):
        tag_tpl = '<{0}{1}>{2}</{0}>'
        attr_tpl = ' {}="{}"'
        attrs_pairs = exp['attrs'].items()
        attrs = ''
        if len(attrs_pairs):
            attrs = [attr_tpl.format(k, v) for k, v in attrs_pairs]
            attrs = ' ' + ''.join(attrs)
        return tag_tpl.format(exp['id'], attrs, ' '.join(exp['values']))

    output = dale.eval('(x "foo")')
    assert output == '<x>foo</x>'
