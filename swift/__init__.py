from swift import cli_handler
from swift import log_handler
from swift import meta_handler

import inspect, os, logging, datetime
from pathlib import Path

store = meta_handler.Bucket()

def add(func):
    '''add function to store'''
    store.add_func(func)
    return func

def cli(desc=None, logs=False):
    '''init cli and store'''

    if store.log:
        cli_obj = cli_handler.CLI(desc, logs, store.log.loggers)
    else:
        cli_obj = cli_handler.CLI(desc, logs)
    cli_obj.add_funcs(store.funcs)
    cli_obj.parse()
    store.add_cli(cli_obj)
    return cli_obj

# CLI NOTES:
# * add debug command for running module with debug level logs
# * check cli is working with stream handler


def logger(name = os.path.basename(inspect.stack()[-1].filename)[:-3], 
           loggers = None, 
           filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), 
           filepath = None,
           loglvl = logging.INFO,
           formatter = logging.Formatter('%(asctime)s, %(msecs)d %(name)s \t %(levelname)s \t %(message)s', datefmt='%H:%M:%S'), 
           handler = None,
           filecap = None, 
           filetimeout = None):
    '''init logger object and store'''

    # if check for filepath must be inside function because filename is not initialized
    if not filepath:
        filepath = os.path.join('logs', name, f'{filename}.log')

    # check if log path parent directory has been initialized
    if not os.path.exists(Path(filepath).parent):
        os.makedirs(Path(filepath).parent) # make parent directory tree for given filepath
    
    # if check for handler must be inside function because filename is not initialized
    if not handler:
        handler = logging.FileHandler(filepath, 'w')

    # if check for loggers must be inside function because func keys will be empty at initialization
    if not loggers and store.funcs:
        log_obj = log_handler.Logger(name, list(store.funcs.keys()), filename, filepath, loglvl, formatter, handler, filecap, filetimeout)
    else:
        log_obj = log_handler.Logger(name, loggers, filename, filepath, loglvl, formatter, handler, filecap, filetimeout)

    store.add_log(log_obj)
    return log_obj

# LOG NOTES:
# * Simplify
# * add stream handling ability (console logging) with ability to pass formatter to that as well
# * de-standardize naming of logger_object if possible. (standardization was forced at first to enable CLI to run functions with loggers in them)
# * alter empty file creation fix to not need separate out call at end of module
# * if no cli exists logger must create cli for debug command (should have - options to call all levels)

# __init__
# * import importing module into init after start up to be able to feed module to cli for debug
# * importing the import may also assist in refactoring current empty file management solution