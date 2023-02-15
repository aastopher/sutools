import inspect, os, logging, datetime
from swiftutils import meta_handler


utils = meta_handler.Utils()

def add(func):
    '''add function to store'''
    utils.add_func(func)
    return func

def cli(desc = None, logs = False, loggers = None):
    '''init cli and store'''
    cli_obj = utils.add_cli(desc, logs, loggers)
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
           stream = False,
           warn = False,
           cli = False):
    '''init logger object and store'''
    log_obj = utils.add_log(name, loggers, loglvl, filename, filepath, filefmt, fhandler, filecap, filetimeout, file, streamfmt, shandler, stream, warn, cli)
    return log_obj

def log():
    return utils.log.loggers