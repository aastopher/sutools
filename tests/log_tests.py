from unittest.mock import patch
from io import StringIO
from sutools import log_handler

#### Properties

# Test 1: this should test passing in a name for our root logger
# (i.e. something like `os.path.basename(inspect.stack()[-1].filename)[:-3]`)
def test_name():
    pass

# Test 2: this should test passing list of strings for loggers to 
# reference as an optional choice of naming loggers 
# and not using the register decorator
def test_loggers():
    pass

# Test 3: this should test passing a log level 
# to change the default log level (i.e. did the log level change)
def test_loglvl():
    pass

# Test 4: this should test passing a filename convention 
# (i.e. something like `datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')`)
# the resulting filename should be equivalent to value passed in
def test_filename():
    pass

# Test 5: this should test passing a Path object to test the filepath output
# this folder should be created if it does not exist already
def test_filepath():
    pass

# Test 6: this should test passing a formatter object for the file logger
# the result should be the file logger outputs a 
# corresponding log in the given format
def test_filefmt():
    pass

# Test 7: this should test passing a handler object for the file logger
# (i.e. `logging.FileHandler(filepath, 'w')`)
def test_fhandler():
    pass

# Test 8: this should test passing a file cap integer
# 5 for capping the log files to 5 files
def test_filecap():
    pass

# Test 9: this should test passing a file timeout string
# define a timeout period by combining time unit characters with the desired integer for a specified time unit i.e. `(10m = 10 minute, 2h = 2 hours, ...)`
# unit keys = {'m': 'minutes', 'h': 'hours', 'd': 'days', 'o':'months', 'y': 'years'}
def test_filetimeout():
    pass

# Test 10: this should test passing a file boolean
# a False value should turn file logging off, 
# it is set to True by default
def test_file():
    pass

# Test 11: this should test passing a formatter object for the stream logger
# the result should be the stream logger outputs a 
# corresponding log in the given format
def test_streamfmt():
    pass

# Test 12: this should test passing a stream handler object
# (i.e. `logging.StreamHandler()`)
def test_shandler():
    pass

# Test 12: this should test passing a stream boolean
# a False value should turn stream logging off, 
# it is set to False by default
def test_stream():
    pass

#### Methods

# Test 13: this should test the out method 
# create a file in the filepath with file size of 0 
# then run the out method
# the file should be removed
def test_out():
    pass