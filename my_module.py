"""This module does random stuff."""

import swift as sw
import inspect, logging


@sw.add
def echo(string: str):
    '''echo a string'''
    log.loggers.echo.info('this is a test')
    print(string)

@sw.add
def add(x : int, y : int):
    '''add two integers'''
    log.loggers.add.info('this is another test')
    print(x + y)

@sw.add
def minus(x : int, y : int):
    print(x - y)

@sw.add
def do():
    log.loggers.do.debug('this function is do do')
    print(f'do {inspect.stack()[0][3]}')

### TESTS ###
# formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
# log = sw.logger(filecap=5, filetimeout='1m')
log = sw.logger(filetimeout='1m')
# log = sw.logger(filecap=5)
# log = sw.logger()

# log = sw.logger('my_module', ['echo', 'add', 'minus', 'do'])
# sw.cli(__doc__)
sw.cli(__doc__, logs=True)
# log = sw.logger()

# echo('test')
# add(1,2)
# do()

# need this for now to prevent empty files
log.out()

if __name__ == '__main__':
    pass