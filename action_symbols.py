from enum import Enum


class ActionSymbols(Enum):
    SET_DECLARING = 0
    PUSH = 1
    UPDATE_TYPE = 2
    UPDATE_VAR_ATTRIBUTES = 3
    UPDATE_ARR_ATTRIBUTES = 4
    UPDATE_FUNC_ATTRIBUTES = 5
    START_SCOPE = 6
    END_SCOPE = 7
    PUSH_ID = 8
    LABEL = 9
    WHILE_SAVE = 10
    WHILE = 11
    SAVE = 12
    JPF_SAVE = 13
    JP = 14
    JPF = 15
    ASSIGN = 16
    POP = 17
    UPDATE_ID = 18
    OPERATION = 19
    NEG = 23
    SAVE_NUM = 24
    BREAK = 25
    PUSH_ZERO = 26
    NEW_ARG = 27
    CALL = 28
    RETURN_AT_THE_END_OF_FUNCTION = 29
    END_OF_PROGRAM = 30
    RETURN = 31
    RETURN_VALUE = 32
    TYPE_POP = 33
    START_FUNCTION = 34


class CheckSymbols(Enum):
    ID_IS_DEFINED = 0
    VAR_ARR_IS_INT = 1
    PARAMETER_NUMBER = 2
    BREAK_IS_IN_LOOP = 3
    TYPE_MATCH = 4
    ARG_TYPE = 5
