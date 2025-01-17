from .nonterminals import NonTerminals
from .terminals import Terminals

start_symbol = NonTerminals.PROGRAM

productions = {NonTerminals.PROGRAM: [[NonTerminals.DECLARATION_LIST]],
               NonTerminals.DECLARATION_LIST: [[NonTerminals.DECLARATION, NonTerminals.DECLARATION_LIST],
                                               [Terminals.EPSILON]],
               NonTerminals.DECLARATION: [[NonTerminals.DECLARATION_INITIAL, NonTerminals.DECLARATION_PRIME]],
               NonTerminals.DECLARATION_INITIAL: [[NonTerminals.TYPE_SPECIFIER, Terminals.ID]],
               NonTerminals.DECLARATION_PRIME: [[NonTerminals.FUN_DECLARATION_PRIME],
                                                [NonTerminals.VAR_DECLARATION_PRIME]],
               NonTerminals.VAR_DECLARATION_PRIME: [[Terminals.SEMICOLON],
                                                    [Terminals.BRACKET_OPEN, Terminals.NUM, Terminals.BRACKET_CLOSE,
                                                     Terminals.SEMICOLON]],
               NonTerminals.FUN_DECLARATION_PRIME: [
                   [Terminals.PARENTHESIS_OPEN, NonTerminals.PARAMS, Terminals.PARENTHESIS_CLOSE,
                    NonTerminals.COMPOUND_STMT]],
               NonTerminals.TYPE_SPECIFIER: [[Terminals.INT], [Terminals.VOID]],
               NonTerminals.PARAMS: [[Terminals.INT, Terminals.ID, NonTerminals.PARAM_PRIME, NonTerminals.PARAM_LIST],
                                     [Terminals.VOID]],
               NonTerminals.PARAM_LIST: [[Terminals.COMMA, NonTerminals.PARAM, NonTerminals.PARAM_LIST],
                                         [Terminals.EPSILON]],
               NonTerminals.PARAM: [[NonTerminals.DECLARATION_INITIAL, NonTerminals.PARAM_PRIME]],
               NonTerminals.PARAM_PRIME: [[Terminals.BRACKET_OPEN, Terminals.BRACKET_CLOSE], [Terminals.EPSILON]],
               NonTerminals.COMPOUND_STMT: [
                   [Terminals.BRACE_OPEN, NonTerminals.DECLARATION_LIST, NonTerminals.STATEMENT_LIST,
                    Terminals.BRACE_CLOSE]],
               NonTerminals.STATEMENT_LIST: [[NonTerminals.STATEMENT, NonTerminals.STATEMENT_LIST],
                                             [Terminals.EPSILON]],
               NonTerminals.STATEMENT: [[NonTerminals.EXPRESSION_STMT], [NonTerminals.COMPOUND_STMT],
                                        [NonTerminals.SELECTION_STMT], [NonTerminals.ITERATION_STMT],
                                        [NonTerminals.RETURN_STMT]],
               NonTerminals.EXPRESSION_STMT: [[NonTerminals.EXPRESSION, Terminals.SEMICOLON],
                                              [Terminals.BREAK, Terminals.SEMICOLON], [Terminals.SEMICOLON]],
               NonTerminals.SELECTION_STMT: [
                   [Terminals.IF, Terminals.PARENTHESIS_OPEN, NonTerminals.EXPRESSION, Terminals.PARENTHESIS_CLOSE,
                    NonTerminals.STATEMENT, NonTerminals.ELSE_STMT]],
               NonTerminals.ELSE_STMT: [[Terminals.ENDIF], [Terminals.ELSE, NonTerminals.STATEMENT, Terminals.ENDIF]],
               NonTerminals.ITERATION_STMT: [
                   [Terminals.WHILE, Terminals.PARENTHESIS_OPEN, NonTerminals.EXPRESSION, Terminals.PARENTHESIS_CLOSE,
                    NonTerminals.STATEMENT]],
               NonTerminals.RETURN_STMT: [[Terminals.RETURN, NonTerminals.RETURN_STMT_PRIME]],
               NonTerminals.RETURN_STMT_PRIME: [[Terminals.SEMICOLON], [NonTerminals.EXPRESSION, Terminals.SEMICOLON]],
               NonTerminals.EXPRESSION: [[NonTerminals.SIMPLE_EXPRESSION_ZEGOND], [Terminals.ID, NonTerminals.B]],
               NonTerminals.B: [[Terminals.ASSIGN, NonTerminals.EXPRESSION],
                                [Terminals.BRACKET_OPEN, NonTerminals.EXPRESSION, Terminals.BRACKET_CLOSE,
                                 NonTerminals.H], [NonTerminals.SIMPLE_EXPRESSION_PRIME]],
               NonTerminals.H: [[Terminals.ASSIGN, NonTerminals.EXPRESSION],
                                [NonTerminals.G, NonTerminals.D, NonTerminals.C]],
               NonTerminals.SIMPLE_EXPRESSION_ZEGOND: [[NonTerminals.ADDITIVE_EXPRESSION_ZEGOND, NonTerminals.C]],
               NonTerminals.SIMPLE_EXPRESSION_PRIME: [[NonTerminals.ADDITIVE_EXPRESSION_PRIME, NonTerminals.C]],
               NonTerminals.C: [[NonTerminals.RELOP, NonTerminals.ADDITIVE_EXPRESSION], [Terminals.EPSILON]],
               NonTerminals.RELOP: [[Terminals.LESS_THAN], [Terminals.EQUAL]],
               NonTerminals.ADDITIVE_EXPRESSION: [[NonTerminals.TERM, NonTerminals.D]],
               NonTerminals.ADDITIVE_EXPRESSION_PRIME: [[NonTerminals.TERM_PRIME, NonTerminals.D]],
               NonTerminals.ADDITIVE_EXPRESSION_ZEGOND: [[NonTerminals.TERM_ZEGOND, NonTerminals.D]],
               NonTerminals.D: [[NonTerminals.ADDOP, NonTerminals.TERM, NonTerminals.D], [Terminals.EPSILON]],
               NonTerminals.ADDOP: [[Terminals.PLUS], [Terminals.MINUS]],
               NonTerminals.TERM: [[NonTerminals.SIGNED_FACTOR, NonTerminals.G]],
               NonTerminals.TERM_PRIME: [[NonTerminals.SIGNED_FACTOR_PRIME, NonTerminals.G]],
               NonTerminals.TERM_ZEGOND: [[NonTerminals.SIGNED_FACTOR_ZEGOND, NonTerminals.G]],
               NonTerminals.G: [[NonTerminals.MULOP, NonTerminals.SIGNED_FACTOR, NonTerminals.G], [Terminals.EPSILON]],
               NonTerminals.MULOP: [[Terminals.STAR], [Terminals.SLASH]],
               NonTerminals.SIGNED_FACTOR: [[Terminals.PLUS, NonTerminals.FACTOR],
                                            [Terminals.MINUS, NonTerminals.FACTOR], [NonTerminals.FACTOR]],
               NonTerminals.SIGNED_FACTOR_PRIME: [[NonTerminals.FACTOR_PRIME]],
               NonTerminals.SIGNED_FACTOR_ZEGOND: [[Terminals.PLUS, NonTerminals.FACTOR],
                                                   [Terminals.MINUS, NonTerminals.FACTOR],
                                                   [NonTerminals.FACTOR_ZEGOND]],
               NonTerminals.FACTOR: [[Terminals.PARENTHESIS_OPEN, NonTerminals.EXPRESSION, Terminals.PARENTHESIS_CLOSE],
                                     [Terminals.ID, NonTerminals.VAR_CALL_PRIME], [Terminals.NUM]],
               NonTerminals.VAR_CALL_PRIME: [
                   [Terminals.PARENTHESIS_OPEN, NonTerminals.ARGS, Terminals.PARENTHESIS_CLOSE],
                   [NonTerminals.VAR_PRIME]],
               NonTerminals.VAR_PRIME: [[Terminals.BRACKET_OPEN, NonTerminals.EXPRESSION, Terminals.BRACKET_CLOSE],
                                        [Terminals.EPSILON]],
               NonTerminals.FACTOR_PRIME: [[Terminals.PARENTHESIS_OPEN, NonTerminals.ARGS, Terminals.PARENTHESIS_CLOSE],
                                           [Terminals.EPSILON]],
               NonTerminals.FACTOR_ZEGOND: [
                   [Terminals.PARENTHESIS_OPEN, NonTerminals.EXPRESSION, Terminals.PARENTHESIS_CLOSE], [Terminals.NUM]],
               NonTerminals.ARGS: [[NonTerminals.ARG_LIST], [Terminals.EPSILON]],
               NonTerminals.ARG_LIST: [[NonTerminals.EXPRESSION, NonTerminals.ARG_LIST_PRIME]],
               NonTerminals.ARG_LIST_PRIME: [[Terminals.COMMA, NonTerminals.EXPRESSION, NonTerminals.ARG_LIST_PRIME],
                                             [Terminals.EPSILON]]}


def first(statement):
    first_set = set()
    for i, state in enumerate(statement):
        if type(state) is NonTerminals:
            s = set(state.first)

            if Terminals.EPSILON in s:
                if i < (len(statement) - 1):
                    s.remove(Terminals.EPSILON)
                first_set.update(s)
            else:
                first_set.update(s)
                break
        else:
            first_set.add(state)
            break
    return list(first_set)
