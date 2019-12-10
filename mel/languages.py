'''
mel = Grammar('Mel')

@mel.rule("object", " '(' key expression* ')' ")
def parse_rule(id, node):
    return Node(node)


@mel.rule("int", "/-?[d]+/")
def parse_int(id, node):
    return Node(node)


'''
