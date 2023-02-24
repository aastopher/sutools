from unittest.mock import patch
from io import StringIO
import sutools as su

#### Methods

# Test 1: this should test the register decorator from sutools
# the result should be that the su.store contains a 
# none empty dictionary for the func property
def test_register():
    pass

# Test 2: this should test the cli from sutools
# the result should be that the cli property is not None in su.store
# the cli object should contain commands for any registered functions
def test_cli():
    pass

# Test 3: this should test the logger from sutools
# the result should be that the log property is no None in su.store
# the log object should also contain a property loggers with 
# the names of the loggers passed in to loggers property in the logger
def test_logger():
    pass

# Test 4: this should test the log helper function
# the should return a namespace of loggers defined 
# in the log object in the su.store
def test_log():
    pass

#### Integrations

# Test 5: this should test integrations for cli and logger compatibility
# this should init both a logger and a cli as well as 
# at least one registered test function.
# the result should be that the log statements in the cli are 
# logged if the cli has logs set to True
def test_logger_cli():
    pass