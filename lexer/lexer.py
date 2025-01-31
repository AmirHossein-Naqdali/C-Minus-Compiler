from errorHandler import report_lexical_error
from .constants import *
from .state import *
from symbolTable import SymbolTable


class Token:
    def __init__(self, value, token_type, line_number):
        self.lexeme = value
        self.type = token_type
        self.line_number = line_number


class Lexer:
    def __init__(self, text, symbol_table: SymbolTable):
        self.text = text
        self.line_number = 1
        self.tokens = []
        self.symbol_table = symbol_table

    def __get_next_state(self, current_state, char):
        transition_type = TransitionTypes.get_transition_type(char)
        return current_state.read(transition_type)

    def get_next_token(self):
        token_value = ''
        index = 0
        state = States.Q0.value

        while True:
            if index >= len(self.text):
                if state in [States.Q6.value, States.Q7.value]:
                    report_lexical_error(self.line_number, token_value, ErrorMessages.UNCLOSED_COMMENT.value)
                break

            char = self.text[index]
            state = self.__get_next_state(state, char)

            if state.error_message:
                token_value = token_value + char
                report_lexical_error(self.line_number, token_value, state.error_message)

                token_value = ''
                index += 1
                state = States.Q0.value
            elif state.is_finished:
                if not state.does_need_reversion:
                    index += 1
                    token_value = token_value + char
                break
            elif state.does_reset:
                token_value = ''
                state = States.Q0.value
                index += 1
                if char == '\n':
                    self.line_number += 1
            else:
                token_value = token_value + char
                index += 1

        token_type = state.token_type
        if token_type and token_type == TokenTypes.ID_KEY.value:
            if token_value in keywords:
                token_type = TokenTypes.KEY.value
            else:
                token_type = TokenTypes.ID.value

        if not token_type or not token_value:
            # token_type = token_value = None
            token_type = 'END'
            token_value = '$'

        token = Token(token_value, token_type, self.line_number)

        self.text = self.text[index:]
        # add_to_symbol_table(token.type, token.lexeme)
        self.symbol_table.add_to_symbol_table(token.type, token.lexeme)
        self.tokens.append(token)

        # return Token(token_value, token_type, self.line_number)
        return token
