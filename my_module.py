"""This module does random stuff."""

import swift as sw
import inspect

# scli = sw.cli(__doc__)

test_logger = sw.logger('my_module', ['echo', 'add', 'minus', 'do'])
echo_logger = test_logger.getLogger('echo')

@sw.add
def echo(string: str):
    '''echo a string'''
    echo_logger.info(f'echo this {string}')
    print(string)

@sw.add
def add(x : int, y : int):
    '''add two integers'''
    print(x + y)

@sw.add
def minus(x : int, y : int):
    print(x - y)

@sw.add
def do():
  print(f'do {inspect.stack()[0][3]}')

# sw.cli(__doc__)

# sw.logger()

# scli.parse()

# echo('blah blah')
# print(sw.store.funcs)

if __name__ == '__main__':
    pass