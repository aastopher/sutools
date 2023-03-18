from unittest.mock import patch, mock_open, MagicMock, Mock, call
import logging, sys, datetime, os, time
from sutools import log_handler
from freezegun import freeze_time
import pytest


### FIXTURES
@pytest.fixture
def mock_os(monkeypatch):
    mock_os = Mock()
    monkeypatch.setattr(log_handler, "os", mock_os)
    return mock_os


@pytest.fixture
def mock_atexit_register(monkeypatch):
    mock_atexit_register = Mock()
    monkeypatch.setattr(log_handler.atexit, "register", mock_atexit_register)
    return mock_atexit_register


### TESTS


# Test 1: tests name, file, and stream options in log_handler.Logger()
def test_name_file_stream(mock_atexit_register):
    expected = "test_name"
    log_obj = log_handler.Logger(
        expected,
        ["log"],
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

    assert expected == log_obj.name


# Test 2: tests the logger option in log_handler.Logger()
def test_loggers(mock_atexit_register):
    expected = ["logger1", "logger2", "logger3"]
    log_obj = log_handler.Logger(
        "test name",
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

    assert all(item in log_obj.loggers.__dict__ for item in expected)


# Test 3: tests loglvl, shandler, and streamfmt options in log_handler.Logger()
def test_loglvl_shandler_streamfmt(capsys, mock_atexit_register):
    expected = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S"
    )

    def func_test():
        log_obj.loggers.log.debug("debug message")
        log_obj.loggers.log.info("info message")
        log_obj.loggers.log.warning("warning message")
        log_obj.loggers.log.error("error message")
        log_obj.loggers.log.critical("critical message")

    log_obj = log_handler.Logger(
        "test_logger",
        ["log"],
        logging.DEBUG,
        None,
        None,
        None,
        None,
        None,
        None,
        False,
        formatter,
        logging.StreamHandler(sys.stdout),
        stream=True,
    )

    func_test()
    captured = capsys.readouterr()
    assert all(level in captured.out for level in expected)

    with patch.object(log_obj.loggers.log.handlers[0].stream, "write") as mock_write:
        log_obj.loggers.log.handlers[0].setFormatter(formatter)
        log_time = datetime.datetime.now().strftime("%H:%M:%S")
        log_obj.loggers.log.info("Test log message")
        expected_msg = f"{log_time}, log INFO Test log message\n"
        assert expected_msg == mock_write.call_args_list[0][0][0]


# Test 4: tests filepath, filename, and fhandler options in log_handler.Logger()
def test_filepath_filename_fhandler(mock_atexit_register):
    expected_filename = "test_file.log"

    with patch("builtins.open", mock_open()) as mock_file:

        def func_test():
            log_obj.loggers.log.info("info msg")

        mock_filepath = "/logs/test_name"

        log_obj = log_handler.Logger(
            name="test_name",
            loggers=["log"],
            loglvl=logging.INFO,
            filename=expected_filename,
            filepath=mock_filepath,
            filefmt=logging.Formatter(
                "%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s",
                datefmt="%H:%M:%S",
            ),
            fhandler=logging.FileHandler(
                f"{mock_filepath}/{expected_filename}", "w", encoding="locale"
            ),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False,
        )

        func_test()

        # # check that the file was opened with the expected arguments
        expected_call = (f"{mock_filepath}/{expected_filename}", "w")
        actual_call = mock_file.mock_calls[0][1:2][0]
        assert expected_call == actual_call

        # verify that atexit.register called once
        mock_atexit_register.assert_called_once()


# Test 5: tests filefmt option in log_handler.Logger()
def test_filefmt(mock_atexit_register):
    filename = "test_file.log"
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S"
    )

    with patch("builtins.open", mock_open()):
        log_obj = log_handler.Logger(
            name="test_name",
            loggers=["log"],
            loglvl=logging.INFO,
            filename=filename,
            filepath="/logs/test_name",
            filefmt=formatter,
            fhandler=logging.FileHandler(
                f"/logs/test_name/{filename}", "w", encoding="locale"
            ),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False,
        )

        with patch.object(
            log_obj.loggers.log.handlers[0].stream, "write"
        ) as mock_write:
            log_obj.loggers.log.handlers[0].setFormatter(formatter)
            log_time = datetime.datetime.now().strftime("%H:%M:%S")
            log_obj.loggers.log.info("Test log message")
            expected_msg = f"{log_time}, log INFO Test log message\n"
            assert expected_msg == mock_write.call_args_list[0][0][0]

            # verify that atexit.register called once
            mock_atexit_register.assert_called_once()


# Test 6: this should test passing a file cap integer
# 5 for capping the log files to 5 files
def test_filecap(mock_os, mock_atexit_register):
    folder = "path/to/logs"
    filename = "test_file.log"
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S"
    )

    with patch("builtins.open", mock_open()):
        # mock the os functions used inside the cap method
        mock_os.path.getctime.return_value = 1646106476
        mock_os.listdir.return_value = ["file1.log", "file2.log", "file3.log"]

        # create an instance of the Logger class
        log_handler.Logger(
            name="test_name",
            loggers=["log"],
            loglvl=logging.INFO,
            filename=filename,
            filepath=folder,
            filefmt=formatter,
            fhandler=logging.FileHandler(
                f"{folder}/{filename}", "w", encoding="locale"
            ),
            filecap=2,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False,
        )

        # verify that os.path.join was called twice for each file with correct filename
        join_calls = [call[0][1] for call in mock_os.path.join.call_args_list]
        expected_files = ["file1.log", "file2.log", "file3.log"]
        assert all(filename in expected_files for filename in join_calls)
        assert mock_os.path.join.call_count == 6

        # verify that os.path.getctime was called once for each file
        assert mock_os.path.getctime.call_count == 3

        # verify that os.remove was called once
        mock_os.remove.assert_called_once

        # verify that os.listdir was called once
        mock_os.listdir.assert_called_once

        # verify that atexit.register called once
        mock_atexit_register.assert_called_once()


# Test 7: tests if filecap was turned on after logs generated
# forcing more than 1 file removed
def test_filecap_tomany(mock_os, mock_atexit_register):
    folder = "path/to/logs"
    filename = "test_file.log"
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S"
    )

    # create mock files with different creation times
    file1 = ("path/to/logs/file1.log", 1646106476)
    file2 = ("path/to/logs/file2.log", 1646192876)
    file3 = ("path/to/logs/file3.log", 1646279276)
    file4 = ("path/to/logs/file4.log", 1646365676)

    # create a list of mock files that exceeds the filecap
    mock_files = [file1, file2, file3, file4]

    with patch("builtins.open", mock_open()):
        # mock the os functions used inside the cap method
        mock_os.path.getctime.side_effect = [f[1] for f in mock_files]
        mock_os.listdir.return_value = [f[0].split("/")[-1] for f in mock_files]

        # create an instance of the Logger class with filecap set to 2
        log_handler.Logger(
            name="test_name",
            loggers=["log"],
            loglvl=logging.INFO,
            filename=filename,
            filepath=folder,
            filefmt=formatter,
            fhandler=logging.FileHandler(
                f"{folder}/{filename}", "w", encoding="locale"
            ),
            filecap=2,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False,
        )

        # verify that os.path.join was called twice for each file with correct filename
        join_calls = [call[0][1] for call in mock_os.path.join.call_args_list]
        expected_files = ["file1.log", "file2.log", "file3.log", "file4.log"]
        assert all(filename in expected_files for filename in join_calls)
        assert mock_os.path.join.call_count == 8

        # verify that os.path.getctime was called once for each file
        assert mock_os.path.getctime.call_count == 4

        # verify that os.remove was called for the files that exceeded the cap
        assert mock_os.remove.call_count == 2

        # verify that os.listdir was called once
        mock_os.listdir.assert_called_once()

        # verify that atexit.register called once
        mock_atexit_register.assert_called_once()


# Test 8: this should test passing a file timeout string
# define a timeout period by combining time unit characters
# with the desired integer for a specified time unit
# i.e. `(10m = 10 minute, 2h = 2 hours, ...)`
@freeze_time("2023-02-25 10:00:00")
def test_timeout(mock_os, mock_atexit_register):
    folder = "path/to/logs"
    filename = "test_file.log"
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S"
    )
    mock_files = [
        ("path/to/logs/file1.log", time.time() - 63072000),  # 2 years
        ("path/to/logs/file2.log", time.time() - 2592000),  # 30 days
        ("path/to/logs/file3.log", time.time() - 18000),  # 5 hours
        ("path/to/logs/file4.log", time.time() - 1800),  # 30 minutes
    ]

    time_units = {
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "o": "months",
        "y": "years",
    }

    for filetimeout, expected_removed_files in [
        ("1y", 1),
        ("1o", 1),
        ("30d", 1),
        ("5h", 2),
        ("30m", 3),
        ("1z", 0),
    ]:
        if filetimeout[-1] not in time_units:
            # assert that warnings.warn was called once with the correct message for an invalid time unit
            with patch("builtins.open", side_effect=mock_files), patch(
                "warnings.warn"
            ) as mock_warn:
                log_handler.Logger(
                    name="test_name",
                    loggers=["log"],
                    loglvl=logging.INFO,
                    filename=filename,
                    filepath=folder,
                    filefmt=formatter,
                    fhandler=logging.FileHandler(
                        f"{folder}/{filename}", "w", encoding="locale"
                    ),
                    filecap=None,
                    filetimeout=filetimeout,
                    file=True,
                    streamfmt=None,
                    shandler=None,
                    stream=False,
                )
                mock_warn.assert_called_once_with(
                    f"Invalid time unit: {filetimeout[-1]}", Warning
                )
        else:
            # mock the return values for os.path.getctime and os.listdir
            mock_os.path.getctime.side_effect = [f[1] for f in mock_files]
            mock_os.listdir.return_value = [os.path.basename(f[0]) for f in mock_files]

            with patch("builtins.open", side_effect=mock_files):
                # reset the call count for remove mock object
                mock_os.remove.call_count = 0

                log_handler.Logger(
                    name="test_name",
                    loggers=["log"],
                    loglvl=logging.INFO,
                    filename=filename,
                    filepath=folder,
                    filefmt=formatter,
                    fhandler=logging.FileHandler(
                        f"{folder}/{filename}", "w", encoding="locale"
                    ),
                    filecap=None,
                    filetimeout=filetimeout,
                    file=True,
                    streamfmt=None,
                    shandler=None,
                    stream=False,
                )

                # assert that os.listdir was called with the correct folder path
                mock_os.listdir.assert_called_once

                # assert that the correct logs were removed
                assert mock_os.remove.call_count == expected_removed_files


# Test 9: this should test the out method
# create a file in the filepath with file size of 0
# then run the out method
# the file should be removed
def test_out(mock_os, mock_atexit_register):
    folder = "path/to/logs/"
    filename = "test_file.log"
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S"
    )

    with patch("builtins.open", mock_open()):
        # create an instance of the Logger class
        log_obj = log_handler.Logger(
            name="test_name",
            loggers=["log"],
            loglvl=logging.INFO,
            filename=filename,
            filepath=folder,
            filefmt=formatter,
            fhandler=logging.FileHandler(
                f"{folder}/{filename}", "w", encoding="locale"
            ),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False,
        )

        ##### test file size 0 #####
        # mock the getsize() and remove() methods of the os.path module
        mock_os.path.getsize = MagicMock(return_value=0)
        mock_os.remove = MagicMock(return_value=None)

        # Call the out() method of the Logger object
        log_obj.out()

        # Verify that the getsize method was called once
        mock_os.path.getsize.assert_called_once_with(folder)
        # Verify that the remove method was not called
        mock_os.remove.assert_called_once_with(folder)

        ##### test file size 1 #####
        # mock the getsize() and remove() methods of the os.path module
        mock_os.path.getsize = MagicMock(return_value=1)
        mock_os.remove = MagicMock(return_value=None)

        # Call the out() method of the Logger object
        log_obj.out()

        # Verify that the getsize method was called once
        mock_os.path.getsize.assert_called_once_with(folder)

        # Verify that the remove method was not called
        mock_os.remove.assert_not_called()

        # verify that atexit.register called once
        mock_atexit_register.assert_called_once()


# Test 10: Test out method failing to remove file
def test_out_file_fail(capsys, mock_os, mock_atexit_register):
    folder = "path/to/logs/"
    filename = "test_file.log"
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S"
    )

    with patch("builtins.open", mock_open()):
        # create an instance of the Logger class
        log_obj = log_handler.Logger(
            name="test_name",
            loggers=["log"],
            loglvl=logging.INFO,
            filename=filename,
            filepath=folder,
            filefmt=formatter,
            fhandler=logging.FileHandler(
                f"{folder}/{filename}", "w", encoding="locale"
            ),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False,
        )

        mock_os.path.getsize = MagicMock(return_value=0)
        mock_os.remove = MagicMock(side_effect=FileNotFoundError())

        log_obj.out()
        captured = capsys.readouterr()
        assert "Failed to remove file" in captured.out

        # Verify that the getsize method was called once
        mock_os.path.getsize.assert_called_once_with(folder)


# Test 11: test out failing to remove folder
def test_out_folder_fail(capsys, mock_os, mock_atexit_register):
    folder = "path/to/logs/"
    filename = "test_file.log"
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S"
    )

    with patch("builtins.open", mock_open()):
        # create an instance of the Logger class
        log_obj = log_handler.Logger(
            name="test_name",
            loggers=["log"],
            loglvl=logging.INFO,
            filename=filename,
            filepath=folder,
            filefmt=formatter,
            fhandler=logging.FileHandler(
                f"{folder}/{filename}", "w", encoding="locale"
            ),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False,
        )

        mock_os.path.getsize = MagicMock(return_value=0)
        mock_os.remove = MagicMock(return_value=None)
        mock_os.listdir = MagicMock(return_value=[])
        mock_os.rmdir = MagicMock(side_effect=FileNotFoundError())

        log_obj.out()
        captured = capsys.readouterr()
        assert "Failed to remove module folder" in captured.out
        assert "Failed to remove log folder" in captured.out

        # Verify that the getsize method was called once
        mock_os.path.getsize.assert_called_once_with(folder)
