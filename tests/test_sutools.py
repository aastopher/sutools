from unittest.mock import patch, Mock, mock_open
import inspect, pytest, sys, argparse, logging
import sutools as su


#### Fixtures
@pytest.fixture
def mock_os(monkeypatch):
    mock_os = Mock()
    mock_os.makedirs.side_effect = lambda path: None
    monkeypatch.setattr(su, "os", mock_os)
    return mock_os


@pytest.fixture
def mock_atexit_register(monkeypatch):
    mock_atexit_register = Mock()
    monkeypatch.setattr(su.log_handler.atexit, "register", mock_atexit_register)
    return mock_atexit_register


# #### Methods


# Test 1: this should test the register decorator from sutools
# the result should be that the su.store contains a
# none empty dictionary for the func property
def test_register():
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

    @su.register
    def func_test(x: int, y: int) -> int:
        """this is a test function"""
        return x + y

    names = inspect.getfullargspec(func_test).args  # collect arg names
    types = inspect.getfullargspec(func_test).annotations  # collect types of args
    defaults = _get_defaults(func_test)
    desc = func_test.__doc__

    expected_dict = {func_test.__name__: (func_test, names, types, defaults, desc)}

    assert expected_dict == su.store.funcs


# Test 2: this should test the cli from sutools
# the result should be that the cli property is not None in su.store
# the cli object should contain commands for any registered functions
def test_cli(mock_atexit_register, monkeypatch):
    # patch the input namespace with the desired command
    namespace = argparse.Namespace(command="", help=True)

    with patch(
        "sutools.cli_handler.argparse.ArgumentParser.parse_args", return_value=namespace
    ):
        # patch the sys.exit function so it doesn't exit the interpreter during the test
        monkeypatch.setattr(sys, "exit", lambda *args: None)

        su.cli()

    assert su.store.cli is not None


# Test 3: thisfunc_test should test the logger from sutools
# the result should be that the log property is no None in su.store
# the log object should also contain a property loggers with
# the names of the loggers passed in to loggers property in the logger
def test_logger(mock_atexit_register, monkeypatch):
    with patch("builtins.open", mock_open()) as mock_file:
        monkeypatch.setattr(su.os, "makedirs", lambda *args, **kwargs: None)
        su.logger(filepath="path")

    assert su.store.log is not None
    assert mock_file.called


def test_logger_path(mock_os, mock_atexit_register):
    expected_filename = "test_file.log"
    mock_filepath = "/logs/test_name"

    mock_os.makedirs = Mock()
    mock_os.path.exists.return_value = False

    with patch("builtins.open", mock_open()):
        su.logger(
            loggers=["logger1", "logger2", "logger3"],
            filepath=mock_filepath,
            fhandler=logging.FileHandler(
                f"{mock_filepath}/{expected_filename}", "w", encoding="locale"
            ),
        )

        assert su.store.log is not None
        assert mock_os.path.join.call_args[0][0] == mock_filepath
        mock_os.makedirs.assert_called_once()


def test_logger_cloggers(mock_os, mock_atexit_register):
    expected = ["logger1", "logger2", "logger3"]

    with patch("builtins.open", mock_open()):
        su.logger(
            loggers=expected,
            fhandler=logging.FileHandler(
                "test/folder/test_log.log", "w", encoding="locale"
            ),
        )

    assert su.store.log is not None
    assert all(name in vars(su.store.log.loggers) for name in expected)


# Test 4: this should test the log helper function
# the should return a namespace of loggers defined
# in the log object in the su.store
def test_log(mock_os, mock_atexit_register):
    @su.register
    def func_test():
        pass

    with patch("builtins.open", mock_open()):
        su.logger(
            fhandler=logging.FileHandler(
                "test/folder/test_log.log", "w", encoding="locale"
            )
        )
    assert "func_test" in vars(su.log()).keys()


#### Integration


# Test 5: this should test integrations for cli and logger compatibility
# this should init both a logger and a cli as well as
# at least one registered test function.
# the result should be that the log statements in the cli are
# logged if the cli has logs set to True
def test_logger_cli(capsys, mock_os, mock_atexit_register, monkeypatch):
    expected_cli = "Test CLI"
    expected_log = "test log"

    @su.register
    def func_test():
        su.log().func_test.info(expected_log)

    with patch("builtins.open", mock_open()):
        su.logger(
            file=False,
            fhandler=logging.FileHandler(
                "test/folder/test_log.log", "w", encoding="locale"
            ),
            stream=True,
            shandler=logging.StreamHandler(sys.stdout),
        )

    # patch the input namespace with the desired command
    namespace = argparse.Namespace(command="func_test")

    with patch(
        "sutools.cli_handler.argparse.ArgumentParser.parse_args", return_value=namespace
    ):
        # patch the sys.exit function so it doesn't exit the interpreter during the test
        monkeypatch.setattr(sys, "exit", lambda *args: None)

        # call the cli() function to execute the desired command and capture the log output
        su.cli(desc=expected_cli, logs=True)

    captured = capsys.readouterr()

    assert expected_log in captured.out
