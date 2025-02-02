from action_symbols import ActionSymbols, CheckSymbols
from lexer.lexer import Token
from symbolTable import SymbolTable
from errorHandler import report_semantic_error


class CodeGenerator:
    def __init__(self, symbol_table: SymbolTable):
        self.semantic_stack = []
        self.program_block = ['']
        self.symbol_table = symbol_table
        self.temp_address = 508
        self.jump_stack = []
        self.call_stack = []
        self.is_declaring_parameters = True
        self.is_erroneous = False
        self.type_stack = []

    def print_pb(self):
        for i, command in enumerate(self.program_block):
            print(f'{i}\t{command}')

    def get_temp(self):
        address = self.temp_address
        self.temp_address += 4
        return address

    def semantic_stack_pop(self, num: int = 1):
        for _ in range(num):
            self.semantic_stack.pop()

    def is_function_output(self, stack_index, pb_index=None):
        if self.semantic_stack[stack_index] != '@1000':
            return False
        else:
            new_address = self.get_temp()
            if not pb_index:
                self.program_block.append(f'(ASSIGN, @1000, {new_address}, )')
                self.program_block.append(f'(SUB, 1000, #4, 1000)')
            else:
                self.program_block.insert(pb_index, f'(ASSIGN, @1000, {new_address}, )')
                self.program_block.insert(pb_index + 1, f'(SUB, 1000, #4, 1000)')
            self.semantic_stack[stack_index] = new_address
            return True

    def semantic_check(self, check_symbol: CheckSymbols, current_token: Token):
        if check_symbol == CheckSymbols.ID_IS_DEFINED:
            symbol = self.symbol_table.find_symbol_by_lexeme(current_token.lexeme)
            if symbol is None and current_token.lexeme != 'output':
                report_semantic_error(current_token.line_number, f'\'{current_token.lexeme}\' is not defined.')
                self.semantic_stack.append(0)
                self.type_stack.append('int')
                self.is_erroneous = True
        elif check_symbol == CheckSymbols.VAR_ARR_IS_INT:
            symbol = self.symbol_table.get_last_symbol()
            if not symbol.is_function and symbol.type == 'void':
                report_semantic_error(current_token.line_number, f'Illegal type of void for \'{symbol.lexeme}\'.')
                self.is_erroneous = True
        elif check_symbol == CheckSymbols.PARAMETER_NUMBER:
            caller = self.call_stack[-1]
            number_pushed_args = self.semantic_stack[-1]
            if (caller == 'output' and number_pushed_args == 1) or \
                    (caller != 'output' and number_pushed_args == len(caller.parameters)):
                report_semantic_error(current_token.line_number,
                                      f'Mismatch in numbers of arguments of \'{caller.lexeme}\'.')
                self.is_erroneous = True
        elif check_symbol == CheckSymbols.BREAK_IS_IN_LOOP:
            if not self.jump_stack:
                report_semantic_error(current_token.line_number, f'No \'while\' found for \'break\'.')
                self.is_erroneous = True
        elif check_symbol == CheckSymbols.TYPE_MATCH:
            if self.type_stack[-1] != self.type_stack[-2]:
                report_semantic_error(
                    current_token.line_number,
                    f'Type mismatch in operands, Got {self.type_stack[-2]} instead of {self.type_stack[-1]}.')
                self.is_erroneous = True
        elif check_symbol == CheckSymbols.ARG_TYPE:
            index = self.semantic_stack[-2]
            caller = self.call_stack[-1]
            if caller == 'output':
                parameter_type = 'int'
            else:
                if index >= len(caller.parameters):
                    self.type_stack.pop()
                    return
                parameter_address = caller.parameters[index]
                parameter_symbol = self.symbol_table.find_symbol_by_address(parameter_address)
                parameter_type = 'array' if parameter_symbol.is_array else parameter_symbol.type
            arg_type = self.type_stack.pop()
            if parameter_type != arg_type:
                report_semantic_error(
                    current_token.line_number,
                    f'Mismatch in type of argument {index + 1} of \'{caller.lexeme}\'. Expected \'{parameter_type}\' but got \'{arg_type}\' instead.')
                self.is_erroneous = True

    def code_gen(self, action_symbol: ActionSymbols, current_token: Token):
        if action_symbol == ActionSymbols.SET_DECLARING:
            self.symbol_table.is_declaring = True
        elif action_symbol == ActionSymbols.PUSH:
            self.semantic_stack.append(current_token.lexeme)
        elif action_symbol == ActionSymbols.UPDATE_TYPE:
            saved_type = self.semantic_stack.pop()
            self.symbol_table.update_type(saved_type)
        elif action_symbol == ActionSymbols.UPDATE_VAR_ATTRIBUTES:
            symbol = self.symbol_table.update_last_symbol()
            if self.call_stack:
                self.call_stack[-1].size += 1
            if not self.is_declaring_parameters:
                self.program_block.append(f'(ASSIGN, #0, {symbol.address}, )')
        elif action_symbol == ActionSymbols.UPDATE_ARR_ATTRIBUTES:
            size = int(current_token.lexeme) if current_token.type == 'NUM' else 0
            symbol = self.symbol_table.update_last_symbol(is_array=True, size=size)
            if self.call_stack:
                self.call_stack[-1].size += symbol.size
            if not self.is_declaring_parameters:
                address = symbol.address
                for _ in range(symbol.size):
                    self.program_block.append(f'(ASSIGN, #0, {address}, )')
                    address += 4
        elif action_symbol == ActionSymbols.START_SCOPE:
            self.symbol_table.add_scope()
        elif action_symbol == ActionSymbols.START_FUNCTION:
            self.symbol_table.add_scope()
            self.is_declaring_parameters = True
        elif action_symbol == ActionSymbols.END_SCOPE:
            self.symbol_table.del_scope()
        elif action_symbol == ActionSymbols.UPDATE_FUNC_ATTRIBUTES:
            self.is_declaring_parameters = False
            function_symbol = self.symbol_table.update_last_function()
            function_symbol.code_beginning = len(self.program_block)
            self.call_stack.append(function_symbol)
            if function_symbol.lexeme == 'main':
                self.program_block.append(f'(ASSIGN, #1000, 1000, )')
                for addr in range(100, self.symbol_table.last_used_address() + 4, 4):
                    self.program_block.append(f'(ASSIGN, #0, {addr}, )')
                self.semantic_stack.append(len(self.program_block))
                function_symbol.code_beginning = len(self.program_block)
                self.program_block.append('')
        elif action_symbol == ActionSymbols.LABEL:
            self.semantic_stack.append(len(self.program_block))
        elif action_symbol == ActionSymbols.SAVE:
            self.semantic_stack.append(len(self.program_block))
            self.program_block.append('')
        elif action_symbol == ActionSymbols.WHILE_SAVE:
            self.is_function_output(-1)
            temp_addr = self.get_temp()
            self.jump_stack.append(temp_addr)
            self.program_block.append(f'(JPF, {self.semantic_stack[-1]}, @{temp_addr},)')
            self.semantic_stack_pop(1)
        elif action_symbol == ActionSymbols.WHILE:
            index = len(self.program_block)
            self.program_block[self.semantic_stack[-2]] = f'(ASSIGN, #{index + 1}, {self.jump_stack[-1]},)'
            self.program_block.append(f'(JP, {self.semantic_stack[-1]}, ,)')
            self.jump_stack.pop()
            self.semantic_stack_pop(2)
        elif action_symbol == ActionSymbols.JPF_SAVE:
            index = len(self.program_block)
            if self.is_function_output(-2, self.semantic_stack[-1]):
                self.program_block[self.semantic_stack[-1] + 2] = f'(JPF, {self.semantic_stack[-2]}, {index + 3},)'
            else:
                self.program_block[self.semantic_stack[-1]] = f'(JPF, {self.semantic_stack[-2]}, {index + 1},)'
            self.semantic_stack_pop(2)
            self.semantic_stack.append(len(self.program_block))
            self.program_block.append('')
        elif action_symbol == ActionSymbols.JP:
            index = len(self.program_block)
            self.program_block[self.semantic_stack[-1]] = f'(JP, {index}, ,)'
            self.semantic_stack_pop(1)
        elif action_symbol == ActionSymbols.JPF:
            index = len(self.program_block)
            if self.is_function_output(-2, self.semantic_stack[-1]):
                self.program_block[self.semantic_stack[-1] + 2] = f'(JPF, {self.semantic_stack[-2]}, {index + 2},)'
            else:
                self.program_block[self.semantic_stack[-1]] = f'(JPF, {self.semantic_stack[-2]}, {index},)'
            self.semantic_stack_pop(2)
        elif action_symbol == ActionSymbols.PUSH_ID:
            symbol = self.symbol_table.find_symbol_by_lexeme(current_token.lexeme)
            if not symbol:
                if current_token.lexeme == 'output':
                    self.call_stack.append('output')
                    self.type_stack.append('void')
            elif symbol.is_function:
                self.call_stack.append(symbol)
                addr = symbol.first_address
                for _ in range(symbol.size):
                    self.program_block.append(f'(ADD, 1000, #4, 1000)')
                    self.program_block.append(f'(ASSIGN, {addr}, @1000, )')
                    addr += 4
                self.program_block.append(f'(ADD, 1000, #4, 1000)')
                self.program_block.append(f'(ASSIGN, 500, @1000, )')

                for item in reversed(self.semantic_stack):
                    if type(item) is int and item >= 500:
                        self.program_block.append(f'(ADD, 1000, #4, 1000)')
                        self.program_block.append(f'(ASSIGN, {item}, @1000, )')
                    if type(item) is str and item[0] == '@' and int(item[1:]) >= 500:
                        self.program_block.append(f'(ADD, 1000, #4, 1000)')
                        self.program_block.append(f'(ASSIGN, {item[1:]}, @1000, )')
                self.type_stack.append(symbol.type)
            else:
                self.semantic_stack.append(symbol.address)
                if symbol.is_array:
                    self.type_stack.append('array')
                else:
                    self.type_stack.append(symbol.type)
        elif action_symbol == ActionSymbols.ASSIGN:
            self.is_function_output(-2)
            self.is_function_output(-1)
            self.program_block.append(f'(ASSIGN, {self.semantic_stack[-1]}, {self.semantic_stack[-2]}, )')
            self.semantic_stack.pop(-2)
            self.type_stack.pop()
        elif action_symbol == ActionSymbols.POP:
            if self.semantic_stack[-1] == '@1000':
                self.program_block.append(f'(SUB, 1000, #4, 1000)')

            self.semantic_stack_pop()
        elif action_symbol == ActionSymbols.UPDATE_ID:
            temp_addr = self.get_temp()
            self.program_block.append(f'(MULT, {self.semantic_stack[-1]}, #4, {temp_addr})')
            if self.semantic_stack[-2] in self.call_stack[0].parameters:
                self.program_block.append(f'(ADD, {self.semantic_stack[-2]}, {temp_addr}, {temp_addr})')
            else:
                self.program_block.append(f'(ADD, #{self.semantic_stack[-2]}, {temp_addr}, {temp_addr})')
            self.semantic_stack_pop(2)
            self.semantic_stack.append(f'@{temp_addr}')
            self.type_stack.pop()
            self.type_stack.pop()
            self.type_stack.append('int')
        elif action_symbol == ActionSymbols.OPERATION:
            operator = self.semantic_stack.pop(-2)
            command = {'*': 'MULT', '/': 'DIV', '+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}[operator]
            self.is_function_output(-1)
            self.is_function_output(-2)
            temp_addr = self.get_temp()
            self.program_block.append(f'({command}, {self.semantic_stack[-2]}, {self.semantic_stack[-1]}, {temp_addr})')
            self.semantic_stack_pop(2)
            self.semantic_stack.append(temp_addr)
            self.type_stack.pop()
        elif action_symbol == ActionSymbols.NEG:
            self.is_function_output(-1)
            self.program_block.append(f'(MULT, {self.semantic_stack[-1]}, #-1, {self.semantic_stack[-1]})')
        elif action_symbol == ActionSymbols.SAVE_NUM:
            self.semantic_stack.append(f'#{current_token.lexeme}')
            self.type_stack.append('int')
        elif action_symbol == ActionSymbols.BREAK:
            if self.jump_stack:
                self.program_block.append(f'(JP, @{self.jump_stack[-1]}, , )')
        elif action_symbol == ActionSymbols.PUSH_ZERO:
            self.semantic_stack.append(0)
        elif action_symbol == ActionSymbols.NEW_ARG:
            if self.call_stack[-1] == 'output':
                self.semantic_stack.pop(-2)
                self.semantic_stack.append(0)
            else:
                parameter_value = self.semantic_stack.pop()
                parameter_index = self.semantic_stack.pop()
                if parameter_index < len(self.call_stack[-1].parameters):
                    parameter_address = self.call_stack[-1].parameters[parameter_index]
                    if self.symbol_table.find_symbol_by_address(parameter_address).is_array:
                        if self.symbol_table.find_symbol_by_address(parameter_value) \
                                and self.symbol_table.find_symbol_by_address(parameter_value).is_array \
                                and parameter_value in self.call_stack[-1].parameters:
                            self.program_block.append(f'(ASSIGN, {parameter_value}, {parameter_address}, )')
                        else:
                            self.program_block.append(f'(ASSIGN, #{parameter_value}, {parameter_address}, )')
                    else:
                        self.program_block.append(f'(ASSIGN, {parameter_value}, {parameter_address}, )')
                self.semantic_stack.append(parameter_index + 1)
        elif action_symbol == ActionSymbols.CALL:
            caller = self.call_stack.pop()
            if caller == 'output':
                value = self.semantic_stack.pop()
                self.program_block.append(f'(PRINT, {value}, , )')
                self.semantic_stack.append(0)
            else:
                index = len(self.program_block)
                self.program_block.append(f'(ASSIGN, #{index + 2}, 500, )')
                self.program_block.append(f'(JP, {caller.code_beginning}, , )')

                for item in self.semantic_stack:
                    if type(item) is int and item >= 500:
                        self.program_block.append(f'(ASSIGN, @1000, {item}, )')
                        self.program_block.append(f'(SUB, 1000, #4, 1000)')
                    if type(item) is str and item[0] == '@' and int(item[1:]) >= 500:
                        self.program_block.append(f'(ASSIGN, @1000, {item[1:]}, )')
                        self.program_block.append(f'(SUB, 1000, #4, 1000)')

                self.program_block.append(f'(ASSIGN, @1000, 500, )')
                self.program_block.append(f'(SUB, 1000, #4, 1000)')
                last_address = caller.first_address + (caller.size - 1) * 4
                addr = last_address
                for _ in range(caller.size):
                    self.program_block.append(f'(ASSIGN, @1000, {addr}, )')
                    self.program_block.append(f'(SUB, 1000, #4, 1000)')
                    addr -= 4
                self.program_block.append(f'(ADD, 1000, #4, 1000)')
                self.program_block.append(f'(ASSIGN, 504, @1000, )')
                self.semantic_stack.append('@1000')
        elif action_symbol == ActionSymbols.RETURN_AT_THE_END_OF_FUNCTION:
            symbol = self.call_stack.pop()
            self.program_block.append(f'(ASSIGN, #0, 504, )')
            self.program_block.append(f'(JP, @500, , )')
            if symbol.lexeme == 'main':
                number_of_initialized_parameters = int((symbol.first_address - 100) / 4) + 1
                self.program_block[0] = f'(JP, {symbol.code_beginning - number_of_initialized_parameters}, , )'
        elif action_symbol == ActionSymbols.END_OF_PROGRAM:
            address = self.semantic_stack.pop()
            index = len(self.program_block)
            self.program_block[address] = f'(ASSIGN, #{index}, 500, )'
        elif action_symbol == ActionSymbols.RETURN:
            self.program_block.append(f'(ASSIGN, #0, 504, )')
            self.program_block.append(f'(JP, @500, , )')
        elif action_symbol == ActionSymbols.RETURN_VALUE:
            value = self.semantic_stack.pop()
            self.program_block.append(f'(ASSIGN, {value}, 504, )')
            self.program_block.append(f'(JP, @500, , )')
        elif action_symbol == ActionSymbols.TYPE_POP:
            self.type_stack.pop()
