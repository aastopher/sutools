from swift import cli_handler
from swift import log_handler
from swift import func_store

import inspect, os

store = func_store.Funcs()
# cli_obj = None
# log_obj = None

def add(func):
    store.add(func)
    return func

def cli(doc):
    cli_obj = cli_handler.Init(doc)
    cli_obj.add_funcs(store.funcs)
    cli_obj.parse()
    return cli_obj

def logger(log_name=None, loggers=None):
    if not loggers and store.funcs and not log_name:
        log_obj = log_handler.Init(os.path.basename(inspect.stack()[-1].filename)[:-3], store.funcs.keys())
    elif not loggers and store.funcs and log_name:
        log_obj = log_handler.Init(log_name, store.funcs.keys())
    else:
        log_obj = log_handler.Init(log_name, loggers)
    return log_obj


# DL = DeepLogger('connection',['decrypt','socket','connect'])
# decryptLogger = DL.getLogger('decrypt')
# socketLogger = DL.getLogger('socket')
# connectLogger = DL.getLogger('connect')

# print(os.path.basename(inspect.stack()[-1].filename)[:-3])