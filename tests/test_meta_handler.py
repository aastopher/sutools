from unittest.mock import Mock
import logging, pytest
from sutools import meta_handler, cli_handler, log_handler

#### Fixtures
@pytest.fixture
def mock_atexit_register(monkeypatch):
    mock_atexit_register = Mock()
    monkeypatch.setattr(log_handler.atexit, "register", mock_atexit_register)
    return mock_atexit_register

# Test 1: this should test adding references of functions 
# for to the cli to run (a dictionary of functions should be provided 
# then the cli should be tested to use those functions)
def test_add_func():

    def func_test():
        pass

    store = meta_handler.Bucket()
    store.add_func(func_test)
    assert 'func_test' in store.funcs.keys()

# Test 2: this should test the add_cli method 
# this the store should contain a cli obj
def test_add_cli():
    store = meta_handler.Bucket()
    cli_obj = cli_handler.CLI('desc', False)
    store.add_cli(cli_obj)
    assert isinstance(store.cli, cli_handler.CLI)

# Test 2: this should test the parse method 
# this is called after functions are added to be called as a command
def test_add_log(mock_atexit_register):
    store = meta_handler.Bucket()

    log_obj = log_handler.Logger(
                'test_logger', 
                ['logger1','logger2','logger3'], 
                logging.INFO, 
                None, None, None, None, None, None, 
                False, 
                logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'), 
                logging.StreamHandler(), 
                stream=True
              )

    store.add_log(log_obj)
    assert isinstance(store.log, log_handler.Logger)

