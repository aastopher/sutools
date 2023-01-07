"""This module does random stuff."""

import swift as sw
import inspect

# scli = sw.cli(__doc__)

# test_logger = sw.logger('my_module', ['echo', 'add', 'minus', 'do'])
# echo_logger = test_logger.getLogger('echo')

test_logger = sw.logger('my_module', ['echo', 'add', 'minus', 'do'])


@sw.add
def echo(string: str):
    '''echo a string'''
    # test_logger.loggers.echo.info('testing')
    print(test_logger.loggers)
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

sw.cli(__doc__)

# test_logger.log()

# sw.logger()

# scli.parse()

print(test_logger.loggers)
echo('test')
# print(sw.store.funcs)

if __name__ == '__main__':
    pass