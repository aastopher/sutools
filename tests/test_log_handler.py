from unittest.mock import patch, mock_open, MagicMock, Mock
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
def test_filecap(monkeypatch, mock_file_controller):
    folder = 'path/to/logs'
    filename = "test_file.log"
    formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

    # create mock files with different creation times
    file1 = ('path/to/logs/file1.log', 1646106476)
    file2 = ('path/to/logs/file2.log', 1646192876)
    file3 = ('path/to/logs/file3.log', 1646279276)

    # create a list of mock files
    mock_files = [file1, file2, file3]

    # mock the open function to return a mock file object for each mock file
    mock_file_objects = []
    for f in mock_files:
        m = mock_open()
        m.return_value.__iter__.return_value = ['test line 1', 'test line 2']
        mock_file_objects.append(m)

    with patch('builtins.open', side_effect=mock_file_objects):

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
    
        def mock_cap(filecap, mock_files):
            deleted_files = []
            if len(mock_files) > filecap:
                logs_to_remove = len(mock_files) - filecap
                for log in mock_files[filecap:]:
                    deleted_files.append(log[0])
                if logs_to_remove > 1:
                    print(f'filecap removed {logs_to_remove} logs')
                else:
                    print("filecap reached")
            return deleted_files
        
        monkeypatch.setattr(log_obj, "cap", mock_cap)
        # call the cap method with the mock files using the patched implementation
        deleted_files = log_obj.cap(2, mock_files)

        # check that the mock files were deleted correctly
        assert file1[0] not in deleted_files
        assert file2[0] not in deleted_files
        assert file3[0] in deleted_files

# Test 7: this should test passing a file timeout string
# define a timeout period by combining time unit characters with the desired integer for a specified time unit i.e. `(10m = 10 minute, 2h = 2 hours, ...)`
@freeze_time("2023-02-25 10:00:00")
def test_timeout(monkeypatch, mock_file_controller):
    folder = 'path/to/logs'
    filename = "test_file.log"
    formatter = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

    # create mock files with different timestamps
    file1 = ('path/to/logs/file1.log', time.time() - 1800)  # 30 mins ago
    file2 = ('path/to/logs/file2.log', time.time() - 900)   # 15 mins ago
    file3 = ('path/to/logs/file3.log', time.time() - 3600)  # 1 hour ago

    # create a list of mock files
    mock_files = [file1, file2, file3]

    with patch('builtins.open', side_effect=mock_files), \
         patch('warnings.warn') as mock_warn:
        
        def mock_timeout(self, filetimeout, mockfiles):
            '''delete any file outside given time range'''
            try:
                # get the mock file paths
                logs = [f[0] for f in mockfiles if f[0].endswith('.log')]

                # define time units and extract the amount and unit of the file timeout.
                time_units = {'m': 'minutes', 'h': 'hours', 'd': 'days', 'o':'months', 'y': 'years'}
                time_unit = time_units[filetimeout[-1]]
                time_amount = int(filetimeout[:-1])

                # get the current time and calculate the time threshold based on the file timeout
                now = datetime.datetime.now()
                if time_unit == 'years':
                    time_threshold = now - datetime.timedelta(days=time_amount*365)
                elif time_unit == "minutes":
                    time_threshold = now - datetime.timedelta(minutes=time_amount)
                elif time_unit == 'months':
                    time_threshold = now - datetime.timedelta(days=time_amount*30)
                else:
                    time_threshold = now - datetime.timedelta(**{time_unit: time_amount})

                # remove all logs that are older than the time threshold and collect the removed logs
                logs_removed = []
                for file, time in mockfiles:
                    if time < time_threshold.timestamp():
                        logs_removed.append((file, time))
                        
                # print the number of logs that were removed if any
                if logs_removed:
                    print(f'timeout removed {len(logs_removed)} logs')
                
                return logs_removed

            except KeyError:
                # warn the user if an invalid time unit is provided
                warnings.warn(f"Invalid time unit: {filetimeout[-1]}", Warning)
        
        monkeypatch.setattr(log_handler.Logger, "timeout", mock_timeout)

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

        removedfiles = log_obj.timeout('30m', mock_files)
        print(removedfiles)

        assert file1 not in removedfiles
        assert file2 not in removedfiles
        assert file3 in removedfiles

        # call the timeout method with an invalid time unit
        log_obj.timeout('1z', mock_files)

        # check that a warning is raised
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
        