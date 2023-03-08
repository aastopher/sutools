from unittest.mock import patch
from io import StringIO
import inspect
import sutools as su

#### Methods

# Test 1: this should test the register decorator from sutools
# the result should be that the su.store contains a 
# none empty dictionary for the func property
def test_register():

    def _get_defaults(func):
        '''helper function to collect default func args'''

        # get the signature of the function
        sig = inspect.signature(func)

        # collect a dictionary of default argument values
        defaults = {}
        for param in sig.parameters.values():
            if param.default is not inspect.Parameter.empty:
                defaults[param.name] = param.default

        return defaults

    @su.register
    def func_test(x: int, y: int) -> int:
        '''this is a test function'''
        return x + y
    
    names = inspect.getfullargspec(func_test).args # collect arg names
    types = inspect.getfullargspec(func_test).annotations # collect types of args
    defaults = _get_defaults(func_test)
    desc = func_test.__doc__

    expected_dict = {func_test.__name__: (func_test, names, types, defaults, desc)}
    
    assert expected_dict == su.store.funcs


# Test 2: this should test the cli from sutools
# the result should be that the cli property is not None in su.store
# the cli object should contain commands for any registered functions
def test_cli():

    su.cli()
    assert su.store.cli != None

# Test 3: this should test the logger from sutools
# the result should be that the log property is no None in su.store
# the log object should also contain a property loggers with 
# the names of the loggers passed in to loggers property in the logger
def test_logger():
    su.logger()
    assert su.store.log != None

# Test 4: this should test the log helper function
# the should return a namespace of loggers defined 
# in the log object in the su.store
def test_log():
    
    @su.register
    def func_test():
        pass

    assert 'func_test' in vars(su.log()).keys()

#### Integrations

# Test 5: this should test integrations for cli and logger compatibility
# this should init both a logger and a cli as well as 
# at least one registered test function.
# the result should be that the log statements in the cli are 
# logged if the cli has logs set to True
def test_logger_cli():
    pass