## NEEDS EDIT!!

# Overview
A lightweight logging library designed for easy granular logging for all your modules.

[![PyPI version](https://badge.fury.io/py/DeepLogger.svg)](https://badge.fury.io/py/DeepLogger)

## Basic Usage

* The Deep Logger object takes 2 arguments. Your module name as a **string** and the **list** of granular loggers you would like to create
```
from DeepLogger import DeepLogger

DL = DeepLogger('module_name',['function_1','function_2','function_n'])
F1Logger = DL.getLogger('function_1')
F2Logger = DL.getLogger('function_2')
FNLogger = DL.getLogger('function_n')
```

## How to use your new loggers

* To create a new info level log line in one of your function loggers use the following pattern. (see below for additional log level options)
* `F1Logger.info('log message')`
* Each Deep Logger object contains it's own StreamHandler which will allow you to print to console based on the above configuration as follows
* `DL.console_logger('log message')`

## Log levels

* NOTSET = 0: This is the initial default setting of a log when it is created. It is not really relevant and most developers will not even take notice of this category. In many circles, it has already become nonessential. The root log is usually created with level WARNING.
* DEBUG = 10: This level gives detailed information, useful only when a problem is being diagnosed.
* INFO = 20: This is used to confirm that everything is working as it should.
* WARNING = 30: This level indicates that something unexpected has happened or some problem is about to happen in the near future.
* ERROR = 40: As it implies, an error has occurred. The software was unable to perform some function.
* CRITICAL = 50: A serious error has occurred. The program itself may shut down or not be able to continue running properly.

## To do

* add sample log output to docs
