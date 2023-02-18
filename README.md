# Description
**su (Super User) tools**

Per module utilities, designed to be lightweight, easy to configure, and reduce boilerplate code.

***

## Install
```
pip install sutools
```
***

## Initializing the Logger

</br>

The logger should be instantiated after any registered functions but before any script level functions. The loggers will not exist for function calls in this case.


</br>

**Logger Initialization Structure**
```python
import sutools as su

# registered functions...

su.logger()

# script level function calls...

if __name__ == '__main__':
    # main code...
```

***
## Logger Properties
</br>


**Default Example**
* init an sutools logger with all default settings
```python
import sutools as su

# module code...

su.logger()

if __name__ == '__main__':
    # main code...
```

</br>

**Named Property**
* optionally pass in the name of your root application logger
* by default this will be the filename
```python
import sutools as su

# module code...

su.logger(name='optional_name')

if __name__ == '__main__':
    # main code...
```

</br>

**Functional Loggers Property**
* optionally pass in your own set of functional logger names to add to the namespace of loggers
* by default this namespace will be defined as the set of names for all registered functions
```python
import sutools as su

# module code...

su.logger(loggers=['logger1','logger2','logger3'])

if __name__ == '__main__':
    # main code...
```

</br>

**Log Level Property**
* optionally pass in your own log level this can also be an integer check out the defined [log levels](https://docs.python.org/3/library/logging.html#logging-levels)
* by default this will be defined as `logging.INFO`
```python
import logging
import sutools as su

# module code...

su.logger(loglvl=logging.DEBUG)

if __name__ == '__main__':
    # main code...
```

***

## Logger Usage Examples

***

## Initializing the CLI
</br>

The CLI should be instantiated after only if the script is called directly thus it is suggested to define this after `if __name__ == '__main__'`. Any code before the cli will run even if a cli command is used; code after the cli definition will not run when passing a cli command. 

**NOTE:** The CLI should at the very least be defined after the logger if you choose to use the two utilities in parallel.

</br>

**Logger Initialization Structure**
```python
import sutools as su

# registered functions...

su.logger() # optional

# script level function calls...

if __name__ == '__main__':
    # main code (will run even when using cli commands)...
    su.cli()
    # main code (will NOT run when using cli commands)...
```

***
## Logger Properties
</br>

**Default Example**
* init an sutools cli with all default settings
```python
import sutools as su

# module code...

if __name__ == '__main__':
    su.cli()
```

</br>

**Named Example**
* optionally add a cli description 
* by default this is `None`
* it is suggested to pass in your modules doc string
```python
import sutools as su

# module code...

if __name__ == '__main__':
    su.cli(__doc__)
```

</br>

**Log Example**
* optionally turn logs on or off when running cli commands
* by default this is False (i.e. logs will not run)
```python
import sutools as su

# module code...

if __name__ == '__main__':
    su.cli(logs=True)
```

***

## CLI Usage Examples

***

## TO-DO
* build tests
* write git action
* document
* add version badge
* add pipeline passing / failing badge