# Overview
Swift utilities are designed to be lightweight easy to setup per module utilities

* module cli
* module logging

# TO-DO

## Logger
* if no cli exists logger must create cli for debug command (should have - options to call all levels)
* must init logger before cli at present

## CLI
* when running cli func, whole module still runs?
* add debug command for running whole module with debug level logs (can I do this by using meta logger and just setting the level?)
* import importing module for running whole module

# __init__
* import importing module into init after start up to be able to feed module to cli for debug

## Misc.
* comment everything
* build tests
* document