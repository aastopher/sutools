from unittest.mock import patch, mock_open, MagicMock, Mock, call
from io import StringIO
import logging, sys, datetime, os, time, warnings
from sutools import log_handler
from pathlib import Path
from freezegun import freeze_time
import pytest


### FIXTURES
@pytest.fixture
def mock_os(monkeypatch):
    mock_os = Mock()
    monkeypatch.setattr(log_handler, "os", mock_os)
    return mock_os

@pytest.fixture
def mock_file_controller(monkeypatch):
    def _mock_file_controller(self):
        self.fhandler.setLevel(self.loglvl) # set the level of the file handler
        self.fhandler.setFormatter(self.filefmt) # set the formatter for the file handler
        for log in vars(self.loggers).keys():
            logger = logging.getLogger(log)
            logger.addHandler(self.fhandler) # add the file handler to the logger
            logger.propagate = False # disable propagation of log messages to ancestor loggers
        return

    monkeypatch.setattr(log_handler.Logger, "file_controller", _mock_file_controller)

### TESTS

# Test 1: tests name, file, and stream options in log_handler.Logger()
def test_name_file_stream():
    expected = "test_name"
    log_obj = log_handler.Logger(
                expected,
                ['log'],
                logging.INFO,
                None, None, None, None, None, None,
                False,
                logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'),
                logging.StreamHandler(sys.stdout),
                stream=True)

    assert expected == log_obj.name

# Test 2: tests the logger option in log_handler.Logger()
def test_loggers():
    expected = ['logger1','logger2','logger3']
    log_obj = log_handler.Logger(
                'test name',
                expected,
                logging.INFO,
                None, None, None, None, None, None,
                False,
                logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'),
                logging.StreamHandler(sys.stdout),
                stream=True)

    assert all(item in log_obj.loggers.__dict__ for item in expected)

# Test 3: tests loglvl, shandler, and streamfmt options in log_handler.Logger()
def test_loglvl_shandler_streamfmt(capsys):
    expected = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

    def func_test():
        log_obj.loggers.log.debug('debug message')
        log_obj.loggers.log.info('info message')
        log_obj.loggers.log.warning('warning message')
        log_obj.loggers.log.error('error message')
        log_obj.loggers.log.critical('critical message')

    log_obj = log_handler.Logger(
                'test_logger',
                ['log'],
                logging.DEBUG,
                None, None, None, None, None, None,
                False,
                formatter,
                logging.StreamHandler(sys.stdout),
                stream=True)

    func_test()
    captured = capsys.readouterr()
    assert all(level in captured.out for level in expected)

    with patch.object(log_obj.loggers.log.handlers[0].stream, 'write') as mock_write:
            log_obj.loggers.log.handlers[0].setFormatter(formatter)
            log_time = datetime.datetime.now().strftime("%H:%M:%S")
            log_obj.loggers.log.info('Test log message')
            expected_msg = f'{log_time}, log INFO Test log message\n'
            assert expected_msg == mock_write.call_args_list[0][0][0]


# Test 4: tests filepath, filename, and fhandler options in log_handler.Logger()
def test_filepath_filename_fhandler(mock_file_controller):
    expected_filename = "test_file.log"

    with patch('builtins.open', mock_open()) as mock_file:

        def func_test():
            log_obj.loggers.log.info('info msg')

        mock_filepath = '/logs/test_name'

        log_obj = log_handler.Logger(
                    name='test_name',
                    loggers=['log'],
                    loglvl=logging.INFO,
                    filename=expected_filename,
                    filepath=mock_filepath,
                    filefmt=logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'),
                    fhandler=logging.FileHandler(f'{mock_filepath}/{expected_filename}', 'w', encoding='locale'),
                    filecap=None,
                    filetimeout=None,
                    file=True,
                    streamfmt=None,
                    shandler=None,
                    stream=False)

        func_test()

        # check that the file was opened with the expected arguments
        mock_file.assert_called_with(f'{mock_filepath}/{expected_filename}', 'w', encoding='locale', errors=None)


# Test 5: tests filefmt option in log_handler.Logger()
def test_filefmt(mock_file_controller):
    filename = "test_file.log"
    formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

    with patch('builtins.open', mock_open()) as mock_file:

        log_obj = log_handler.Logger(
            name='test_name',
            loggers=['log'],
            loglvl=logging.INFO,
            filename=filename,
            filepath='/logs/test_name',
            filefmt=formatter,
            fhandler=logging.FileHandler(f'/logs/test_name/{filename}', 'w', encoding='locale'),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False)

        with patch.object(log_obj.loggers.log.handlers[0].stream, 'write') as mock_write:
            log_obj.loggers.log.handlers[0].setFormatter(formatter)
            log_time = datetime.datetime.now().strftime("%H:%M:%S")
            log_obj.loggers.log.info('Test log message')
            expected_msg = f'{log_time}, log INFO Test log message\n'
            assert expected_msg == mock_write.call_args_list[0][0][0]

# Test 6: this should test passing a file cap integer
# 5 for capping the log files to 5 files
def test_filecap(mock_os, mock_file_controller):
    folder = 'path/to/logs'
    filename = "test_file.log"
    formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

    # create mock files with different creation times
    file1 = ('path/to/logs/file1.log', 1646106476)
    file2 = ('path/to/logs/file2.log', 1646192876)
    file3 = ('path/to/logs/file3.log', 1646279276)

    # create a list of mock files
    mock_files = [file1, file2, file3]

    with patch('builtins.open', mock_open()):
        # create an instance of the Logger class
        log_obj = log_handler.Logger(
            name='test_name',
            loggers=['log'],
            loglvl=logging.INFO,
            filename=filename,
            filepath=folder,
            filefmt=formatter,
            fhandler=logging.FileHandler(f'{folder}/{filename}', 'w', encoding='locale'),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False)

        # mock the os functions used inside the cap method
        mock_os.path.getctime.return_value = 1646106476
        mock_os.listdir.return_value = ['file1.log', 'file2.log', 'file3.log']

        # call the cap method with filecap = 2
        log_obj.cap(2)

        # verify that os.path.join was called twice for each file with correct filename
        join_calls = [call[0][1] for call in mock_os.path.join.call_args_list]
        expected_files = ['file1.log', 'file2.log', 'file3.log']
        assert all(filename in expected_files for filename in join_calls)
        assert mock_os.path.join.call_count == 6

        # verify that os.path.getctime was called once for each file
        assert mock_os.path.getctime.call_count == 3

        # verify that os.remove was called once
        mock_os.remove.assert_called_once

        # verify that os.listdir was called once
        mock_os.listdir.assert_called_once


# Test 7: this should test passing a file timeout string
# define a timeout period by combining time unit characters with the desired integer for a specified time unit i.e. `(10m = 10 minute, 2h = 2 hours, ...)`
@freeze_time("2023-02-25 10:00:00")
def test_timeout(mock_os, mock_file_controller):
    folder = 'path/to/logs'
    filename = "test_file.log"
    formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
    mock_files = [
        ('path/to/logs/file1.log', time.time() - 1800),
        ('path/to/logs/file2.log', time.time() - 900),
        ('path/to/logs/file3.log', time.time() - 3600)
    ]

    # mock the return values for os.path.getctime and os.listdir
    mock_os.path.getctime.side_effect = [f[1] for f in mock_files]
    mock_os.listdir.return_value = [os.path.basename(f[0]) for f in mock_files]

    with patch('builtins.open', side_effect=mock_files):
        log_obj = log_handler.Logger(
            name='test_name',
            loggers=['log'],
            loglvl=logging.INFO,
            filename=filename,
            filepath=folder,
            filefmt=formatter,
            fhandler=logging.FileHandler(f'{folder}/{filename}', 'w', encoding='locale'),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False)

        # call the timeout method
        log_obj.timeout('30m')

        # assert that os.listdir was called with the correct folder path
        mock_os.listdir.assert_called_once

        # assert that os.remove was not called for logs that have not timed out
        mock_os.remove.assert_called_once()

        # assert that warnings.warn was called once with the correct message for an invalid time unit
        with patch('warnings.warn') as mock_warn:
            log_obj.timeout('1z')
            mock_warn.assert_called_once_with('Invalid time unit: z', Warning)
            

# Test 8: this should test the out method
# create a file in the filepath with file size of 0
# then run the out method
# the file should be removed
def test_out(mock_os, mock_file_controller):
    folder = 'path/to/logs/'
    filename = "test_file.log"
    formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

    with patch('builtins.open', mock_open()) as mock_file:

        # create an instance of the Logger class
        log_obj = log_handler.Logger(
            name='test_name',
            loggers=['log'],
            loglvl=logging.INFO,
            filename=filename,
            filepath=folder,
            filefmt=formatter,
            fhandler=logging.FileHandler(f'{folder}/{filename}', 'w', encoding='locale'),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False)


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
        