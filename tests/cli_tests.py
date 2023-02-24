from unittest.mock import patch
from io import StringIO
from sutools import cli_handler

#### Properties

# Test 1: this should test passing in a cli description
def test_desc():
    pass

# Test 2: this should test passing a 
# boolean to logs to turn logging on or off (i.e. 51)
def test_logs():
    pass

# Test 3: this should test passing a logger object 
# (if a log_obj is passed in there should be loggers in the log property)
def test_log_obj():
    pass

#### Methods

# Test 4: this should test adding references of functions 
# for to the cli to run (a dictionary of functions should be provided 
# then the cli should be tested to use those functions)
def test_add_funcs():
    pass

# Test 5: this should test the parse method 
# this is called after functions are added to be called as a command
def test_parse():
    pass