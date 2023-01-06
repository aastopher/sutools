import inspect

class Funcs:
    '''internal object for storing function dictionary'''
    def __init__(self):
        self.funcs = {}
    
    def add(self, func):
        names = inspect.getfullargspec(func).args # collect arg names
        types = list(inspect.getfullargspec(func).annotations.values()) # collect types of args

        # update dictionary 
        if func.__doc__:
            self.funcs.update({func.__name__: (func, names, types, func.__doc__)})
        else:
            self.funcs.update({func.__name__: (func, names, types)})