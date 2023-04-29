from unittest.mock import patch, Mock
import sys, logging, argparse, pytest, asyncio
from sutools import cli_handler, log_handler, meta_handler


#### Fixtures
@pytest.fixture
def mock_atexit_register(monkeypatch):
    mock_atexit_register = Mock()
    monkeypatch.setattr(log_handler.atexit, "register", mock_atexit_register)
    return mock_atexit_register


#### Tests


def test_cli_desc(capsys, monkeypatch):
    def func_test(
        test, test2: str, test3: str = "test", test4="test2", teest4: str = "test"
    ) -> str:
        pass # pass since we are only testing the function description
    
    store = meta_handler.Bucket()
    store.add_func(func_test)

    expected = "Test CLI"
    cli_obj = cli_handler.CLI(expected, False)
    cli_obj.add_funcs(store.funcs)

    monkeypatch.setattr(sys, "exit", lambda x: None)

    cli_obj.input = cli_obj.parser.parse_args(["-h"])
    assert cli_obj.parser.description == expected

    cli_obj.parse()
    captured = capsys.readouterr()

    assert expected in captured.out


def test_cli_logs_on(capsys, monkeypatch, mock_atexit_register):
    expected = "test log"

    def func_test():
        log_obj.loggers.func_test.info(expected)
        return expected

    store = meta_handler.Bucket()
    store.add_func(func_test)

    log_obj = log_handler.Logger(
        "test_logger",
        list(store.funcs.keys()),
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
        logging.StreamHandler(sys.stdout),
        stream=True,
    )

    namespace = argparse.Namespace(command="func_test")

    with patch(
        "sutools.cli_handler.argparse.ArgumentParser.parse_args", return_value=namespace
    ):
        cli_obj = cli_handler.CLI("description", True, log_obj=log_obj)
        cli_obj.add_funcs(store.funcs)

        monkeypatch.setattr(sys, "exit", lambda *args: None)

        cli_obj.parse()

    captured = capsys.readouterr()

    assert expected in captured.out


def test_cli_logs_off(capsys, monkeypatch, mock_atexit_register):
    def func_test():
        log_obj.loggers.func_test.info("fail")
        print("pass")

    store = meta_handler.Bucket()
    store.add_func(func_test)

    log_obj = log_handler.Logger(
        "test_logger",
        list(store.funcs.keys()),
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
        logging.StreamHandler(sys.stdout),
        stream=True,
    )

    cli_obj = cli_handler.CLI("description", False, log_obj=log_obj)
    cli_obj.add_funcs(store.funcs)

    monkeypatch.setattr(sys, "exit", lambda *args: None)

    namespace = argparse.Namespace(command="func_test")

    monkeypatch.setattr(
        cli_handler.argparse.ArgumentParser, "parse_args", lambda self: namespace
    )

    cli_obj.parse()

    captured = capsys.readouterr()

    assert "pass" in captured.out and "fail" not in captured.out


def test_cli_log_obj(mock_atexit_register):
    expected = ["logger1", "logger2", "logger3"]

    log_obj = log_handler.Logger(
        "test_logger",
        expected,
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
        logging.StreamHandler(sys.stdout),
        stream=True,
    )

    cli_obj = cli_handler.CLI("description", True, log_obj=log_obj)
    assert all(item in cli_obj.log.__dict__ for item in expected)


def test_cli_add_funcs(capsys, monkeypatch):
    def func_test(x: int, y: int, c: str = "-") -> int:
        pass # pass since we are only testing the function is added to store

    expected = func_test.__name__

    namespace = argparse.Namespace(command="func_test", help=True, x=1, y=2, c="+")

    with patch(
        "sutools.cli_handler.argparse.ArgumentParser.parse_args", return_value=namespace
    ):
        cli_obj = cli_handler.CLI("description", False)
        store = meta_handler.Bucket()
        store.add_func(func_test)
        cli_obj.add_funcs(store.funcs)

        monkeypatch.setattr(sys, "exit", lambda *args: None)

        cli_obj.parse()

    assert expected in cli_obj.parser.format_help()

def test_async_func(capsys, monkeypatch, mock_atexit_register):
    async def func_test():
        await asyncio.sleep(0.1)
        print('pass')

    store = meta_handler.Bucket()
    store.add_func(func_test)

    log_obj = log_handler.Logger(
        "test_logger",
        list(store.funcs.keys()),
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
        logging.StreamHandler(sys.stdout),
        stream=True,
    )

    cli_obj = cli_handler.CLI("description", False, log_obj=log_obj)
    cli_obj.add_funcs(store.funcs)

    monkeypatch.setattr(sys, "exit", lambda *args: None)

    namespace = argparse.Namespace(command="func_test")

    monkeypatch.setattr(
        cli_handler.argparse.ArgumentParser, "parse_args", lambda self: namespace
    )

    cli_obj.parse()

    captured = capsys.readouterr()

    assert "pass" in captured.out
