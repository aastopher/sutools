import inspect

class Bucket:
    '''internal object for storing function dictionary'''
    def __init__(self):
        self.funcs = {} # init function registration dictionary
        self.cli = None # init cli object store
        self.log = None # init logger object store
    
    def add_func(self, func):
        '''registers a function to the function dictionary'''
        names = inspect.getfullargspec(func).args # collect arg names
        types = inspect.getfullargspec(func).annotations # collect types of args

        # update function dictionary 
        if func.__doc__:
            self.funcs.update({func.__name__: (func, names, types, func.__doc__)})
        else:
            self.funcs.update({func.__name__: (func, names, types)})


    def add_cli(self, cli_obj):
        '''adds a cli object to the store'''
        self.cli = cli_obj
    
    def add_log(self, log_obj):
        '''adds a logger object to the store'''
        self.log = log_obj