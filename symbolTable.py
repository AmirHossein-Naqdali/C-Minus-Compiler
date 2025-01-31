class Symbol:
    def __init__(self, lexeme=None, first_address=0):
        self.lexeme = lexeme
        self.type = None
        self.address = 0
        self.is_array = False
        self.is_function = False
        self.parameters = []
        self.size = 0
        self.first_address = first_address
        self.code_beginning = None

    def __str__(self):
        return f'lexeme: {self.lexeme}, type: {self.type}, address: {self.address}, is_array: {self.is_array}, ' \
               f'is_function: {self.is_function}, size: {self.size}, parameters: {self.parameters}, ' \
               f'first_address: {self.first_address}, code_beginning: {self.code_beginning}'


class SymbolTable:
    def __init__(self):
        self.table = [[]]
        self.is_declaring = False
        self.current_address = 100

    def add_to_symbol_table(self, token_type, token_string):
        if token_type != 'ID' or not self.is_declaring:
            return
        sym = Symbol(lexeme=token_string, first_address=self.current_address)
        self.table[-1].append(sym)
        self.is_declaring = False

    def add_scope(self):
        self.table.append([])

    def del_scope(self):
        self.table.pop()

    def update_type(self, type):
        symbol = self.table[-1][-1]
        symbol.type = type

    def update_last_symbol(self, is_array=False, size=0):
        symbol = self.table[-1][-1]
        symbol.is_array = is_array
        symbol.size = size
        symbol.address = self.current_address
        if size == 0:
            self.current_address += 4
        else:
            self.current_address += size * 4
        return symbol

    def update_last_function(self):
        symbol = self.table[-2][-1]
        symbol.is_function = True
        for sym in self.table[-1]:
            symbol.parameters.append(sym.address)
        symbol.size = len(symbol.parameters)
        return symbol

    def get_last_function(self):
        for scope in reversed(self.table):
            for symbol in reversed(scope):
                if symbol.is_function:
                    return symbol

    def print_table(self):
        for i, scope in enumerate(self.table):
            print(f'scope {i}: ')
            for sym in scope:
                print(f'\t{sym}')
        print('end print')

    def find_symbol(self, lexeme):
        for scope in reversed(self.table):
            for symbol in reversed(scope):
                if symbol.lexeme == lexeme:
                    return symbol
        return None

    def last_used_address(self):
        return self.current_address - 4
