from unittest.mock import patch
from io import StringIO, FileIO
import os, sys, inspect, logging, datetime
sys.path.append("../")
from sutools import cli_handler, log_handler
from pathlib import Path


# Test 1: this should test passing in a cli description
def test_cli_desc(monkeypatch):

    def test_func():
        pass
    
    func_dict = {}
    names = inspect.getfullargspec(test_func).args # collect arg names
    types = list(inspect.getfullargspec(test_func).annotations.values()) # collect types of args
    func_dict.update({test_func.__name__: (test_func, names, types)})

    expected = "Test CLI"
    cli_obj = cli_handler.CLI(expected, False)
    cli_obj.add_funcs(func_dict)

    # mock sys.exit() so it doesn't stop the test
    monkeypatch.setattr(sys, 'exit', lambda x: None)

    # mock the parse method
    def mock_parse(self):
        self.input = self.parser.parse_args(["-h"])
        assert self.parser.description == expected  # check description value directly
        return

    monkeypatch.setattr(cli_handler.CLI, "parse", mock_parse)

    with patch("sys.stdout", new=StringIO()) as output:
        cli_obj.parse()  # call the mocked parse method
        assert expected == output.getvalue().split('\n')[2].strip()  # check output value

# Test 2: this should test passing a 
# boolean to logs to turn logging on
def test_cli_logs_on(capsys, monkeypatch):

    expected = "test log"

    def func_test():
        log_obj.loggers.func_test.info(expected)

    func_dict = {func_test.__name__ : (func_test, [], [])}

    log_obj = log_handler.Logger(
            'test_logger', 
            list(func_dict.keys()), 
            logging.INFO, 
            None, None, None, None, None, None, 
            False, 
            logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'), 
            logging.StreamHandler(sys.stdout), 
            stream=True
            )

    cli_obj = cli_handler.CLI('description', True, log_obj=log_obj)
    cli_obj.add_funcs(func_dict)

    # mock sys.exit() so it doesn't stop the test
    monkeypatch.setattr(sys, 'exit', lambda x: None)

    # mock the parse method
    def mock_parse(self):
        self.input = self.parser.parse_args(["func_test"])

        if self.input.command:
            func_tup = self.func_dict[self.input.command] # retrieve function and arg names for given command
            func, arg_names = func_tup[0], func_tup[1] # unpack just the args and function
            args = [getattr(self.input, arg) for arg in arg_names] # collect given args from namespace
            func(*args) # run function with given args
        return

    monkeypatch.setattr(cli_handler.CLI, "parse", mock_parse)

    cli_obj.parse()  # call the mocked parse method

    captured = capsys.readouterr()

    assert expected in captured.out

# Test 3: this should test passing a 
# boolean to logs to turn logging off (i.e. 51)
def test_cli_logs_on(capsys, monkeypatch):

    def func_test():
        log_obj.loggers.func_test.info('fail')
        print('pass')

    func_dict = {func_test.__name__ : (func_test, [], [])}

    log_obj = log_handler.Logger(
            'test_logger', 
            list(func_dict.keys()), 
            logging.INFO, 
            None, None, None, None, None, None, 
            False, 
            logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'), 
            logging.StreamHandler(sys.stdout), 
            stream=True
            )

    cli_obj = cli_handler.CLI('description', False, log_obj=log_obj)
    cli_obj.add_funcs(func_dict)

    # mock sys.exit() so it doesn't stop the test
    monkeypatch.setattr(sys, 'exit', lambda x: None)

    # mock the parse method
    def mock_parse(self):
        self.input = self.parser.parse_args(["func_test"])

        if self.input.command:
            func_tup = self.func_dict[self.input.command] # retrieve function and arg names for given command
            func, arg_names = func_tup[0], func_tup[1] # unpack just the args and function
            args = [getattr(self.input, arg) for arg in arg_names] # collect given args from namespace
            func(*args) # run function with given args
        return

    monkeypatch.setattr(cli_handler.CLI, "parse", mock_parse)

    cli_obj.parse()  # call the mocked parse method

    captured = capsys.readouterr()

    assert 'pass' in captured.out and 'fail' not in captured.out


# Test 4: this should test passing a logger object 
# (if a log_obj is passed in there should be loggers in the log property)
def test_cli_log_obj():
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
def test_cli_add_funcs(monkeypatch):

    def func_test():
        print('test func')

    expected = func_test.__name__
    cli_obj = cli_handler.CLI('description', False)
    cli_obj.add_funcs({func_test.__name__ : (func_test, [], [])})

    # mock sys.exit() so it doesn't stop the test
    monkeypatch.setattr(sys, 'exit', lambda x: None)

    # mock the parse method
    def mock_parse(self, arg):
        self.input = self.parser.parse_args(["func_test","-h"])
        return

    monkeypatch.setattr(cli_handler.CLI, "parse", mock_parse)

    with patch("sys.stdout", new=StringIO()) as output:
        cli_obj.parse(None)  # call the mocked parse method
        assert expected == output.getvalue().split('\n')[0].split(' ')[2]  # check output value

