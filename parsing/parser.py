from anytree import Node

from code_generator import CodeGenerator
from errorHandler import report_syntax_error
from lexer.lexer import Lexer
from .grammar import *
from .parsing_table import *


class Parser:
    def __init__(self, lexer: Lexer, code_generator: CodeGenerator):
        self.lexer = lexer
        self.code_generator = code_generator
        self.__current_token = None
        self.__lookahead = None
        self.node = Node(start_symbol.name)
        self.stack = [start_symbol]
        create_parsing_table()

    def __get_token(self):
        self.__current_token = self.lexer.get_next_token()
        if self.__current_token.type in ['KEYWORD', 'SYMBOL', 'END']:
            la = self.__current_token.lexeme
        else:
            la = self.__current_token.type
        self.__lookahead = Terminals.get_enum_by_content(la)

    def parse(self):
        is_running = True
        nodes = [self.node]
        self.__get_token()
        while self.stack and is_running:
            top = self.stack[-1]
            if type(top) is ActionSymbols:
                self.code_generator.code_gen(top, self.__current_token)
                self.stack.pop()
            elif type(top) is CheckSymbols:
                self.code_generator.semantic_check(top, self.__current_token)
                self.stack.pop()
            elif type(top) is Terminals:
                if top == Terminals.EPSILON:
                    self.stack.pop()
                    node = nodes.pop(0)
                    node.name = Terminals.EPSILON.content
                elif top == self.__lookahead:
                    self.stack.pop()
                    node = nodes.pop(0)
                    node.name = '(' + self.__current_token.type + ', ' + self.__current_token.lexeme + ')'
                    self.__get_token()
                else:
                    report_syntax_error(self.__current_token.line_number, f'missing {top.content}')
                    self.stack.pop()
                    node = nodes.pop(0)
                    node.parent = None
            else:
                action = ll1_table[top.name][self.__lookahead.name]
                if action is None:
                    if self.__lookahead == Terminals.DOLLAR:
                        report_syntax_error(self.__current_token.line_number, f'Unexpected EOF')
                        is_running = False
                        for node in nodes:
                            node.parent = None
                    else:
                        report_syntax_error(self.__current_token.line_number, f'illegal {self.__lookahead.content}')
                        self.__get_token()
                elif type(action) is str:
                    report_syntax_error(self.__current_token.line_number, f'missing {top.name}')
                    self.stack.pop()
                    node = nodes.pop(0)
                    node.parent = None
                else:
                    new_node = nodes.pop(0)
                    new_nodes = []
                    for variable in action:
                        if type(variable) is not Terminals and type(variable) is not NonTerminals:
                            continue
                        new_nodes.append(Node(variable.name, parent=new_node))
                    nodes = new_nodes + nodes
                    self.stack.pop()
                    self.stack += action[::-1]
        if is_running:
            Node(Terminals.DOLLAR.content, self.node)
        if self.code_generator.is_erroneous:
            self.code_generator.program_block = []
