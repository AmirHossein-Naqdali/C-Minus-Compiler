from action_symbols import ActionSymbols
from .nonterminals import NonTerminals
from .terminals import Terminals

start_symbol = NonTerminals.PROGRAM

productions = {
    NonTerminals.PROGRAM: [
        [NonTerminals.DECLARATION_LIST, ActionSymbols.END_OF_PROGRAM]],
    NonTerminals.DECLARATION_LIST: [
        [NonTerminals.DECLARATION, NonTerminals.DECLARATION_LIST],
        [Terminals.EPSILON]],
    NonTerminals.DECLARATION: [
        [NonTerminals.DECLARATION_INITIAL, NonTerminals.DECLARATION_PRIME]],
    NonTerminals.DECLARATION_INITIAL: [
        [ActionSymbols.SET_DECLARING, ActionSymbols.PUSH, NonTerminals.TYPE_SPECIFIER, ActionSymbols.UPDATE_TYPE,
         Terminals.ID]],
    NonTerminals.DECLARATION_PRIME: [
        [NonTerminals.FUN_DECLARATION_PRIME],
        [NonTerminals.VAR_DECLARATION_PRIME]],
    NonTerminals.VAR_DECLARATION_PRIME: [
        [ActionSymbols.UPDATE_VAR_ATTRIBUTES, Terminals.SEMICOLON],
        [Terminals.BRACKET_OPEN, ActionSymbols.UPDATE_ARR_ATTRIBUTES, Terminals.NUM, Terminals.BRACKET_CLOSE,
         Terminals.SEMICOLON]],
    NonTerminals.FUN_DECLARATION_PRIME: [
        [ActionSymbols.START_SCOPE, Terminals.PARENTHESIS_OPEN, NonTerminals.PARAMS, Terminals.PARENTHESIS_CLOSE,
         ActionSymbols.UPDATE_FUNC_ATTRIBUTES, NonTerminals.COMPOUND_STMT, ActionSymbols.RETURN_AT_THE_END_OF_FUNCTION,
         ActionSymbols.END_SCOPE]],
    NonTerminals.TYPE_SPECIFIER: [
        [Terminals.INT],
        [Terminals.VOID]],
    NonTerminals.PARAMS: [
        [ActionSymbols.SET_DECLARING, ActionSymbols.PUSH, Terminals.INT, ActionSymbols.UPDATE_TYPE, Terminals.ID,
         NonTerminals.PARAM_PRIME, NonTerminals.PARAM_LIST],
        [Terminals.VOID]],
    NonTerminals.PARAM_LIST: [
        [Terminals.COMMA, NonTerminals.PARAM, NonTerminals.PARAM_LIST],
        [Terminals.EPSILON]],
    NonTerminals.PARAM: [
        [NonTerminals.DECLARATION_INITIAL, NonTerminals.PARAM_PRIME]],
    NonTerminals.PARAM_PRIME: [
        [ActionSymbols.UPDATE_ARR_ATTRIBUTES, Terminals.BRACKET_OPEN, Terminals.BRACKET_CLOSE],
        [ActionSymbols.UPDATE_VAR_ATTRIBUTES, Terminals.EPSILON]],
    NonTerminals.COMPOUND_STMT: [
        [Terminals.BRACE_OPEN, NonTerminals.DECLARATION_LIST, NonTerminals.STATEMENT_LIST, Terminals.BRACE_CLOSE]],
    NonTerminals.STATEMENT_LIST: [
        [NonTerminals.STATEMENT, NonTerminals.STATEMENT_LIST],
        [Terminals.EPSILON]],
    NonTerminals.STATEMENT: [
        [NonTerminals.EXPRESSION_STMT],
        [NonTerminals.COMPOUND_STMT],
        [NonTerminals.SELECTION_STMT],
        [NonTerminals.ITERATION_STMT],
        [NonTerminals.RETURN_STMT]],
    NonTerminals.EXPRESSION_STMT: [
        [NonTerminals.EXPRESSION, ActionSymbols.POP, Terminals.SEMICOLON],
        [Terminals.BREAK, ActionSymbols.BREAK, Terminals.SEMICOLON],
        [Terminals.SEMICOLON]],
    NonTerminals.SELECTION_STMT: [
        [Terminals.IF, Terminals.PARENTHESIS_OPEN, NonTerminals.EXPRESSION, Terminals.PARENTHESIS_CLOSE,
         ActionSymbols.SAVE, NonTerminals.STATEMENT, NonTerminals.ELSE_STMT]],
    NonTerminals.ELSE_STMT: [
        [ActionSymbols.JPF, Terminals.ENDIF],
        [Terminals.ELSE, ActionSymbols.JPF_SAVE, NonTerminals.STATEMENT, ActionSymbols.JP, Terminals.ENDIF]],
    NonTerminals.ITERATION_STMT: [
        [Terminals.WHILE, ActionSymbols.SAVE, ActionSymbols.LABEL, Terminals.PARENTHESIS_OPEN, NonTerminals.EXPRESSION,
         Terminals.PARENTHESIS_CLOSE, ActionSymbols.WHILE_SAVE, NonTerminals.STATEMENT, ActionSymbols.WHILE]],
    NonTerminals.RETURN_STMT: [
        [Terminals.RETURN, NonTerminals.RETURN_STMT_PRIME]],
    NonTerminals.RETURN_STMT_PRIME: [
        [ActionSymbols.RETURN, Terminals.SEMICOLON],
        [NonTerminals.EXPRESSION, ActionSymbols.RETURN_VALUE, Terminals.SEMICOLON]],
    NonTerminals.EXPRESSION: [
        [NonTerminals.SIMPLE_EXPRESSION_ZEGOND],
        [ActionSymbols.PUSH_ID, Terminals.ID, NonTerminals.B]],
    NonTerminals.B: [
        [Terminals.ASSIGN, NonTerminals.EXPRESSION, ActionSymbols.ASSIGN],
        [Terminals.BRACKET_OPEN, NonTerminals.EXPRESSION, Terminals.BRACKET_CLOSE, ActionSymbols.UPDATE_ID,
         NonTerminals.H],
        [NonTerminals.SIMPLE_EXPRESSION_PRIME]],
    NonTerminals.H: [
        [Terminals.ASSIGN, NonTerminals.EXPRESSION, ActionSymbols.ASSIGN],
        [NonTerminals.G, NonTerminals.D, NonTerminals.C]],
    NonTerminals.SIMPLE_EXPRESSION_ZEGOND: [
        [NonTerminals.ADDITIVE_EXPRESSION_ZEGOND, NonTerminals.C]],
    NonTerminals.SIMPLE_EXPRESSION_PRIME: [
        [NonTerminals.ADDITIVE_EXPRESSION_PRIME, NonTerminals.C]],
    NonTerminals.C: [
        [ActionSymbols.PUSH, NonTerminals.RELOP, NonTerminals.ADDITIVE_EXPRESSION, ActionSymbols.OPERATION],
        [Terminals.EPSILON]],
    NonTerminals.RELOP: [
        [Terminals.LESS_THAN],
        [Terminals.EQUAL]],
    NonTerminals.ADDITIVE_EXPRESSION: [
        [NonTerminals.TERM, NonTerminals.D]],
    NonTerminals.ADDITIVE_EXPRESSION_PRIME: [
        [NonTerminals.TERM_PRIME, NonTerminals.D]],
    NonTerminals.ADDITIVE_EXPRESSION_ZEGOND: [
        [NonTerminals.TERM_ZEGOND, NonTerminals.D]],
    NonTerminals.D: [
        [ActionSymbols.PUSH, NonTerminals.ADDOP, NonTerminals.TERM, ActionSymbols.OPERATION, NonTerminals.D],
        [Terminals.EPSILON]],
    NonTerminals.ADDOP: [
        [Terminals.PLUS],
        [Terminals.MINUS]],
    NonTerminals.TERM: [
        [NonTerminals.SIGNED_FACTOR, NonTerminals.G]],
    NonTerminals.TERM_PRIME: [
        [NonTerminals.SIGNED_FACTOR_PRIME, NonTerminals.G]],
    NonTerminals.TERM_ZEGOND: [
        [NonTerminals.SIGNED_FACTOR_ZEGOND, NonTerminals.G]],
    NonTerminals.G: [
        [ActionSymbols.PUSH, NonTerminals.MULOP, NonTerminals.SIGNED_FACTOR, ActionSymbols.OPERATION, NonTerminals.G],
        [Terminals.EPSILON]],
    NonTerminals.MULOP: [
        [Terminals.STAR],
        [Terminals.SLASH]],
    NonTerminals.SIGNED_FACTOR: [
        [Terminals.PLUS, NonTerminals.FACTOR],
        [Terminals.MINUS, NonTerminals.FACTOR, ActionSymbols.NEG],
        [NonTerminals.FACTOR]],
    NonTerminals.SIGNED_FACTOR_PRIME: [
        [NonTerminals.FACTOR_PRIME]],
    NonTerminals.SIGNED_FACTOR_ZEGOND: [
        [Terminals.PLUS, NonTerminals.FACTOR],
        [Terminals.MINUS, NonTerminals.FACTOR, ActionSymbols.NEG],
        [NonTerminals.FACTOR_ZEGOND]],
    NonTerminals.FACTOR: [
        [Terminals.PARENTHESIS_OPEN, NonTerminals.EXPRESSION, Terminals.PARENTHESIS_CLOSE],
        [ActionSymbols.PUSH_ID, Terminals.ID, NonTerminals.VAR_CALL_PRIME],
        [ActionSymbols.SAVE_NUM, Terminals.NUM]],
    NonTerminals.VAR_CALL_PRIME: [
        [Terminals.PARENTHESIS_OPEN, NonTerminals.ARGS, Terminals.PARENTHESIS_CLOSE, ActionSymbols.CALL],
        [NonTerminals.VAR_PRIME]],
    NonTerminals.VAR_PRIME: [
        [Terminals.BRACKET_OPEN, NonTerminals.EXPRESSION, ActionSymbols.UPDATE_ID, Terminals.BRACKET_CLOSE],
        [Terminals.EPSILON]],
    NonTerminals.FACTOR_PRIME: [
        [Terminals.PARENTHESIS_OPEN, NonTerminals.ARGS, Terminals.PARENTHESIS_CLOSE, ActionSymbols.CALL],
        [Terminals.EPSILON]],
    NonTerminals.FACTOR_ZEGOND: [
        [Terminals.PARENTHESIS_OPEN, NonTerminals.EXPRESSION, Terminals.PARENTHESIS_CLOSE],
        [ActionSymbols.SAVE_NUM, Terminals.NUM]],
    NonTerminals.ARGS: [
        [ActionSymbols.PUSH_ZERO, NonTerminals.ARG_LIST],
        [Terminals.EPSILON]],
    NonTerminals.ARG_LIST: [
        [NonTerminals.EXPRESSION, ActionSymbols.NEW_ARG, NonTerminals.ARG_LIST_PRIME]],
    NonTerminals.ARG_LIST_PRIME: [
        [Terminals.COMMA, NonTerminals.EXPRESSION, ActionSymbols.NEW_ARG, NonTerminals.ARG_LIST_PRIME],
        [ActionSymbols.POP, Terminals.EPSILON]]}


def first(statement):
    first_set = set()
    for i, state in enumerate(statement):
        if type(state) is ActionSymbols:
            continue
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
