# coding=utf8

from parser import build_tree

data = '''
<?php
$val = 5;
$result = substr( "foobar", 2*(7-$val) ); /* comment */
echo "это наш результат: ", $result;
'''

result = build_tree(data)
print result
