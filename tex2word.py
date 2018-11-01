from collections import namedtuple
from ply import lex, yacc

tokens = ('CMD',
#    'LITERALNEWLINE',
    'MANUALNEWLINE',
    'WORD',
    'COMMENT',
    'COLSPEC'
)

t_CMD = r'\\(?P<cmd>[a-zA-Z0-9]+)'
#t_LITERALNEWLINE = '[\n]'
t_MANUALNEWLINE = r'\\\\'
t_WORD = r'(?<!\\)[a-zA-Z0-9|:!&]+|\\%'
t_COMMENT = r'[%].*'
t_COLSPEC = r'[lcr]'
t_ignore = ' \t'

def t_error(tok) :
    print('lex error:')
    print(tok)

# latex grammar is like:
# document        : expression
#                 | expression document
# expression      : WORD
#                 | command
#                 | COMMENT
#                 | tabular_colspec
#                 | expression
# command         : CMD
#                 | CMD LBRACE expression RBRACE
#                 | CMD LBRACKET paramlist RBRACKET LBRACE expression RBRACE
#                 | CMD LBRACE expression RBRACE LBRACE expression RBRACE
#                 | CMD LBRACE expression RBRACE LBRACKET expression RBRACKET LBRACE expression RBRACE

Text = namedtuple('Text',('value',))
Newline = namedtuple('Newline',())
Comment = namedtuple('Comment',('value',))
Command = namedtuple('Command',('name','arg1','arg2','opts'))

literals = ['{','}','[',']',',','\n']
def p_expression_word(p):
    '''expression : WORD
                  | WORD expression'''
    if len(p) == 2 :
        p[0] = [Text(p[1])]
    else :
        p[0] = [Text(p[1])]+p[2]

def p_expression_newline(p):
    r'''expression : '\n'
                   | '\n' expression
                   | MANUALNEWLINE
                   | MANUALNEWLINE expression
                  '''
    if len(p) == 2 :
        p[0] = [Newline()]
    else :
        p[0] = [Newline()]+p[2]

def p_expression_cmd(p):
    '''expression : command
                  | command expression'''
    p[0] = [p[1]]+p[2:]

def p_expression_comment(p):
    '''expression : COMMENT
                  | COMMENT expression'''
    if len(p) == 2 :
        p[0] = [Comment(p[1])]
    else :
        p[0] = [Comment(p[1])]+p[2:]

def p_command_noarg(p):
    'command : CMD'
    p[0] = Command(p[1],None,None,None)
def p_command_onearg(p) :
    "command : CMD '{' expression '}'"
    p[0] = Command(p[1],p[3],None,None)
def p_command_optarg(p) :
    "command : CMD '[' expression ']' '{' expression '}'"
    p[0] = Command(p[1],p[6],None,p[3])
def p_command_argopt(p) :
    "command : CMD '{' expression '}' '[' expression ']'"
    p[0] = Command(p[1],p[6],None,p[3])
def p_command_twoarg(p) :
    "command : CMD '{' expression '}' '{' expression '}'"
    p[0] = Command(p[1],p[3],p[6],None)
def p_command_argoptarg(p) :
    "command : CMD '{' expression '}' '[' expression ']' '{' expression '}'"
    p[0] = Command(p[1],p[3],p[9],p[6])

def p_error(p) :
    print('parsing error:')
    print(p)

lexer = lex.lex()
parser = yacc.yacc()

def tex_to_word(tex) :

    result = parser.parse(tex.strip())
    return result

    #while True :
    #    tok = lexer.token()
    #    if not tok: break
    #    print(tok)
