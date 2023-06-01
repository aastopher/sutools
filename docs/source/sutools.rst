sutools
-------

**su (Super User) tools**

Per module utilities, designed to be lightweight, easy to configure, and reduce boilerplate code.

**info**

This package is intended to create an lower barrier for entry for logging and module level cli with sensible defaults; sutools is not intended to replace click, argparse, logging or other utility libraries. If your project requires a more flexible configuration please use the appropriate tooling.

.. automodule:: sutools
   :members:

store
^^^^^

sutools ``store`` instance is a global instance of the ``meta_handler.Bucket`` class. This instance is used to store functions, cli objects, and logger objects for access across utilities.

benchy
^^^^^^^

sutools ``benchy`` instance is a global instance of the ``bench_handler.Benchy`` class. This instance is used as a decorator to collect benchmarking stats for selected functions.