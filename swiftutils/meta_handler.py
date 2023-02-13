
from swiftutils.cli_handler import CLI
from swiftutils.log_handler import Logger
import inspect, os, logging
from pathlib import Path


class Utils:
    '''internal object for storing function dictionary'''
    def __init__(self):
        self.funcs = {}
        self.cli = None
        self.log = None
    
    def add_func(self, func):
        '''adds a function to the function dictionary'''
        names = inspect.getfullargspec(func).args # collect arg names
        types = list(inspect.getfullargspec(func).annotations.values()) # collect types of args

        # update dictionary 
        if func.__doc__:
            self.funcs.update({func.__name__: (func, names, types, func.__doc__)})
        else:
            self.funcs.update({func.__name__: (func, names, types)})

    def add_cli(self, desc, logs):
        '''adds a cli object to the store'''
        # it should also push to logger?
        
        if self.log:
            self.cli = CLI(desc, logs, self.log)
        else:
            self.cli = CLI(desc, logs)
        self.cli.add_funcs(self.funcs)
        self.cli.parse()
        return self.cli
    
    def add_log(self, name, loggers, loglvl, filename, filepath, filefmt, fhandler, filecap, filetimeout, file, streamfmt, shandler, stream, warn, cli):
        '''adds a logger object to the store'''
        # it should also push to cli?


        # if check for filepath must be inside function because filename is not initialized
        if self.cli:
            cli = True

        # if check for filepath must be inside function because filename is not initialized
        if not filepath:
            filepath = os.path.join('logs', name, f'{filename}.log')

        # check if log path parent directory has been initialized
        if not os.path.exists(Path(filepath).parent):
            os.makedirs(Path(filepath).parent) # make parent directory tree for given filepath

        # if check for handler must be inside function because filename is not initialized
        if not fhandler:
            fhandler = logging.FileHandler(filepath, 'w')

        # if check for loggers must be inside function because func keys will be empty at initialization
        if not loggers and self.funcs:
            self.log = Logger(name, list(self.funcs.keys()), loglvl, filename, filepath, filefmt, fhandler, filecap, filetimeout, file, streamfmt, shandler, stream, warn, cli)
        else:
            self.log = Logger(name, loggers, loglvl, filename, filepath, filefmt, fhandler, filecap, filetimeout, file, streamfmt, shandler, stream, warn, cli)
        return self.log 