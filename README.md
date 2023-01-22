# Overview
Swift utilities are designed to be lightweight easy to setup per module utilities

* module cli
* module logging

# TO-DO

## Logger
* add stream handling ability (console logging) with ability to pass formatter to that as well
* if no cli exists logger must create cli for debug command (should have - options to call all levels)
* de-standardize naming of logger_object if possible. (standardization was forced at first to enable CLI to run functions with loggers in them)
* alter empty file creation fix to not need separate out call at end of module

## CLI
* add debug command for running whole module with debug level logs (can I do this by using meta logger and just setting the level?)
* check cli is working with stream handler
* import importing module for running whole module

# __init__
* import importing module into init after start up to be able to feed module to cli for debug
* importing the import may also assist in refactoring current empty file management solution

## Misc.
* comment everything
* build tests
* document