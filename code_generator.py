from action_symbols import ActionSymbols
from lexer.lexer import Token
from symbolTable import SymbolTable


class CodeGenerator:
    def __init__(self, symbol_table: SymbolTable):
        self.semantic_stack = []
        self.program_block = ['']
        self.symbol_table = symbol_table
        self.temp_address = 508
        self.jump_stack = []
        self.call_stack = []
        self.is_declaring_parameters = True

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
            self.is_declaring_parameters = True
        elif action_symbol == ActionSymbols.END_SCOPE:
            self.symbol_table.del_scope()
        elif action_symbol == ActionSymbols.UPDATE_FUNC_ATTRIBUTES:
            self.is_declaring_parameters = False
            function_symbol = self.symbol_table.update_last_function()
            function_symbol.code_beginning = len(self.program_block)
            self.call_stack.append(function_symbol)
            if function_symbol.lexeme == 'main':
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
            self.program_block[self.semantic_stack[-1]] = f'(JPF, {self.semantic_stack[-2]}, {index},)'
            self.semantic_stack_pop(2)
        elif action_symbol == ActionSymbols.PUSH_ID:
            symbol = self.symbol_table.find_symbol(current_token.lexeme)
            if not symbol:
                self.call_stack.append('output')
            elif symbol.is_function:
                self.call_stack.append(symbol)
                addr = symbol.first_address
                for _ in range(symbol.size):
                    temp_addr = self.get_temp()
                    self.program_block.append(f'(ASSIGN, {addr}, {temp_addr}, )')
                    self.semantic_stack.append(temp_addr)
                    addr += 4
                temp_addr = self.get_temp()
                self.program_block.append(f'(ASSIGN, 500, {temp_addr}, )')
                self.semantic_stack.append(temp_addr)
            else:
                self.semantic_stack.append(symbol.address)
        elif action_symbol == ActionSymbols.ASSIGN:
            self.program_block.append(f'(ASSIGN, {self.semantic_stack[-1]}, {self.semantic_stack[-2]}, )')
            self.semantic_stack.pop(-2)
        elif action_symbol == ActionSymbols.POP:
            self.semantic_stack_pop()
        elif action_symbol == ActionSymbols.UPDATE_ID:
            temp_addr = self.get_temp()
            self.program_block.append(f'(MULT, {self.semantic_stack[-1]}, #4, {temp_addr})')
            self.program_block.append(f'(ADD, {self.semantic_stack[-2]}, {temp_addr}, {temp_addr})')
            self.semantic_stack_pop(2)
            self.semantic_stack.append(f'@{temp_addr}')
        elif action_symbol == ActionSymbols.OPERATION:
            operator = self.semantic_stack.pop(-2)
            command = {'*': 'MULT', '/': 'DIV', '+': 'ADD', '-': 'SUB', '<': 'LT', '==': 'EQ'}[operator]
            temp_addr = self.get_temp()
            self.program_block.append(f'({command}, {self.semantic_stack[-2]}, {self.semantic_stack[-1]}, {temp_addr})')
            self.semantic_stack_pop(2)
            self.semantic_stack.append(temp_addr)
        elif action_symbol == ActionSymbols.NEG:
            self.program_block.append(f'(MULT, {self.semantic_stack[-1]}, #-1, {self.semantic_stack[-1]})')
        elif action_symbol == ActionSymbols.SAVE_NUM:
            self.semantic_stack.append(f'#{current_token.lexeme}')
        elif action_symbol == ActionSymbols.BREAK:
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
                parameter_address = self.call_stack[-1].parameters[parameter_index]
                self.program_block.append(f'(ASSIGN, {parameter_value}, {parameter_address}, )')
                self.semantic_stack.append(parameter_index + 1)
        elif action_symbol == ActionSymbols.CALL:
            if self.call_stack[-1] == 'output':
                value = self.semantic_stack.pop()
                self.program_block.append(f'(PRINT, {value}, , )')
                self.semantic_stack.append(0)
            else:
                index = len(self.program_block)
                self.program_block.append(f'(ASSIGN, #{index + 2}, 500, )')
                self.program_block.append(f'(JP, {self.call_stack[-1].code_beginning}, , )')
                previous_return_address = self.semantic_stack.pop()
                self.program_block.append(f'(ASSIGN, {previous_return_address}, 500, )')
                last_address = self.call_stack[-1].first_address + (self.call_stack[-1].size - 1) * 4
                addr = last_address
                for _ in range(self.call_stack[-1].size):
                    saved_temp_addr = self.semantic_stack.pop()
                    self.program_block.append(f'(ASSIGN, {saved_temp_addr}, {addr}, )')
                    addr -= 4
                temp_addr = self.get_temp()
                self.program_block.append(f'(ASSIGN, 504, {temp_addr}, )')
                self.semantic_stack.append(temp_addr)
            self.call_stack.pop()
            # caller = self.call_stack.pop()
            # if caller == 'output':
            #     value = self.semantic_stack.pop()
            #     self.program_block.append(f'(PRINT, {value}, , )')
            #     self.semantic_stack.append(0)
            # else:
            #     index = len(self.program_block)
            #     self.program_block.append(f'(ASSIGN, #{index + 2}, 500, )')
            #     self.program_block.append(f'(JP, {caller.code_beginning}, , )')
            #     previous_return_address = self.semantic_stack.pop()
            #     self.program_block.append(f'(ASSIGN, {previous_return_address}, 500, )')
            #     last_address = caller.first_address + (caller.size - 1) * 4
            #     addr = last_address
            #     for _ in range(caller.size):
            #         saved_temp_addr = self.semantic_stack.pop()
            #         self.program_block.append(f'(ASSIGN, {saved_temp_addr}, {addr}, )')
            #         addr -= 4
            #     temp_addr = self.get_temp()
            #     self.program_block.append(f'(ASSIGN, 504, {temp_addr}, )')
            #     self.semantic_stack.append(temp_addr)
        elif action_symbol == ActionSymbols.RETURN_AT_THE_END_OF_FUNCTION:
            symbol = self.call_stack.pop()
            self.program_block.append(f'(ASSIGN, #0, 504, )')
            self.program_block.append(f'(JP, @500, , )')
            if symbol.lexeme == 'main':
                number_of_initialized_parameters = int((symbol.first_address - 100) / 4)
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
