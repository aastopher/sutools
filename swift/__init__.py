from swift import cli_handler
from swift import log_handler
from swift import meta_handler

import inspect, os, logging

store = meta_handler.Bucket()

def add(func):
    store.add_func(func)
    return func

def cli(doc=None, logs=False):
    if store.log:
        cli_obj = cli_handler.CLI(doc, logs, store.log.loggers)
    else:
        cli_obj = cli_handler.CLI(doc, logs)
    cli_obj.add_funcs(store.funcs)
    cli_obj.parse()
    store.add_cli(cli_obj)
    return cli_obj

def logger(name=None, loggers=None, filefmt='%Y-%m-%d_%H-%M-%S', datefmt='%H:%M:%S', loglvl=logging.INFO, formatter=None):
    if formatter:
        fmt = formatter
    else:
        fmt = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt=datefmt)
        
    if not loggers and store.funcs and not name:
        log_obj = log_handler.Logger(os.path.basename(inspect.stack()[-1].filename)[:-3], list(store.funcs.keys()), filefmt, loglvl, fmt)
    elif not loggers and store.funcs and name:
        log_obj = log_handler.Logger(name, list(store.funcs.keys()), filefmt, loglvl, fmt)
    else:
        log_obj = log_handler.Logger(name, loggers, filefmt, loglvl, fmt)
    store.add_log(log_obj)
    return log_obj.loggers