#this is the parser for PA-3
import sys
from lex import LexToken
import yacc as yacc

tokens_filename = sys.argv[1]
tokens_filehandle = open(tokens_filename, 'r')
tokens_lines = tokens_filehandle.readlines()
tokens_filehandle.close()

def get_token_line():
    global tokens_lines
    result = tokens_lines[0].strip()
    print(result)
    tokens_lines = tokens_lines[1:]
    return result

pa2_tokens = []

while tokens_lines != []:
    line_number = get_token_line()
    token_type = get_token_line()
    token_lexeme = token_type
    if token_type in ['identifier', 'integer', 'type']:
        token_lexeme = get_token_line()
    pa2_tokens = pa2_tokens + [(line_number, token_type.upper(), token_lexeme)]

 
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

tokens = (
    'AT',
    'CASE',
    'CLASS',
    'COLON',
    'COMMA',
    'COMMENT',
    'DOT',
    'DIVIDE',
    'ELSE',
    'EQUALS',
    'ESAC',
    'FALSE',
    'FI',
    'IDENTIFIER',
    'IF',
    'IN',
    'INHERITS',
    'INTEGER',
    'ISVOID',
    'LARROW',
    'LBRACE',
    'LE',
    'LET',
    'LOOP',
    'LPAREN',
    'LT',
    'MINUS',
    'NEW',
    'NOT',
    'NUMBER',
    'OF',
    'PLUS',
    'POOL',
    'RARROW',
    'RBRACE',
    'RPAREN',
    'SEMI',
    'STRING',
    'THEN',
    'TILDE',
    'TIMES',
    'TRUE',
    'TYPE',
    'WHILE', 
    'NEWLINE'
)

precedence = ( ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE')  #binds more tightly
              )

def p_program_classlist(p):
    'program : classlist'
    p[0] = p[1]

def p_classlist_one(p):
    'classlist : '
    p[0] = []

def p_classlist_some(p):
    'classlist : class SEMI classlist'
    p[0] = [p[1]] + p[3]

def p_class_noinherit(p):
    'class : CLASS type LBRACE featurelist RBRACE'
    p[0] = (p.lineno(1), 'no_inherits', p[2], p[4])

def p_class_inherit(p):
    'class : CLASS type INHERITS type LBRACE featurelist RBRACE'
    p[0] = (p.lineno(1), 'inherits', p[2], p[4], p[6])

def p_type(p):
    'type : TYPE'
    p[0] = (p.lineno(1), p[1])

def p_featurelist_one(p):
    'featurelist : feature'
    p[0] = p[1]

def p_featurelist_some(p):
    'featurelist : feature SEMI featurelist'
    p[0] = [p[1]] + p[3]


def p_feature_withlist(p):
    'feature : IDENTIFIER LPAREN formal_parameters RPAREN COLON type LBRACE exp RBRACE'
    p[0] = (p.lineno(1), 'attribute_no_init', p[1], p[3], p[4])


def p_formal_parameters(p):
    '''formal_parameters : formal_parameter
                         | formal_parameter SEMI formal_parameters
                         | '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_formal_parameter(p):
    'formal_parameter : IDENTIFIER COLON type'
    p[0] = ('formal_parameter', p[1], p[3])

def p_formal_parameter_fail(p):
    '''formal_parameter : '''
    p[0]=["FAIL"]

def p_feature_attributeinit(p):
    'feature : IDENTIFIER COLON type LARROW exp'
    p[0] = (p.lineno(1), 'attribute_init', p[1], p[3], p[5])

def p_feature_attributenoinit(p):
    'feature : IDENTIFIER COLON type'
    p[0] = (p.lineno(1), 'attribute_init', p[1], p[3])

def p_exp_plus(p):
    'exp : exp PLUS exp'
    p[0] = ((p[1])[0], 'plus' , p[1], p[3]) 

def p_exp_minus(p):
    'exp : exp MINUS exp'
    p[0] = ((p[1])[0], 'minus' , p[1], p[3]) 

def p_exp_times(p):
    'exp : exp TIMES exp'
    p[0] = ((p[1])[0], 'times' , p[1], p[3])

def p_exp_divide(p):
    'exp : exp DIVIDE exp'
    p[0] = ((p[1])[0], 'divide' , p[1], p[3])

def p_exp_tilde(p):
    'exp : TILDE exp'
    p[0] = (p.lineno(1), 'tilde', p[2])

def p_exp_lt(p):
    'exp : exp LT exp'
    p[0] = ((p[1])[0], 'lt', p[1], p[3])

def p_exp_le(p):
    'exp : exp LE exp'
    p[0] = ((p[1])[0], 'le', p[1], p[3])

def p_exp_equals(p):
    'exp : exp EQUALS exp'
    p[0] = ((p[1])[0], 'eq', p[1], p[3])

def p_exp_not(p):
    'exp : NOT exp'
    p[0] = (p.lineno(1), 'not', p[2])

def p_exp_paren(p): # very unsure of this one, not on the project output guidelines?
    'exp : LPAREN exp RPAREN'
    p[0] = (p.lineno(1), "paren", p[2]) 

def p_exp_integer(p):
    'exp : INTEGER'
    p[0] = (p.lineno(1), 'integer', p[1])


def p_exp_isvoid(p):
    'exp : ISVOID exp'
    p[0] = (p.lineno(1), 'isvoid', p[2])

def p_exp_new(p):
    'exp : NEW type'
    p[0] = (p.lineno(1), 'new', p[2])

def p_exp_assign(p):
    'exp : IDENTIFIER LARROW exp'
    p[0] = (p.lineno(2), 'assign', p[1], p[3])

def p_expr_dispatch(p):
    '''exp : IDENTIFIER LPAREN exp_list RPAREN 
            | exp DOT IDENTIFIER LPAREN exp_list RPAREN
            | exp DOT IDENTIFIER LPAREN RPAREN'''
    if len(p) == 6:
        p[0] = (p.lineno(1), 'dynamic_dispatch', p[1], p[3], p[5])
    elif len(p) == 5:
        p[0] = (p.lineno(1), 'dynamic_dispatch', p[1], None, p[4])
    elif len(p) == 8:
        p[0] = (p.lineno(1), 'static_dispatch', p[1], p[3], p[5], p[7])
    else:
        p[0] = (p.lineno(1), 'static_dispatch', p[1], p[3], None, p[6])

def p_exp_if(p):
    'exp : IF exp THEN exp ELSE exp FI'
    p[0] = (p.lineno(1), 'if', p[2], p[4], p[6])

def p_exp_while(p):
    'exp : WHILE exp LOOP exp POOL'
    p[0] = (p.lineno(1), 'while', p[2], p[4])

def p_exp_block(p):
    'exp : LBRACE exp_list_semi RBRACE'
    p[0] = (p.lineno(1), 'block', p[2])

def p_exp_let(p):
    'exp : LET let_list IN exp'
    p[0] = (p.lineno(1), 'let', p[2], p[4])

def p_let_list_one(p):
    '''let_list : IDENTIFIER COLON TYPE
                | IDENTIFIER COLON TYPE LARROW exp '''
    if len(p) == 4:
        p[0] = [(p.lineno(1), 'let_binding_no_init', p[1], p[3])]
    elif len(p) == 6:
        p[0] = [(p.lineno(1), 'let_binding_init', p[1], p[3], p[5])]
    else:
        p[0] = [(p.lineno(1), 'let_binding_no_init', p[1], p[3])] + p[5]

def p_let_list(p):
    '''let_list : '''
    p[0] = []

def p_exp_case(p):
    'exp : CASE exp OF case_list ESAC'
    p[0] = (p.lineno(1), 'case', p[2], p[4])

def p_case_list(p):
    '''case_list : IDENTIFIER COLON TYPE LARROW exp
                 | IDENTIFIER COLON TYPE LARROW exp SEMI case_list'''
    if len(p) == 6:
        p[0] = [(p.lineno(1), p[1], p[3], p[5])]
    else:
        p[0] = [(p.lineno(1), p[1], p[3], p[5])] + p[7]

def p_case_list_one(p):
    '''case_list : '''
    p[0] = []


def p_exp_dispatch_static(p):
    'exp : exp AT TYPE DOT IDENTIFIER LPAREN exp_list RPAREN'
    p[0] = (p.lineno(2), 'static_dispatch', p[1], p[3], p[5], p[7])

def p_exp_list_empty(p):
    'exp_list : '
    p[0] = []

def p_exp_list_multiple(p):
    'exp_list : exp SEMI exp_list'
    p[0] = p[1] + [p[3]]


def p_exp_list_semi_empty(p):
    'exp_list_semi : '
    p[0] = []

def p_exp_list_semi_multiple(p):
    'exp_list_semi : exp SEMI SEMI exp_list_semi'
    p[0] = p[1] + [p[3]]


def p_exp_id(p):
    'exp : IDENTIFIER'
    p[0] = p[1]


def p_error(p):
    if p:
         print("ERROR: ", p.lineno, ": Parser:  parse error near ", p.type)
         # Just discard the token and tell the parser it's okay.
         exit(1)
    else:
        #  FIGUREOUT HOW TO END FILE
         print("Syntax error at EOF") #FIX THIS

#build the PA3 parser from the above rules 

parser = yacc.yacc()
ast = yacc.parse(lexer=pa2lexer)

print(ast)

ast_filename = (sys.argv[1])[:-4]+ "-ast"
fout = open(ast_filename, 'w')

def print_identifier(ast):
    fout.write(str(ast[0]) + "\n")
    fout.write(ast[1] + "\n")

def print_exp(ast, line_number=0):
    fout.write(str(line_number) + "\n")
    expression_type = ast[0]
    if expression_type == 'assign':
        fout.write("assign\n")
        fout.write("var:" + ast[1] + "\n")
        print_exp(ast[2])
    elif expression_type == 'dynamic_dispatch':
        fout.write("dynamic_dispatch\n")
        print_exp(ast[1])
        fout.write("method:" + ast[2] + "\n")
        print_exp(ast[3])
    elif expression_type == 'static_dispatch':
        fout.write("static_dispatch\n")
        print_exp(ast[1])
        fout.write("type:" + ast[2] + "\n")
        fout.write("method:" + ast[3] + "\n")
        print_exp(ast[4])
    elif expression_type == 'self_dispatch':
        fout.write("self_dispatch\n")
        fout.write("method:" + ast[1] + "\n")
        print_exp(ast[2])
    elif expression_type == 'if':
        fout.write("if\n")
        print_exp(ast[1])
        print_exp(ast[2])
        print_exp(ast[3])
    elif expression_type == 'while':
        fout.write("while\n")
        print_exp(ast[1])
        print_exp(ast[2])
    elif expression_type == 'block':
        fout.write("block\n")
        for exp in ast[1:]:
            print_exp(exp)
    elif expression_type == 'new':
        fout.write("new\n")
        fout.write("class:" + ast[1] + "\n")
    elif expression_type == 'isvoid':
        fout.write("isvoid\n")
        print_exp(ast[1])
    elif expression_type in ['plus', 'minus', 'times', 'divide', 'lt', 'le', 'eq']:
        fout.write(expression_type + "\n")
        print_exp(ast[1])
        print_exp(ast[2])
    elif expression_type in ['not', 'negate', 'integer', 'string', 'identifier', 'true', 'false']:
        print(str(ast[0]) + "\n"+ ast[1] + "\n")
        fout.write(expression_type + "\n")
        if len(ast) > 1:
            fout.write(ast[1] + "\n")
    elif expression_type == 'let':
        fout.write("let\n")
        for binding in ast[1]:
            if len(binding) == 2:
                fout.write("let_binding_no_init\n")
                fout.write("variable:" + binding[0] + "\n")
                fout.write("type:" + binding[1] + "\n")
            elif len(binding) == 3:
                fout.write("let_binding_init\n")
                fout.write("variable:" + binding[0] + "\n")
                fout.write("type:" + binding[1] + "\n")
                print_exp(binding[2])
        print_exp(ast[2])
    elif expression_type == 'case':
        fout.write("case\n")
        print_exp(ast[1])
        for case_element in ast[2:]:
            fout.write("case-element\n")
            fout.write("variable:" + case_element[0] + "\n")
            fout.write("type:" + case_element[1] + "\n")
            print_exp(case_element[2])
    else:
        print("unhandled expression" + expression_type)
        exit(1)

def print_feature(ast):
    if ast[1]== 'attribute_no_init':
        fout.write("attribute_no_init\n")
        print_identifier(ast[2])
        print_identifier(ast[3])
    elif ast[1]== 'attribute_init':
        fout.write("attribute_init\n")
        print_identifier(ast[2])
        print_identifier(ast[3])
        print_exp(ast[4])
    else :
        print("unhandled expression" + ast[1])
        exit(1)

def print_list(ast, print_element_function):
    fout.write(str(len(ast))+ "\n") 
    for elem in ast:
        print_element_function(elem)

def print_class(ast):
    print_identifier(ast[2])
    fout.write("no_inherits\n")
    print_list(ast[3], print_feature)

def print_program(ast):
    print_list(ast, print_class)
    
print_program(ast)
fout.close()