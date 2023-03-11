from unittest.mock import patch, Mock
from io import StringIO
import inspect, pytest, sys, argparse, logging
import sutools as su

#### Fixtures
@pytest.fixture
def mock_atexit_register(monkeypatch):
    mock_atexit_register = Mock()
    monkeypatch.setattr(su.log_handler.atexit, "register", mock_atexit_register)
    return mock_atexit_register

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
def test_cli(mock_atexit_register, monkeypatch):
    # patch the input namespace with the desired command
    namespace = argparse.Namespace(command='' ,help=True)

    with patch('sutools.cli_handler.argparse.ArgumentParser.parse_args', return_value=namespace):

        # patch the sys.exit function so it doesn't exit the interpreter during the test
        monkeypatch.setattr(sys, 'exit', lambda *args: None)

        su.cli()

    assert su.store.cli != None

# Test 3: thisfunc_test should test the logger from sutools
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

#### Integration

# Test 5: this should test integrations for cli and logger compatibility
# this should init both a logger and a cli as well as 
# at least one registered test function.
# the result should be that the log statements in the cli are 
# logged if the cli has logs set to True
def test_logger_cli(capsys, mock_atexit_register, monkeypatch):
    expected_cli = "Test CLI"
    expected_log = 'test log'

    @su.register
    def func_test():
        su.log().func_test.info(expected_log)

    su.logger(stream = True, shandler = logging.StreamHandler(sys.stdout))

    # patch the input namespace with the desired command
    namespace = argparse.Namespace(command='func_test')

    with patch('sutools.cli_handler.argparse.ArgumentParser.parse_args', return_value=namespace):

        # patch the sys.exit function so it doesn't exit the interpreter during the test
        monkeypatch.setattr(sys, 'exit', lambda *args: None)

        # call the cli() function to execute the desired command and capture the log output
        su.cli(desc=expected_cli, logs=True)
 
    captured = capsys.readouterr()

    assert expected_log in captured.out


