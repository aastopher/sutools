from unittest.mock import patch, mock_open, MagicMock, Mock
from io import StringIO
import logging, sys, datetime
from sutools import log_handler
from pathlib import Path

# Test 1: this should test passing in a name for our root logger
# (i.e. something like `os.path.basename(inspect.stack()[-1].filename)[:-3]`)
def test_name():
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

# Test 2: this should test passing list of strings for loggers to 
# reference as an optional choice of naming loggers 
# and not using the register decorator
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

# Test 3: this should test passing a log level 
# to change the default log level (i.e. did the log level change)
def test_loglvl(capsys):
    expected = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

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
                logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'), 
                logging.StreamHandler(sys.stdout), 
                stream=True)

    func_test()
    captured = capsys.readouterr()
    assert all(level in captured.out for level in expected)


# Test 4: this should test passing a filename convention 
# (i.e. something like `datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')`)
# the resulting filename should be equivalent to value passed in
def test_filepath_filename(monkeypatch):
    expected_filename = "test_file.log"

    with patch('builtins.open', mock_open()) as mock_file:

        def func_test():
            log_obj.loggers.log.info('info msg')

        mock_filepath = '/logs/test_name'

        # mock the file_controller method
        def mock_file_controller(self):
            self.fhandler.setLevel(self.loglvl) # set the level of the file handler
            self.fhandler.setFormatter(self.filefmt) # set the formatter for the file handler
            for log in vars(self.loggers).keys():
                logger = logging.getLogger(log)
                logger.addHandler(self.fhandler) # add the file handler to the logger
                logger.propagate = False # disable propagation of log messages to ancestor loggers
            return

        monkeypatch.setattr(log_handler.Logger, "file_controller", mock_file_controller)

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


# Test 5: this should test passing a formatter object for the file logger
# the result should be the file logger outputs a 
# corresponding log in the given format
def test_filefmt(monkeypatch):
    expected_filename = "test_file.log"

    with patch('builtins.open', mock_open()) as mock_file:

        # mock the file_controller method
        def mock_file_controller(self):
            self.fhandler.setLevel(self.loglvl) # set the level of the file handler
            self.fhandler.setFormatter(self.filefmt) # set the formatter for the file handler
            for log in vars(self.loggers).keys():
                logger = logging.getLogger(log)
                logger.addHandler(self.fhandler) # add the file handler to the logger
                logger.propagate = False # disable propagation of log messages to ancestor loggers
            return

        monkeypatch.setattr(log_handler.Logger, "file_controller", mock_file_controller)

        log_obj = log_handler.Logger(
            name='test_name',
            loggers=['log'],
            loglvl=logging.INFO,
            filename=expected_filename,
            filepath='/logs/test_name',
            filefmt=logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'),
            fhandler=logging.FileHandler(f'/logs/test_name/{expected_filename}', 'w', encoding='locale'),
            filecap=None,
            filetimeout=None,
            file=True,
            streamfmt=None,
            shandler=None,
            stream=False)

        with patch.object(log_obj.loggers.log.handlers[0].stream, 'write') as mock_write:
            log_time = datetime.datetime.now().strftime("%H:%M:%S")
            log_obj.loggers.log.info('Test log message')
            expected_msg = f'log INFO Test log message\n'
            assert expected_msg in mock_write.call_args_list[0][0][0]

# Test 6: this should test passing a handler object for the file logger
# (i.e. `logging.FileHandler(filepath, 'w')`)
def test_fhandler():
    pass

# Test 7: this should test passing a file cap integer
# 5 for capping the log files to 5 files
def test_filecap():
    pass

# Test 8: this should test passing a file timeout string
# define a timeout period by combining time unit characters with the desired integer for a specified time unit i.e. `(10m = 10 minute, 2h = 2 hours, ...)`
# unit keys = {'m': 'minutes', 'h': 'hours', 'd': 'days', 'o':'months', 'y': 'years'}
def test_filetimeout():
    pass

# Test 9: this should test passing a file boolean
# a False value should turn file logging off, 
# it is set to True by default
def test_file():
    pass

# Test 10: this should test passing a formatter object for the stream logger
# the result should be the stream logger outputs a 
# corresponding log in the given format
def test_streamfmt():
    pass

# Test 11: this should test passing a stream handler object
# (i.e. `logging.StreamHandler()`)
def test_shandler():
    pass

# Test 12: this should test passing a stream boolean
# a False value should turn stream logging off, 
# it is set to False by default
def test_stream():
    pass

# Test 13: this should test the out method 
# create a file in the filepath with file size of 0 
# then run the out method
# the file should be removed
def test_out():
    pass