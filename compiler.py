# AmirHossein Naqdalie
# 400105296

from errorHandler import *
from fileHandler import *
from lexer.lexer import Lexer
from lexer.symbolTable import symbol_table
from parsing.parser import Parser

input_text = read_code('input.txt')

lexer = Lexer(input_text)

parser = Parser(lexer)
parser.parse()

# write_tokens(lexer.tokens)
# write_symbol_table(symbol_table)
# write_lexical_errors(lexical_errors)

write_parse_tree(parser.node)
write_syntax_errors(syntax_errors)
