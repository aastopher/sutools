from unittest.mock import Mock
import logging, pytest
from sutools import meta_handler, cli_handler, log_handler

#### Fixtures


# Define a fixture that monkeypatches the atexit module's register function
# with a Mock object, so that we can test if it gets called correctly
@pytest.fixture
def mock_atexit_register(monkeypatch):
    mock_atexit_register = Mock()
    monkeypatch.setattr(log_handler.atexit, "register", mock_atexit_register)
    return mock_atexit_register


### Tests


# Define a test function for the add_func method of the meta_handler.Bucket class
def test_add_func():
    def func_test1():
        pass

    def func_test2():
        pass

    expected = ["func_test1", "func_test2"]
    # Create a new meta_handler.Bucket object
    store = meta_handler.Bucket()

    # Add test functions to the store
    store.add_func(func_test1)
    store.add_func(func_test2)

    # Assert that the function was added correctly
    assert all(item in store.funcs for item in expected)


# Define a test function for the add_cli method of the meta_handler.Bucket class
def test_add_cli():
    # Create a new meta_handler.Bucket object
    store = meta_handler.Bucket()

    # Create a new cli_handler.CLI object
    cli_obj = cli_handler.CLI("desc", False)

    # Add the cli_handler.CLI object to the store
    store.add_cli(cli_obj)

    # Assert that the CLI object was added correctly
    assert isinstance(store.cli, cli_handler.CLI)


# Define a test function for the add_log method of the meta_handler.Bucket class
def test_add_log(mock_atexit_register):
    # Create a new meta_handler.Bucket object
    store = meta_handler.Bucket()

    # Create a new log_handler.Logger object
    log_obj = log_handler.Logger(
        "test_logger",
        ["logger1", "logger2", "logger3"],
        logging.INFO,
        None,
        None,
        None,
        None,
        None,
        None,
        False,
        logging.Formatter(
            "%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
        ),
        logging.StreamHandler(),
        stream=True,
    )

    # Add the log_handler.Logger object to the store
    store.add_log(log_obj)

    # Assert that the Logger object was added correctly
    assert isinstance(store.log, log_handler.Logger)
