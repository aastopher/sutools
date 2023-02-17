"""This module does random stuff."""

import sutools as su
import inspect


@su.register
def echo(string: str):
    '''echo a string'''
    # log.loggers.echo.info('this is a test')
    su.log().echo.info('this is a test')
    print(string)

@su.register
def add(x : int, y : int):
    '''add two integers'''
    su.log().add.info('this is another test')
    print(x + y)

@su.register
def minus(x : int, y : int):
    su.log().minus.info(x - y)
    # print(x - y)

@su.register
def do():
    su.log().do.debug('this function is do do')
    print(f'do {inspect.stack()[0][3]}')

### EXAMPLES ###
# formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

# su.cli(__doc__, logs=True, loggers = su.logger(filecap=5, stream=True))
su.logger(filecap=5, stream=True)

# log = su.logger('my_module', ['echo', 'add', 'minus', 'do'])
# su.cli(__doc__)
# log = su.logger()


### FUNCTION TESTS ##
# echo('test')
# add(1,2)
minus(1,2)
do()

if __name__ == '__main__':
    su.cli(__doc__, logs=True)
    # su.cli(__doc__)