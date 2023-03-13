from unittest.mock import patch, Mock
from io import StringIO
import sys, inspect, logging, argparse, pytest
from sutools import cli_handler, log_handler, meta_handler


#### Fixtures
@pytest.fixture
def mock_atexit_register(monkeypatch):
    mock_atexit_register = Mock()
    monkeypatch.setattr(log_handler.atexit, "register", mock_atexit_register)
    return mock_atexit_register


# Test 1: this should test passing in a cli description
def test_cli_desc(capsys, monkeypatch):

    def func_test():
        pass

    store = meta_handler.Bucket()
    store.add_func(func_test)

    expected = "Test CLI"
    cli_obj = cli_handler.CLI(expected, False)
    cli_obj.add_funcs(store.funcs)

    # patch sys.exit() so it doesn't stop the test
    monkeypatch.setattr(sys, 'exit', lambda x: None)

    # insert a value for self.input to test with
    cli_obj.input = cli_obj.parser.parse_args(["-h"])
    assert cli_obj.parser.description == expected  # check description value directly

    # call the parse method and capture the output with capsys
    cli_obj.parse()
    captured = capsys.readouterr()

    assert expected in captured.out

            
# Test 2: this should test passing a 
# boolean to logs to turn logging on
def test_cli_logs_on(capsys, monkeypatch, mock_atexit_register):
    expected = "test log"

    def func_test():
        log_obj.loggers.func_test.info(expected)
        return expected

    store = meta_handler.Bucket()
    store.add_func(func_test)

    log_obj = log_handler.Logger(
        'test_logger', 
        list(store.funcs.keys()), 
        logging.INFO, 
        None, None, None, None, None, None, 
        False, 
        logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'), 
        logging.StreamHandler(sys.stdout), 
        stream=True
    )

    # patch the input namespace with the desired command
    namespace = argparse.Namespace(command='func_test')

    with patch('sutools.cli_handler.argparse.ArgumentParser.parse_args', return_value=namespace):
        cli_obj = cli_handler.CLI('description', True, log_obj=log_obj)
        cli_obj.add_funcs(store.funcs)
        
        # patch the sys.exit function so it doesn't exit the interpreter
        monkeypatch.setattr(sys, 'exit', lambda *args: None)

        cli_obj.parse()

    captured = capsys.readouterr()

    assert expected in captured.out
    
# Test 3: this should test passing a 
# boolean to logs to turn logging off (i.e. 51)
def test_cli_logs_off(capsys, monkeypatch, mock_atexit_register):
    def func_test():
        log_obj.loggers.func_test.info('fail')
        print('pass')

    store = meta_handler.Bucket()
    store.add_func(func_test)

    log_obj = log_handler.Logger(
        'test_logger',
        list(store.funcs.keys()),
        logging.INFO,
        None, None, None, None, None, None,
        False,
        logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'),
        logging.StreamHandler(sys.stdout),
        stream=True
    )

    cli_obj = cli_handler.CLI('description', False, log_obj=log_obj)
    cli_obj.add_funcs(store.funcs)

    # patch the sys.exit function so it doesn't exit the interpreter
    monkeypatch.setattr(sys, 'exit', lambda *args: None)

    # patch the input namespace with the desired command
    namespace = argparse.Namespace(command='func_test')

    # patch the parse_args() method to return the patched namespace
    monkeypatch.setattr(cli_handler.argparse.ArgumentParser, 'parse_args', lambda self: namespace)

    cli_obj.parse()  # call the parse() method

    captured = capsys.readouterr()

    assert 'pass' in captured.out and 'fail' not in captured.out


# Test 4: this should test passing a logger object 
# (if a log_obj is passed in there should be loggers in the log property)
def test_cli_log_obj(mock_atexit_register):
    expected = ['logger1','logger2','logger3']

    log_obj = log_handler.Logger(
            'test_logger', 
            expected, 
            logging.INFO, 
            None, None, None, None, None, None, 
            False, 
            logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'), 
            logging.StreamHandler(sys.stdout), 
            stream=True
            )

    cli_obj = cli_handler.CLI('description', True, log_obj=log_obj)
    assert all(item in cli_obj.log.__dict__ for item in expected)

# Test 5: this should test adding references of functions 
# for to the cli to run (a dictionary of functions should be provided 
# then the cli should be tested to use those functions)
def test_cli_add_funcs(capsys, monkeypatch):

    def func_test(x : int, y : int , c : str = '-') -> int:
        pass

    expected = func_test.__name__

    # patch the input namespace with the desired command
    namespace = argparse.Namespace(command='func_test', help=True, x=1, y=2, c='+')

    with patch('sutools.cli_handler.argparse.ArgumentParser.parse_args', return_value=namespace):
        cli_obj = cli_handler.CLI('description', False)
        store = meta_handler.Bucket()
        store.add_func(func_test)
        cli_obj.add_funcs(store.funcs)
        
        # patch the sys.exit function so it doesn't exit the interpreter
        monkeypatch.setattr(sys, 'exit', lambda *args: None)

        cli_obj.parse()

    assert expected in cli_obj.parser.format_help()