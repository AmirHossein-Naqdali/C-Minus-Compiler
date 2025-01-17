from .constants import keywords

symbol_table = list(keywords)


def update_symbol_table(token_type, token_string):
    if token_type == 'ID' and token_string not in symbol_table:
        symbol_table.append(token_string)
