# coding=utf8
import ply.lex as lex
from ply.lex import TOKEN
import re

states = (
   ('string','exclusive'),
)

# без этой штуки ничего не съинтерпретируется, потому что этот массив шарится между лексером и парсером и кроме того используется внутренне библиотекой
tokens = (
    'PHPSTART', 'PHPVAR', 'PHPEQUAL', 'PHPFUNC',
    'PHPSTRING', 'PHPECHO', 'PHPCOLON', 'PHPCOMA',
    'PHPOPEN', 'PHPCLOSE', 'PHPNUM', 'PLUSMINUS', 'DIVMUL',
    'STR'
)

# определим регулярку для абстрактного идетификатора
ident = r'[a-z]\w*'

# для каждого токена из массива мы должны написать его определение вида t_ИМЯТОКЕНА = регулярка
t_PHPSTART = r'\<\?php'
t_ANY_PHPVAR = r'\$'+ident # очень удобно, правда?
t_PHPEQUAL = r'\='
t_PHPCOLON = r';'
t_PHPCOMA = r','
t_PHPOPEN = r'\('
t_PHPCLOSE = r'\)'
t_PHPNUM = r'\d+'
t_PLUSMINUS = r'\+|\-'
t_DIVMUL = r'/|\*'

@TOKEN(ident)
def t_PHPFUNC(t):
    if t.value.lower() == 'echo':
        t.type = 'PHPECHO'
    return t

# игнорируем комментарии
def t_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

# изменили токен PHPSTRING и сделали из него функцию, добавили его во все состояния
def t_ANY_PHPSTRING(t): # нужен в обоих состояниях, потому что двойные кавычки матчатся и там и там.
    r'"'
    if t.lexer.current_state() == 'string':
        t.lexer.begin('INITIAL') # переходим в начальное состояние
    else:
        t.lexer.begin('string') # парсим строку
    return t

t_string_STR = r'(\\.|[^$"])+' # парсим пока не дойдем до переменной или до кавычки, попутно игнорируем экранки

# говорим что ничего не будем игнорировать
t_string_ignore = '' # это кстати обязательная переменная, без неё нельзя создать новый state

# ну и куда же мы без обработки ошибок
def t_string_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# здесь мы игнорируем незначащие символы. Нам ведь все равно, написано $var=$value или $var&nbsp;&nbsp;&nbsp;=&nbsp;&nbsp;$value
t_ignore = ' \r\t\f'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# а здесь мы обрабатываем ошибки. Кстати заметьте формат названия функции
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.UNICODE | re.DOTALL | re.IGNORECASE)

if __name__=="__main__":
    data = '''
<?php
$val = 5;
$result = substr( "foobar", 2*(7-$val) );
echo "это наш результат: $result";
    '''

    lexer.input(data)

    while True:
        tok = lexer.token() # читаем следующий токен
        if not tok: break      # закончились печеньки
        print tok
