#this is the parser for PA-3
import sys
from lexer import LexToken
import yacc as yacc

tokens_filename = sys.argv[1]
tokens_filehandle = open(tokens_filename, "r")
tokens_lines = tokens_filehandle.readlines()
tokens_filehandle.close()

def get_token_line():
    global tokens_lines
    result = tokens_lines[0].strip()
    tokens_lines = tokens_lines[1:]
    return result

pa2_tokens = []

while tokens_lines != []:
    line_number = get_token_line()
    token_type = get_token_line()
    if token_type in ['identifier', 'integer', 'type']:
        token_value = get_token_line()
        pa2_tokens.append((line_number, token_type.upper(), token_value))
    else:
        pa2_tokens.append((line_number, token_type.upper(), token_type))

 
class PA2Lexer(object):
    def token(whatever):
        global pa2_tokens
        if pa2_tokens == []:
            return None
        (line, token_type, lexeme) = pa2_tokens[0]
        pa2_tokens = pa2_tokens[1:]
        tok = LexToken()
        tok.type = token_type
        tok.value = lexeme
        tok.lineno = line
        tok.lexpos = 0
        return tok
    
pa2lexer = PA2Lexer()

# Define our grammar