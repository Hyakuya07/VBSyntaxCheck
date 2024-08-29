from ply import lex, yacc

flag = 0

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'IFERS',
    'DOUBLESLASH',
    'MOD',
    'EXPONENT',
    'EQUALS',
    'WHILE_LOOP',
    'DIM',
    'AS',
    'END',
    'COL',
    'TRUE',
    'FALSE',
    'COM',
    'LESSTE',
    'LESST',
    'GREATT',
    'GREATTE',
    'EQUALT',
    'NEQUALT',
    'WRITE',
    'WRITELINE',
    'INTEGER',
    'DOUBLE',
    'SINGLE',
    'STRING',
    'BOOLEAN',
    'CHAR',
    'DECIMAL',
    'LONG',
    'OBJECT',
    'DATE',
    'STRINGS',
    'SUB',
    'FUNCTION',
    'PP',
    'FIFFERS'

)

# Regular expression rules for simple tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_DOUBLESLASH = r'//'
t_MOD = r'%'
t_EXPONENT = r'\^'

t_EQUALS = r'='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COL = r':'
t_COM = r','

t_EQUALT = r'=='
t_LESST = r'<'
t_LESSTE = r'<='
t_GREATT = r'>'
t_GREATTE = r'>='
t_NEQUALT = r'<>'

t_STRINGS = r'(\'[^\']*\'|\"[^\"]*\")'

reserved = {

    'While': 'WHILE_LOOP',
    'True': 'TRUE',
    'False': 'FALSE',

    'Dim': 'DIM',
    'As': 'AS',

    'Integer': 'INTEGER',
    'Double': 'DOUBLE',
    'Single': 'SINGLE',
    'String': 'STRING',
    'Boolean': 'BOOLEAN',
    'Char': 'CHAR',
    'Decimal': 'DECIMAL',
    'Long': 'LONG',
    'Object': 'OBJECT',
    'Date': 'DATE',

}


def t_PP(t):
    r'(Private|Public)\b'
    return t


def t_SUB(t):
    r'Sub'
    return t


def t_FUNCTION(t):
    r'Function'
    return t


def t_FIFFERS(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*\('
    return t


def t_END(t):
    r'End'
    return t


def t_WRITE(t):
    r'Console\.Write\('
    return t


def t_WRITELINE(t):
    r'Console\.WriteLine\('
    return t


def t_IFERS(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IFERS')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \n\t'


# Error handling rule for lexer
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD', 'DOUBLESLASH'),
    ('right', 'EXPONENT'),
)


def p_start(p):
    '''
    start : fdec
          | expression
          | while
          | vdec
          | console
    '''


def p_fdec(p):
    '''
    fdec : PP FUNCTION FIFFERS args RPAREN COL statements END FUNCTION
         | PP SUB FIFFERS args RPAREN COL statements END SUB
         | FUNCTION FIFFERS args RPAREN COL statements END FUNCTION
         | SUB FIFFERS args RPAREN COL statements END SUB
    '''


def p_arg(p):
    '''
    arg : ifers AS types
    '''


def p_args(p):
    '''
    args : arg COM args
         | arg
         | empty
    '''


def p_empty(p):
    'empty :'
    pass


def p_console(p):
    '''
    console : WRITE strings RPAREN
            | WRITELINE strings RPAREN
    '''


def p_strings(p):
    '''
    strings : STRINGS COM strings
            | STRINGS
            | IFERS
            | IFERS COM strings
    '''


def p_expression(p):
    '''
    expression : term
               | expression PLUS term
               | expression MINUS term
    '''


def p_vdec(p):
    '''
    vdec : DIM ifers AS types
         | DIM IFERS AS types
    '''


def p_ifers(p):
    '''
    ifers : IFERS
          | IFERS COM ifers
    '''


def p_types(p):
    '''
    types : INTEGER
          | DOUBLE
          | SINGLE
          | STRING
          | BOOLEAN
          | CHAR
          | DECIMAL
          | LONG
          | OBJECT
          | DATE
    '''


def p_term(p):
    '''
    term : factor
         | term TIMES factor
         | term DIVIDE factor
         | term MOD factor
         | term DOUBLESLASH factor
    '''


def p_factor(p):
    '''
    factor : primary
           | factor EXPONENT primary
    '''


def p_while(p):
    '''
    while : WHILE_LOOP condition COL statements  END WHILE_LOOP
    '''


def p_relation(p):
    '''
    relation : LESSTE
             | LESST
             | GREATT
             | GREATTE
             | EQUALT
             | NEQUALT
    '''


def p_condition(p):
    '''
    condition : IFERS relation IFERS
         | IFERS relation NUMBER
         | NUMBER relation IFERS
         | NUMBER relation NUMBER
         | TRUE
         | FALSE
    '''


def p_statements(p):
    '''
    statements : states COL statements
               | states COL
    '''


def p_states(p):
    '''
    states : assignment
           | while
           | vdec
           | fdec
           | expression
           | console
    '''


def p_assignment(p):
    '''
    assignment : ifers EQUALS expression
    '''


def p_primary(p):
    '''
    primary : NUMBER
            | IFERS
            | LPAREN expression RPAREN
    '''


def p_error(p):
    try:
        print(f"Syntax error at position {p.lexpos}, unexpected token '{p.value}'")
        global flag
        flag = 1
    except:
        print(f"Syntax error, unexpected token")
        flag = 1

    # Build the parser


parser = yacc.yacc()

while True:
    # Get input from the user
    code_to_check = input("\nCode to check : ")

    # Check if the input is an empty string
    if not code_to_check.strip():
        print("\nExiting the parser.\n")
        break

    # Parse the user input
    parser.parse(code_to_check)
    if flag == 0:
        print("Valid Syntax")
    else:
        flag = 0

'''

multiline = 
            """
            While True: 
                a = 10
            End While
            """
print('Parsed Code : ', multiline)
parser.parse(multiline)
parser.parse(code_to_check)
    if flag == 0:
        print("Valid Syntax")
    else:
        flag = 0            

'''