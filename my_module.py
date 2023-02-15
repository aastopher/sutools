"""This module does random stuff."""

import swift as sw
import inspect


@sw.add
def echo(string: str):
    '''echo a string'''
    # log.loggers.echo.info('this is a test')
    sw.log().echo.info('this is a test')
    print(string)

@sw.add
def add(x : int, y : int):
    '''add two integers'''
    sw.log().add.info('this is another test')
    print(x + y)

@sw.add
def minus(x : int, y : int):
    sw.log().minus.info(x - y)
    # print(x - y)

@sw.add
def do():
    sw.log().do.debug('this function is do do')
    print(f'do {inspect.stack()[0][3]}')

### EXAMPLES ###
# formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

# sw.cli(__doc__, logs=True, loggers = sw.logger(filecap=5, stream=True))
sw.logger(filecap=5, stream=True)

# log = sw.logger('my_module', ['echo', 'add', 'minus', 'do'])
# sw.cli(__doc__)
sw.cli(__doc__, logs=True)
# log = sw.logger()


### FUNCTION TESTS ##
# echo('test')
# add(1,2)
minus(1,2)
# do()

if __name__ == '__main__':
    pass