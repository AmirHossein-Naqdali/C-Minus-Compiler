# AmirHossein Naqdalie
# 400105296

from errorHandler import *
from fileHandler import *
from symbolTable import SymbolTable
from lexer.lexer import Lexer
from code_generator import CodeGenerator
from parsing.parser import Parser

input_text = read_code('input.txt')

symbol_table = SymbolTable()
lexer = Lexer(input_text, symbol_table)
code_generator = CodeGenerator(symbol_table)
parser = Parser(lexer, code_generator)

parser.parse()

# write_tokens(lexer.tokens)
# write_symbol_table(symbol_table)
# write_lexical_errors(lexical_errors)

# write_parse_tree(parser.node)
# write_syntax_errors(syntax_errors)

write_TAC(parser.code_generator.program_block)
