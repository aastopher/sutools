# Description
**su (Super User) tools **
This package is intended to be easy to use and reduce boilerplate code.
Per module utilities, designed to be lightweight and easy to configure.


## Install
install 'sutools' using 'pip':
'''
pip install sutools
'''

## Logging Examples
* init an sutools logger with all default settings
'''
import sutools as su

# module code...

su.logger()

if __name__ == '__main__':
    # main code...
'''

* optionally pass in the name of your root application logger
* by default this will be the filename
'''
import sutools as su

# module code...

su.logger(name='optional_name')

if __name__ == '__main__':
    # main code...
'''

* optionally pass in your own set of functional logger names to add to the namespace of loggers
* by default this namespace will be defined as the set of names for all registered functions
'''
import sutools as su

# module code...

su.logger(loggers=['logger1','logger2','logger3'])

if __name__ == '__main__':
    # main code...
'''

## CLI Examples
* init an sutools cli with all default settings
'''
import sutools as su

# module code...

if __name__ == '__main__':
    su.cli()
'''

* optionally add a cli description 
* by default this is 'None'
* it is suggested to pass in your modules doc string
'''
import sutools as su

# module code...

if __name__ == '__main__':
    su.cli(__doc__)
'''

* optionally turn logs on or off when running cli commands
* by default this is False (i.e. logs will not run)
'''
import sutools as su

# module code...

if __name__ == '__main__':
    su.cli(logs=True)
'''

## TO-DO
* build tests
* write git action
* document
* add version badge
* add pipeline passing / failing badge