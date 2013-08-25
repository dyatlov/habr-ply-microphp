# coding=utf8

from lexer import tokens
import ply.yacc as yacc

class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

def p_php(p):
    '''php :
           | PHPSTART phpbody'''
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = p[2]

def p_phpbody(p):
    '''phpbody :
               | phpbody phpline phpcolons'''
    if len(p) > 1:
        if p[1] is None:
            p[1] = Node('body', [])
        p[0] = p[1].add_parts([p[2]])
    else:
        p[0] = Node('body', [])

def p_phpcolons(p):
    '''phpcolons : PHPCOLON
                 | phpcolons PHPCOLON'''

def p_phpline(p):
    '''phpline : assign
               | func
               | PHPECHO args'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('echo', [p[2]])

def p_assign(p):
    '''assign : PHPVAR PHPEQUAL expr'''
    p[0] = Node('assign', [p[1], p[3]])

def p_expr(p):
    '''expr : fact
            | expr PLUSMINUS fact'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_fact(p):
    '''fact : term
            | fact DIVMUL term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_term(p):
    '''term : arg
            | PHPOPEN expr PHPCLOSE'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_func(p):
    '''func : PHPFUNC PHPOPEN args PHPCLOSE'''
    p[0] = Node('func', [p[1], p[3]])

def p_args(p):
    '''args :
            | expr
            | args PHPCOMA expr'''
    if len(p) == 1:
        p[0] = Node('args', [])
    elif len(p) == 2:
        p[0] = Node('args', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_arg(p):
    '''arg : string
           | phpvar
           | PHPNUM
           | func'''
    p[0] = Node('arg', [p[1]])

def p_phpvar(p):
    '''phpvar : PHPVAR'''
    p[0] = Node('var', [p[1]])

def p_string(p):
    '''string : PHPSTRING str PHPSTRING'''
    p[0] = p[2]

def p_str(p):
    '''str :
           | STR
           | str phpvar'''
    if len(p) == 1:
        p[0] = Node('str', [''])
    elif len(p) == 2:
        p[0] = Node('str', [p[1]])
    else:
        p[0] = p[1].add_parts([p[2]])

def p_error(p):
    print 'Unexpected token:', p

parser = yacc.yacc()

def build_tree(code):
    return parser.parse(code)
