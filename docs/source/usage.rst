usage
-----

register functions with sutools
===============================

Using the register decorator `@su.register` on your functions will register it with sutools `meta_handler`. Stored functions are available across tools. This registry is intended to be used by logger and cli utilities.

.. code-block:: python

   import sutools as su

   @su.register
   def add(x : int, y : int):
       '''add two integers'''
       return x + y

You can also register async functions, these will be executed using `asyncio.run()` given a valid coroutine function

.. code-block:: python

   import sutools as su
   import asyncio

   @su.register
   async def delay_add(x : int, y : int):
       '''add two integers after 1 sec'''
       await asyncio.sleep(1)
       return x + y

**NOTE:** Adding type hinting to your functions enforces types in the cli and adds positional arg class identifiers in the help docs for the command.

cli - initialization standard
=============================

It is suggested to define the command line interface after `if __name__ == '__main__'`. Any code before the cli will run even if a cli command is used; code after the cli definition will not run when passing a cli command.

.. code-block:: python

    import sutools as su

    # registered functions...

    su.logger(*args, **kwargs) # optional

    # module level function calls...

    if __name__ == '__main__':
        # main code (will run even when using cli commands)...
        su.cli(*args, **kwargs)
        # main code (will NOT run when using cli commands)...

**NOTE:** The CLI should be defined after the logger if you choose to use the two utilities in parallel.

cli - usage example
===================

The logger utility should be instantiated after any registered functions but before any module level functions.

.. code-block:: python

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

**NOTE:** Adding type hinting to your functions enforces types in the cli and adds positional arg class identifiers in the help docs for the command.

**command usage:**

.. code-block:: console

    python module.py meet foo

**output:**

.. code-block:: console

    hello foo
    goodbye foo

**module help output:**

.. code-block:: console

    usage: module [-h] {meet} ...

    This module does random stuff.

    options:
    -h, --help  show this help message and exit

    commands:
    {meet}
        meet      meet a person

**command help output:**

.. code-block:: console

    usage: module meet [-gr <class 'str'>] [-fa <class 'str'>] [-h] name

    meet(name: str, greeting: str = 'hello', farewell: str = 'goodbye') -> str

    positional arguments:
    name                  <class 'str'>

    options:
    -gr <class 'str'>, --greeting <class 'str'>
                            default: hello
    -fa <class 'str'>, --farewell <class 'str'>
                            default: goodbye
    -h, --help            Show this help message and exit.

cli - using variadic functions
==============================

Variadic functions are compatible with sutools cli utility. When calling kwargs from the cli; `key=value` should be used instead of `--` and `-`, these are reserved for default arguments.

**NOTE:** since input is from `stdin` it will always be of type `<string>` for sutools will not infer the data type you must infer your needed type within the function.

.. code-block:: python

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

**command usage:**

.. code-block:: console

    python module.py variadic 1 2 3 foo=1 bar=2

**output:**

.. code-block:: console

    Positional arguments:
    1
    2
    3
    Keyword arguments:
    foo = 1
    bar = 2

logger - initialization standard
================================

The logger utility should be instantiated after any registered functions but before any module level functions.

.. code-block:: python

    import sutools as su

    # registered functions...

    su.logger(*args, **kwargs)

    # module level function calls...

    if __name__ == '__main__':
        # main code (will run even when using cli commands)...
        su.cli(*args, **kwargs) # optional
        # main code (will NOT run when using cli commands)...


logger - usage examples
=======================

 accessing defined loggers is done with a `log()` helper function. Note the use of `su.log()` in the below functions to access a specified logger before defining the log level and message.


**using registered function names**

.. code-block:: python

    import sutools as su

    @su.register
    def add(x : int, y : int):
        '''add two integers'''
        su.log().add.info(f'{x} + {y} = {x+y}')
        return x + y

    @su.register
    def subtract(x : int, y : int):
        '''subtract two integers'''
        su.log().subtract.info(f'{x} - {y} = {x-y}')
        return x - y

    su.logger() # logger definition

    # module level function calls
    add(1,2)
    subtract(1,2)

    if __name__ == '__main__':
        # main code (will run even when using cli commands)...
        su.cli() # optional
        # main code (will NOT run when using cli commands)...

**log output**

.. code-block:: console

    16:16:34, 961 add INFO 1 + 2 = 3
    16:16:34, 961 subtract INFO 1 - 2 = -1

**using custom logger names**

.. code-block:: python

    import sutools as su

    @su.register
    def add(x : int, y : int):
        '''add two integers'''
        su.log().logger1.info(f'{x} + {y} = {x+y}')
        return x + y

    @su.register
    def subtract(x : int, y : int):
        '''subtract two integers'''
        su.log().logger2.info(f'{x} - {y} = {x-y}')
        return x - y

    su.logger(loggers=['logger1','logger2']) # logger definition

    # module level function calls
    add(1,2)
    subtract(1,2)

    if __name__ == '__main__':
        # main code (will run even when using cli commands)...
        su.cli() # optional
        # main code (will NOT run when using cli commands)...

**log output**

.. code-block:: console

    16:16:34, 961 add INFO 1 + 2 = 3
    16:16:34, 961 subtract INFO 1 - 2 = -1

benchy - usage example
======================

The `benchy` decorator is designed to collect performance timing and call info for selected functions. This can be used in combination with `@su.register`, the decorators are order independent.

.. code-block:: python

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
        '''caclulates a thing'''
        if atype == '+':
            res = add(x, y)
        elif atype == '-':
            res = subtract(x, y)
        return res

    add(1,2)
    add(2,2)
    subtract(1,2)
    calc(2,3, atype='-')


After the functions have been executed, the benchmark report can be accessed with `su.benchy.report`.

.. code-block:: python

    # print the benchmark report
    print(su.benchy.report)

example output

.. code-block:: bash

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

The output of the benchmark report will adhere to the following format. `function > call records`. Call records consist of `{args, kwargs, result, benchmark}` there will be a record for each call of a given function.

**NOTE:** given an iterable for `arg`, `kwarg`, or `result` the object will be summarized in terms of vector length.

.. code-block:: bash

    {'function_name': [{'args': [{'type': 'arg_type', 'value': int}]
                        'benchmark': float,
                        'kwargs': {'kwarg_name': {'type': 'arg_type', 'length': int, }}
                        'result': {'type': 'arg_type', 'value': float}}]}