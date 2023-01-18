import inspect

class Bucket:
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

    def add_cli(self, cli_obj):
        '''adds a cli object to the store'''
        self.cli = cli_obj
    
    def add_log(self, log_obj):
        '''adds a logger object to the store'''
        self.cli = log_obj