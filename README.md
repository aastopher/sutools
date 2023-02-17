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

**Named Example**
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

**Functional Loggers Example**
* optionally pass in your own set of functional logger names to add to the namespace of loggers
* by default this namespace will be defined as the set of names for all registered functions
```python
import sutools as su

# module code...

su.logger(loggers=['logger1','logger2','logger3'])

if __name__ == '__main__':
    # main code...
```

***

## Logger Usage Examples

***

## Initializing the CLI

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