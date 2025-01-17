from enum import Enum


class Terminals(Enum):
    NUM = 'NUM'
    ID = 'ID'
    IF = 'if'
    ELSE = 'else'
    ENDIF = 'endif'
    VOID = 'void'
    INT = 'int'
    WHILE = 'while'
    BREAK = 'break'
    RETURN = 'return'
    SEMICOLON = ';'
    COLON = ':'
    COMMA = ','
    BRACKET_OPEN = '['
    BRACKET_CLOSE = ']'
    PARENTHESIS_OPEN = '('
    PARENTHESIS_CLOSE = ')'
    BRACE_OPEN = '{'
    BRACE_CLOSE = '}'
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    ASSIGN = '='
    LESS_THAN = '<'
    EQUAL = '=='
    SLASH = '/'
    EPSILON = 'epsilon'
    DOLLAR = '$'

    def __init__(self, value):
        self.content = value

    @classmethod
    def get_enum_by_content(cls, content):
        for t in Terminals:
            if t.content == content:
                return t
