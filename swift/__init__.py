from swift import cli_handler
from swift import log_handler
from swift import meta_handler

import inspect, os

store = meta_handler.Bucket()

def add(func):
    store.add_func(func)
    return func

def cli(doc=None, logs=True):
    if store.log:
        cli_obj = cli_handler.CLI(doc, logs, store.log.loggers)
    else:
        cli_obj = cli_handler.CLI(doc, logs)
    cli_obj.add_funcs(store.funcs)
    cli_obj.parse()
    store.add_cli(cli_obj)
    return cli_obj

def logger(log_name=None, loggers=None):
    if not loggers and store.funcs and not log_name:
        log_obj = log_handler.Logger(os.path.basename(inspect.stack()[-1].filename)[:-3], list(store.funcs.keys()))
    elif not loggers and store.funcs and log_name:
        log_obj = log_handler.Logger(log_name, list(store.funcs.keys()))
    else:
        log_obj = log_handler.Logger(log_name, loggers)
    store.add_log(log_obj)
    return log_obj.loggers