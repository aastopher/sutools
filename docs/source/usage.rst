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
       print(x + y)

**NOTE:** Adding type hinting to your functions enforces types in the cli and adds positional arg class identifiers in the help docs for the command.

cli - initialization standard
=============================

It is suggested to define the command line interface after `if __name__ == '__main__'`. Any code before the cli will run even if a cli command is used; code after the cli definition will not run when passing a cli command.

.. code-block:: python

    import sutools as su

    # registered functions...

    su.logger(**args) # optional

    # module level function calls...

    if __name__ == '__main__':
        # main code (will run even when using cli commands)...
        su.cli(**args)
        # main code (will NOT run when using cli commands)...

**NOTE:** The CLI should be defined after the logger if you choose to use the two utilities in parallel.

logger - initialization standard
================================

The logger utility should be instantiated after any registered functions but before any module level functions.

.. code-block:: python

    import sutools as su

    # registered functions...

    su.logger(**args)

    # module level function calls...

    if __name__ == '__main__':
        # main code (will run even when using cli commands)...
        su.cli(**args) # optional
        # main code (will NOT run when using cli commands)...