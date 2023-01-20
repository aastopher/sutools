"""This module does random stuff."""

import swift as sw
import inspect


@sw.add
def echo(string: str):
    '''echo a string'''
    log.echo.info('this is a test')
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


log = sw.logger()
# log = sw.logger('my_module', ['echo', 'add', 'minus', 'do'])
# sw.cli(__doc__)
sw.cli(__doc__, logs=False)
# log = sw.logger()

# echo('test')

if __name__ == '__main__':
    pass