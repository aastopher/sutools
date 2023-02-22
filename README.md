[![Documentation Status](https://readthedocs.org/projects/sutools/badge/?version=latest)](https://sutools.readthedocs.io/en/latest/?badge=latest)

## Description

**su (Super User) tools**

Per module utilities, designed to be lightweight, easy to configure, and reduce boilerplate code.

***

## Install

</br>

```
pip install sutools
```
***

## Register Functions with sutools

</br>

Using the register decorator `@su.register` on your functions will register it with sutools `meta_handler`. Stored functions are available across tools. This registry is intended to be used by logger and cli utilities.

```python
import sutools as su

@su.register
def add(x : int, y : int):
    '''add two integers'''
    print(x + y)

```

**NOTE:** Adding type hinting to your functions enforces types in the cli and adds positional arg class identifiers in the help docs for the command.

</br>

***

## CLI Usage Example

</br>

```python
import sutools as su

@su.register
def add(x : int, y : int):
    '''add two integers'''
    su.log().add.info(f'{x} + {y} = {x+y}') # optional
    print(x + y).

su.logger() # optional

# module level function calls...

if __name__ == '__main__':
    # main code (will run even when using cli commands)...
    su.cli(desc = __doc__)
    # main code (will NOT run when using cli commands)...
```

</br>

**NOTE:** Adding type hinting to your functions enforces types in the cli and adds positional arg class identifiers in the help docs for the command.

**command specific help output:**
```
usage: module add [-h] x y

positional arguments:
  x           <class 'int'>
  y           <class 'int'>

options:
  -h, --help  show this help message and exit
```

## Logger Usage Examples

</br>
 
 accessing defined loggers is done with a `log()` helper function. Note the use of `su.log()` in the below functions to access a specified logger before defining the log level and message.

</br>

**using registered function names**


```python
import sutools as su

@su.register
def add(x : int, y : int):
    '''add two integers'''
    su.log().add.info(f'{x} + {y} = {x+y}')
    print(x + y)

@su.register
def minus(x : int, y : int):
    '''subtract two integers'''
    su.log().minus.info(f'{x} - {y} = {x-y}')
    print(x - y).

su.logger()

# module level function calls
add(1,2)
minus(1,2)

if __name__ == '__main__':
    # main code (will run even when using cli commands)...
    su.cli() # optional
    # main code (will NOT run when using cli commands)...
```

</br>

**log output**
```
16:16:34, 961 add INFO 1 + 2 = 3
16:16:34, 961 minus INFO 1 - 2 = -1
```

</br>

**using custom logger names**


```python
import sutools as su

@su.register
def add(x : int, y : int):
    '''add two integers'''
    su.log().logger1.info(f'{x} + {y} = {x+y}')
    print(x + y)

@su.register
def minus(x : int, y : int):
    '''subtract two integers'''
    su.log().logger2.info(f'{x} - {y} = {x-y}')
    print(x - y).

su.logger(loggers=['logger1','logger2'])

# module level function calls
add(1,2)
minus(1,2)

if __name__ == '__main__':
    # main code (will run even when using cli commands)...
    su.cli() # optional
    # main code (will NOT run when using cli commands)...
```

</br>

**log output**
```
16:16:34, 961 logger1 INFO 1 + 2 = 3
16:16:34, 961 logger2 INFO 1 - 2 = -1
```

***

**command usage:**

```
python module.py add 1 2
```
**output:**
```
3
```

***


## TO-DO
* sphinx autodocs partially complete
* add basic usage back into readme
* build tests
* write git action
* add version badge
* add pipeline passing / failing badge