from enum import Enum
from types import DynamicClassAttribute

from .terminals import Terminals


class NonTerminals(Enum):
    PROGRAM = (0, [Terminals.INT, Terminals.VOID, Terminals.EPSILON],
               [Terminals.DOLLAR])
    DECLARATION_LIST = (1, [Terminals.INT, Terminals.VOID, Terminals.EPSILON],
                        [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN,
                         Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF, Terminals.WHILE,
                         Terminals.RETURN, Terminals.PLUS, Terminals.MINUS, Terminals.DOLLAR])
    DECLARATION = (2, [Terminals.INT, Terminals.VOID],
                   [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.INT,
                    Terminals.VOID, Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF,
                    Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS, Terminals.DOLLAR])
    DECLARATION_INITIAL = (3, [Terminals.INT, Terminals.VOID],
                           [Terminals.SEMICOLON, Terminals.BRACKET_OPEN, Terminals.PARENTHESIS_OPEN,
                            Terminals.PARENTHESIS_CLOSE, Terminals.COMMA])
    DECLARATION_PRIME = (4, [Terminals.SEMICOLON, Terminals.BRACKET_OPEN, Terminals.PARENTHESIS_OPEN],
                         [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.INT,
                          Terminals.VOID, Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF,
                          Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS, Terminals.DOLLAR])
    VAR_DECLARATION_PRIME = (5, [Terminals.SEMICOLON, Terminals.BRACKET_OPEN],
                             [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN,
                              Terminals.INT, Terminals.VOID, Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE,
                              Terminals.BREAK, Terminals.IF, Terminals.WHILE, Terminals.RETURN, Terminals.PLUS,
                              Terminals.MINUS, Terminals.DOLLAR])
    FUN_DECLARATION_PRIME = (6, [Terminals.PARENTHESIS_OPEN],
                             [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN,
                              Terminals.INT, Terminals.VOID, Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE,
                              Terminals.BREAK, Terminals.IF, Terminals.WHILE, Terminals.RETURN, Terminals.PLUS,
                              Terminals.MINUS, Terminals.DOLLAR])
    TYPE_SPECIFIER = (7, [Terminals.INT, Terminals.VOID],
                      [Terminals.ID])
    PARAMS = (8, [Terminals.INT, Terminals.VOID],
              [Terminals.PARENTHESIS_CLOSE])
    PARAM_LIST = (9, [Terminals.COMMA, Terminals.EPSILON],
                  [Terminals.PARENTHESIS_CLOSE])
    PARAM = (10, [Terminals.INT, Terminals.VOID],
             [Terminals.PARENTHESIS_CLOSE, Terminals.COMMA])
    PARAM_PRIME = (11, [Terminals.BRACKET_OPEN, Terminals.EPSILON],
                   [Terminals.PARENTHESIS_CLOSE, Terminals.COMMA])
    COMPOUND_STMT = (12, [Terminals.BRACE_OPEN],
                     [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.INT,
                      Terminals.VOID, Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF,
                      Terminals.ENDIF, Terminals.ELSE, Terminals.WHILE, Terminals.RETURN, Terminals.PLUS,
                      Terminals.MINUS, Terminals.DOLLAR])
    STATEMENT_LIST = (13, [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN,
                           Terminals.BRACE_OPEN, Terminals.BREAK, Terminals.IF, Terminals.WHILE, Terminals.RETURN,
                           Terminals.PLUS, Terminals.MINUS, Terminals.EPSILON],
                      [Terminals.BRACE_CLOSE])
    STATEMENT = (14,
                 [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.BRACE_OPEN,
                  Terminals.BREAK, Terminals.IF, Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS],
                 [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.BRACE_OPEN,
                  Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF, Terminals.ENDIF, Terminals.ELSE,
                  Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS])
    EXPRESSION_STMT = (15,
                       [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.BREAK,
                        Terminals.PLUS, Terminals.MINUS],
                       [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN,
                        Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF, Terminals.ENDIF,
                        Terminals.ELSE, Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS])
    SELECTION_STMT = (16, [Terminals.IF],
                      [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN,
                       Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF, Terminals.ENDIF,
                       Terminals.ELSE, Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS])
    ELSE_STMT = (17, [Terminals.ENDIF, Terminals.ELSE],
                 [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.BRACE_OPEN,
                  Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF, Terminals.ENDIF, Terminals.ELSE,
                  Terminals.WHILE,
                  Terminals.RETURN, Terminals.PLUS, Terminals.MINUS])
    ITERATION_STMT = (18, [Terminals.WHILE],
                      [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN,
                       Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF, Terminals.ENDIF,
                       Terminals.ELSE, Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS])
    RETURN_STMT = (19, [Terminals.RETURN],
                   [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.BRACE_OPEN,
                    Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF, Terminals.ENDIF, Terminals.ELSE,
                    Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS])
    RETURN_STMT_PRIME = (20,
                         [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS,
                          Terminals.MINUS],
                         [Terminals.ID, Terminals.SEMICOLON, Terminals.NUM, Terminals.PARENTHESIS_OPEN,
                          Terminals.BRACE_OPEN, Terminals.BRACE_CLOSE, Terminals.BREAK, Terminals.IF, Terminals.ENDIF,
                          Terminals.ELSE, Terminals.WHILE, Terminals.RETURN, Terminals.PLUS, Terminals.MINUS])
    EXPRESSION = (21, [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
                  [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA])
    B = (22,
         [Terminals.BRACKET_OPEN, Terminals.PARENTHESIS_OPEN, Terminals.ASSIGN, Terminals.LESS_THAN, Terminals.EQUAL,
          Terminals.PLUS, Terminals.MINUS, Terminals.STAR, Terminals.SLASH, Terminals.EPSILON],
         [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA])
    H = (23, [Terminals.ASSIGN, Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
              Terminals.SLASH, Terminals.EPSILON],
         [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA])
    SIMPLE_EXPRESSION_ZEGOND = (24, [Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
                                [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE,
                                 Terminals.COMMA])
    SIMPLE_EXPRESSION_PRIME = (25, [Terminals.PARENTHESIS_OPEN, Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS,
                                    Terminals.MINUS, Terminals.STAR, Terminals.SLASH, Terminals.EPSILON],
                               [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE,
                                Terminals.COMMA])
    C = (26, [Terminals.LESS_THAN, Terminals.EQUAL, Terminals.EPSILON],
         [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA])
    RELOP = (27, [Terminals.LESS_THAN, Terminals.EQUAL],
             [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS])
    ADDITIVE_EXPRESSION = (28,
                           [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
                           [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA])
    ADDITIVE_EXPRESSION_PRIME = (29,
                                 [Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
                                  Terminals.SLASH, Terminals.EPSILON],
                                 [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE,
                                  Terminals.COMMA, Terminals.LESS_THAN, Terminals.EQUAL])
    ADDITIVE_EXPRESSION_ZEGOND = (30, [Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
                                  [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE,
                                   Terminals.COMMA, Terminals.LESS_THAN, Terminals.EQUAL])
    D = (31, [Terminals.PLUS, Terminals.MINUS, Terminals.EPSILON],
         [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
          Terminals.LESS_THAN, Terminals.EQUAL])
    ADDOP = (32, [Terminals.PLUS, Terminals.MINUS],
             [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS])
    TERM = (33, [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
            [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
             Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS])
    TERM_PRIME = (34, [Terminals.PARENTHESIS_OPEN, Terminals.STAR, Terminals.SLASH, Terminals.EPSILON],
                  [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                   Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS])
    TERM_ZEGOND = (35, [Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
                   [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                    Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS])
    G = (36, [Terminals.STAR, Terminals.SLASH, Terminals.EPSILON],
         [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
          Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS])
    MULOP = (37, [Terminals.STAR, Terminals.SLASH],
             [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS])
    SIGNED_FACTOR = (38, [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
                     [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                      Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
                      Terminals.SLASH])
    SIGNED_FACTOR_PRIME = (39, [Terminals.PARENTHESIS_OPEN, Terminals.EPSILON],
                           [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                            Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
                            Terminals.SLASH])
    SIGNED_FACTOR_ZEGOND = (40, [Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
                            [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                             Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
                             Terminals.SLASH])
    FACTOR = (41, [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN],
              [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
               Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR, Terminals.SLASH])
    VAR_CALL_PRIME = (42, [Terminals.BRACKET_OPEN, Terminals.PARENTHESIS_OPEN, Terminals.EPSILON],
                      [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                       Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
                       Terminals.SLASH])
    VAR_PRIME = (43, [Terminals.BRACKET_OPEN, Terminals.EPSILON],
                 [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                  Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
                  Terminals.SLASH])
    FACTOR_PRIME = (44, [Terminals.PARENTHESIS_OPEN, Terminals.EPSILON],
                    [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                     Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
                     Terminals.SLASH])
    FACTOR_ZEGOND = (45, [Terminals.NUM, Terminals.PARENTHESIS_OPEN],
                     [Terminals.SEMICOLON, Terminals.BRACKET_CLOSE, Terminals.PARENTHESIS_CLOSE, Terminals.COMMA,
                      Terminals.LESS_THAN, Terminals.EQUAL, Terminals.PLUS, Terminals.MINUS, Terminals.STAR,
                      Terminals.SLASH])
    ARGS = (46,
            [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS,
             Terminals.EPSILON],
            [Terminals.PARENTHESIS_CLOSE])
    ARG_LIST = (47, [Terminals.ID, Terminals.NUM, Terminals.PARENTHESIS_OPEN, Terminals.PLUS, Terminals.MINUS],
                [Terminals.PARENTHESIS_CLOSE])
    ARG_LIST_PRIME = (48, [Terminals.COMMA, Terminals.EPSILON],
                      [Terminals.PARENTHESIS_CLOSE])

    def __init__(self, idx, first, follow):
        self.index = idx
        self.first = first
        self.follow = follow

    @DynamicClassAttribute
    def name(self):
        parts = super(NonTerminals, self).name.lower().split('_')
        return ''.join([part.capitalize() for part in parts])
