"""This module does random stuff."""

import sutools as su
import inspect, logging


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

### LOGGER EXAMPLES ###
# optionally pass in the name of your root application logger 
# by default this will be the filename
# su.logger(name='optional_name')

# optionally pass in your own set of functional logger names to add to the namespace of loggers
# by default this namespace will be defined as the set of names for all registered functions
# su.logger(loggers=['logger1','logger2','logger3'])

# optionally pass in your own log level default
# by default this is logging.INFO
# su.logger(loglvl=logging.DEBUG)

# optionally pass in your own file name structure
# by default this will be a datetime formatted string
# su.logger(filename=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

# optionally pass in a file path
# by default this will be ./logs/my_module/
# su.logger(filepath='./app/myLogs/')

# optionally pass in your own formatter to change the format of either the file or stream handler
# formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
# su.logger(streamfmt=formatter, streamfmt=formatter)

# optionally pass in your own file or stream handler
# by default this will be set to [logging.FileHandler(filepath, 'w'), logging.StreamHandler()]
# handler = logging.FileHandler(myHandlerPath, 'w')
# su.logger(fhandler=handler, shandler=handler)

# optionally turn off the file logging or streaming
# by default file is True and stream is False
# su.logger(file=False, stream=True)

# define a file cap <int>
# by default there is no cap
# su.logger(filecap=5)

# define a file timeout period
# time_units = {'m': 'minutes', 'h': 'hours', 'd': 'days', 'o':'months', 'y': 'years'}
# combined the above unit letters with the desired integer for that time unit i.e. (10m = 10 minute, 2h = 2 hours, ...)
# by default there is no timeout
# su.logger(filetimeout='1m')

# use with full default settings
# su.logger()

### END EXAMPLES ###

# for development
su.logger(stream=True)

# script level function tests for development
# echo('test')
# add(1,2)
# minus(1,2)
# do()


if __name__ == '__main__':
    ### CLI EXAMPLES ###

    # optionally add a cli description
    # by default this is None
    # su.cli(__doc__)

    # optionally turn logs on or off when running cli commands
    # by default this is False (i.e. logs will not run)
    # su.cli(__doc__, logs=True)

    # init a cli with all default settings
    # su.cli()

    ### END EXAMPLES ###

    # for development
    su.cli(__doc__, logs=True)