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

## CLI Using Variadic Functions

Variadic functions are compatible with sutools cli utility. When calling kwargs from the cli; `key=value` should be used instead of `--` and `-`, these are reserved for default arguments.

**NOTE:** since input is from `stdin` it will always be of type `<string>`, sutools will _not_ infer the data type you must infer your needed type within the function.

```python
"""This module does random stuff."""
import sutools as su

@su.register
def variadic(*args, **kwargs):
    
    print("Positional arguments:")
    for arg in args:
        print(arg)

    print("Keyword arguments:")
    for key, value in kwargs.items():
        print(f"{key} = {value}")

    su.logger() # optional

# module level function calls...

if __name__ == '__main__':
    # main code (will run even when using cli commands)...
    su.cli(desc = __doc__)
    # main code (will NOT run when using cli commands)...
```

**command usage:**

```
python module.py variadic 1 2 3 foo=1 bar=2
```

**output:**

```
Positional arguments:
1
2
3
Keyword arguments:
foo = 1
bar = 2
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
</br>

## Benchy Usage Example

</br>

The `benchy` decorator is designed to collect performance timing and call info for selected functions. This can be used in combination with `@su.register`, the decorators are order independent.

```python
import sutools as su

@su.benchy
@su.register
def add(x : int, y : int):
    '''add two integers'''
    return x + y

@su.register
@su.benchy
def subtract(x : int, y : int):
    '''subtract two integers'''
    return x - y

@su.benchy
@su.register
def calc(x : int, y : int, atype : str = '+') -> int:
    '''calculates a thing'''
    if atype == '+':
        res = x + y
    elif atype == '-':
        res = x - y
    return res

add(1,2)
add(2,2)
subtract(1,2)
calc(2,3, atype='-')

```

After the functions have been executed, the benchmark report can be accessed with `su.benchy.report`.

```python
# print the benchmark report
print(su.benchy.report)
```

**Example output**

```
{'add': [{'args': [{'type': 'int', 'value': 1}, {'type': 'int', 'value': 2}],
        'benchmark': 0.00015466799959540367,
        'kwargs': None,
        'result': {'type': 'int', 'value': 3}},
        {'args': [{'type': 'int', 'value': 2}, {'type': 'int', 'value': 2}],
        'benchmark': 6.068096263334155e-05,
        'kwargs': None,
        'result': {'type': 'int', 'value': 4}}],
'calc': [{'args': [{'type': 'int', 'value': 2}, {'type': 'int', 'value': 3}],
        'benchmark': 4.855601582676172e-05,
        'kwargs': {'atype': {'length': 1, 'type': 'str'}},
        'result': {'type': 'int', 'value': 5}}],
'subtract': [{'args': [{'type': 'int', 'value': 1}, {'type': 'int', 'value': 2}],
        'benchmark': 5.205394700169563e-05,
        'kwargs': None,
        'result': {'type': 'int', 'value': -1}}]}
```

The output of the benchmark report will adhere to the following format: `function > call records`. Call records consist of `{args, kwargs, result, benchmark}` there will be a record for each call of a given function.

**NOTE:** given an iterable for `arg`, `kwarg`, or `result` the object will be summarized in terms of vector length.

```
{'function_name': [{'args': [{'type': 'arg_type', 'value': int}]
                    'benchmark': float,
                    'kwargs': {'kwarg_name': {'type': 'arg_type', 'length': int, }}
                    'result': {'type': 'arg_type', 'value': float}}]}
```