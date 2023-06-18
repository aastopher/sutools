import inspect


class Store:
    """internal object for storing function dictionary"""

    def __init__(self):
        self.funcs = {}  # init function registration dictionary
        self.cli = None  # init cli object store
        self.log = None  # init logger object store

    def add_func(self, func):
        """registers a function to the function dictionary"""
        names = inspect.getfullargspec(func).args  # collect arg names
        types = inspect.getfullargspec(func).annotations  # collect types of args
        defaults = self._get_defaults(func)
        desc = None
        variadic = False

        # if docstring exists and no description defined set desc
        if func.__doc__:
            desc = func.__doc__

        # collect function signature to check if variadic [args, kwargs]
        signature = inspect.signature(func)
        for name, param in signature.parameters.items():
            param_kind = signature.parameters[name].kind
            variadic = param_kind in [inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD]
            # correct names and types definition
            if variadic:
                names.append(str(param))
                types = {}

        # define function meta info
        func_meta = {'func':func, 
                    'names':names, 
                    'types':types, 
                    'defaults':defaults, 
                    'desc':desc, 
                    'variadic':variadic}
        
        # update function in store
        self.funcs.update({func.__name__: func_meta})

    def add_cli(self, cli_obj):
        """adds a cli object to the store"""
        self.cli = cli_obj

    def add_log(self, log_obj):
        """adds a logger object to the store"""
        self.log = log_obj

    @staticmethod
    def _get_defaults(func):
        """helper function to collect default func args"""

        # get the signature of the function
        sig = inspect.signature(func)

        # collect a dictionary of default argument values
        defaults = {}
        for param in sig.parameters.values():
            if param.default is not inspect.Parameter.empty:
                defaults[param.name] = param.default

        return defaults
