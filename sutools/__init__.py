from sutools import cli_handler
from sutools import log_handler
from sutools import meta_handler

import inspect, os, logging, datetime
from pathlib import Path

# init store
store = meta_handler.Bucket()

def register(func):
    '''register a function to the store'''
    store.add_func(func)
    return func

def cli(desc = None, logs = False):
    '''init cli and register to store'''

    if store.log:
        cli_obj = cli_handler.CLI(desc, logs, store.log)
    else:
        cli_obj = cli_handler.CLI(desc, logs)

    cli_obj.add_funcs(store.funcs)
    cli_obj.parse()
    store.add_cli(cli_obj)
    return cli_obj
    
def logger(name = os.path.basename(inspect.stack()[-1].filename)[:-3], 
           loggers = None, 
           loglvl = logging.INFO,
           filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), 
           filepath = None,
           filefmt = logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'), 
           fhandler = None,
           filecap = None, 
           filetimeout = None,
           file = True, 
           streamfmt = logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'),
           shandler = logging.StreamHandler(),
           stream = False):
    '''init logger object and register to store'''

    # if check for filepath must be inside function because filename is not initialized
    if not filepath:
        filepath = os.path.join('logs', name, f'{filename}.log')
    elif filepath:
        filepath = os.path.join(filepath, name, f'{filename}.log')

    # check if log path parent directory has been initialized
    if not os.path.exists(Path(filepath).parent):
        os.makedirs(Path(filepath).parent) # make parent directory tree for given filepath
    
    # if check for handler must be inside function because filename is not initialized
    if not fhandler:
        fhandler = logging.FileHandler(filepath, 'w')

    # if check for loggers must be inside function because func keys will be empty at initialization
    if not loggers and store.funcs:
        log_obj = log_handler.Logger(name, list(store.funcs.keys()), loglvl, filename, filepath, filefmt, fhandler, filecap, filetimeout, file, streamfmt, shandler, stream)
    else:
        log_obj = log_handler.Logger(name, loggers, loglvl, filename, filepath, filefmt, fhandler, filecap, filetimeout, file, streamfmt, shandler, stream)
    store.add_log(log_obj)
    return log_obj

def log():
    '''retrieve loggers namespace from store'''
    return store.log.loggers