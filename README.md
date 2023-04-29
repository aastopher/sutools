[![Documentation Status](https://readthedocs.org/projects/sutools/badge/?version=latest)](https://sutools.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/aastopher/sutools/branch/master/graph/badge.svg?token=ZB0AX8D6JI)](https://codecov.io/gh/aastopher/sutools)
[![PyPI version](https://badge.fury.io/py/sutools.svg)](https://badge.fury.io/py/sutools)
[![DeepSource](https://deepsource.io/gh/aastopher/sutools.svg/?label=active+issues&show_trend=true&token=RVDa2T7M-E-YSg2DVFbr1ro-)](https://deepsource.io/gh/aastopher/sutools/?ref=repository-badge)

## Description

**su (Super User) tools**

Per module utilities, designed to be lightweight, easy to configure, and reduce boilerplate code.


**info**

This package is intended to create an lower barrier for entry for logging and module level cli with sensible defaults; sutools is not intended to replace click, argparse, logging or other utility libraries. If your project requires a more flexible configuration please use the appropriate tooling.
***

## Quick Start:

## Register Functions with sutools

</br>

Using the register decorator `@su.register` on your functions will register it with sutools `meta_handler`. Stored functions are available across tools. This registry is intended to be used by logger and cli utilities.

```python
import sutools as su

@su.register
def add(x : int, y : int):
    '''add two integers'''
    return x + y

```

You can also register async functions, these will be executed using `asyncio.run()` given a valid coroutine function

```python
import sutools as su
import asyncio

@su.register
async def delay_add(x : int, y : int):
    '''add two integers after 1 sec'''
    await asyncio.sleep(1)
    return x + y
    
```

**NOTE:** Adding type hinting to your functions enforces types in the cli and adds positional arg class identifiers in the help docs for the command.

</br>

***

## CLI Usage Example

</br>

```python
"""This module does random stuff."""
import sutools as su

@su.register
def meet(name : str, greeting : str = 'hello', farewell : str = 'goodbye') -> str:
        '''meet a person'''
        output = f'\n{greeting} {name}\n{farewell} {name}'
        su.log().meeting.info(output)
        return output

su.logger() # optional

# module level function calls...

if __name__ == '__main__':
    # main code (will run even when using cli commands)...
    su.cli(desc = __doc__)
    # main code (will NOT run when using cli commands)...
```

</br>

**NOTE:** Adding type hinting to your functions enforces types in the cli and adds positional arg class identifiers in the help docs for the command.

**command usage:**

```
python module.py meet foo
```

**output**

```
hello foo
goodbye foo
```

**module help output:**

```
    usage: module [-h] {meet} ...

    This module does random stuff.

    options:
    -h, --help  show this help message and exit

    commands:
    {meet}
        meet      meet a person
```

**command help output:**

```
    usage: dev meet [-gr <class 'str'>] [-fa <class 'str'>] [-h] name

    meet(name: str, greeting: str = 'hello', farewell: str = 'goodbye') -> str

    positional arguments:
    name                  <class 'str'>

    options:
    -gr <class 'str'>, --greeting <class 'str'>
                            default: hello
    -fa <class 'str'>, --farewell <class 'str'>
                            default: goodbye
    -h, --help            Show this help message and exit.
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
    return x + y

@su.register
def minus(x : int, y : int):
    '''subtract two integers'''
    su.log().minus.info(f'{x} - {y} = {x-y}')
    return x - y

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
    return x + y

@su.register
def minus(x : int, y : int):
    '''subtract two integers'''
    su.log().logger2.info(f'{x} - {y} = {x-y}')
    return x - y

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