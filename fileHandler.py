from anytree import RenderTree


def read_code(address):
    with open(address) as file:
        input_text = file.read()
    return input_text


def write_tokens(tokens):
    text = ''
    current_line = 0
    for token in tokens:
        if token.line_number > current_line:
            if current_line > 0:
                text += '\n'
            current_line = token.line_number
            text += str(token.line_number) + '.\t'
        text += '(' + token.type + ', ' + token.lexeme + ') '
    text += '\n'

    with open('tokens.txt', 'w') as file:
        file.write(text)


def write_lexical_errors(errors):
    text = ''
    for k in sorted(errors.keys()):
        text = text + str(k) + '.\t'
        for v in errors[k]:
            text = text + '(' + v[0] + ', ' + v[1] + ') '
        text = text + '\n'
    if not text:
        text = 'There is no lexical error.\n'

    with open('lexical_errors.txt', 'w') as file:
        file.write(text)


def write_syntax_errors(errors):
    text = ''
    for k in sorted(errors.keys()):
        for v in errors[k]:
            text = text + f'#{k} : syntax error, {v}\n'
    if not text:
        text = 'There is no syntax error.\n'

    with open('syntax_errors.txt', 'w') as file:
        file.write(text)


def write_symbol_table(table):
    text = ''
    for i, record in enumerate(table, start=1):
        text = text + str(i) + '.\t'
        text = text + record + '\n'

    with open('symbol_table.txt', 'w') as file:
        file.write(text)


def write_parse_tree(root_node):
    text = ''
    for pre, fill, node in RenderTree(root_node):
        text = text + '%s%s' % (pre, node.name) + '\n'

    with open('parse_tree.txt', 'w', encoding='utf-8') as file:
        file.write(text)
