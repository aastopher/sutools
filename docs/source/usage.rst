sutools usage
-------------

register functions with sutools
===============================

Using the register decorator `@su.register` on your functions will register it with sutools `meta_handler`. Stored functions are available across tools. This registry is intended to be used by logger and cli utilities.

.. code-block:: python

   import sutools as su

   @su.register
   def add(x : int, y : int):
       '''add two integers'''
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
    def minus(x : int, y : int):
        '''subtract two integers'''
        su.log().minus.info(f'{x} - {y} = {x-y}')
        return x - y

    su.logger() # logger definition

    # module level function calls
    add(1,2)
    minus(1,2)

    if __name__ == '__main__':
        # main code (will run even when using cli commands)...
        su.cli() # optional
        # main code (will NOT run when using cli commands)...

**log output**

.. code-block:: console

    16:16:34, 961 add INFO 1 + 2 = 3
    16:16:34, 961 minus INFO 1 - 2 = -1

**using custom logger names**

.. code-block:: python

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

    su.logger(loggers=['logger1','logger2']) # logger definition

    # module level function calls
    add(1,2)
    minus(1,2)

    if __name__ == '__main__':
        # main code (will run even when using cli commands)...
        su.cli() # optional
        # main code (will NOT run when using cli commands)...

**log output**

.. code-block:: console

    16:16:34, 961 add INFO 1 + 2 = 3
    16:16:34, 961 minus INFO 1 - 2 = -1