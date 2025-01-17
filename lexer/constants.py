from enum import Enum

digits = [chr(i) for i in range(48, 58)]
letters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
symbols = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<']
whitespace = [' ', '\n', '\r', '\t', '\v', '\f']
keywords = ['if', 'else', 'void', 'int', 'while', 'break', 'return', 'endif']


class TokenTypes(Enum):
    NUM = 'NUM'
    ID_KEY = 'ID_KEYWORD'
    ID = 'ID'
    KEY = 'KEYWORD'
    SYMBOL = 'SYMBOL'


class TransitionTypes(Enum):
    DIGIT = digits
    LETTER = letters
    SYMBOL = symbols
    WHITESPACE = whitespace
    NEWLINE = ['\n']
    SLASH = ['/']
    EQUAL = ['=']
    STAR = ['*']
    INVALID = []

    @classmethod
    def get_transition_type(cls, character: chr):
        transition_type = None
        for tr_type in TransitionTypes:
            if character in tr_type.value:
                transition_type = tr_type
        if not transition_type:
            transition_type = TransitionTypes.INVALID
        return transition_type


class ErrorMessages(Enum):
    INVALID_INPUT = 'Invalid input'
    INVALID_NUMBER = 'Invalid number'
    UNMATCHED_COMMENT = 'Unmatched comment'
    UNCLOSED_COMMENT = 'Unclosed comment'
