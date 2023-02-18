# Description
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

## CLI - Initialization Standard

</br>

It is suggested to define the command line interface after `if __name__ == '__main__'`. Any code before the cli will run even if a cli command is used; code after the cli definition will not run when passing a cli command.

**NOTE:** The CLI should be defined after the logger if you choose to use the two utilities in parallel.

</br>

***
## CLI - Properties

```python
import sutools as su

# registered functions...

su.logger() # optional

# script level function calls...

if __name__ == '__main__':
    # main code (will run even when using cli commands)...
    su.cli(desc = 'cli description', logs = False)
    # main code (will NOT run when using cli commands)...
```
</br>

## Property Descriptions
* **desc:** name of root module logger defines the name of log subfolder 
  * **type:** `<str>`
  * **default:** `''`
* **logs:** enable logging inside cli commands
    * **type:** `<bool>`
    * **default:** `False`

***

## CLI Usage Examples

</br>

***

## Logger - Initialization Standard

</br>

The logger utility should be instantiated after any registered functions but before any script level functions.


</br>

***
## Logger - Properties

```python
import sutools as su
from pathlib import Path
import inspect, logging, datetime

# registered functions...

logformat = '%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s'

su.logger(
    name = 'logger_name', 
    loggers = ['logger1','logger2','logger3'], 
    loglvl = logging.DEBUG,
    filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), 
    filepath = Path(filepath),
    filefmt = logging.Formatter(logformat, datefmt='%H:%M:%S'), 
    fhandler = logging.FileHandler(filepath, 'w'),
    filecap = 5, 
    filetimeout = '1h',
    file = True, 
    streamfmt = logging.Formatter(logformat, datefmt='%H:%M:%S'),
    shandler = logging.StreamHandler(),
    stream = False
    )

# script level function calls...

if __name__ == '__main__':
    # main code...
```
</br>

## Property Descriptions
* **name:** name of root module logger defines the name of log subfolder 
  * **type:** `<str>`
  * **default:** `module file name`
* **loggers:** names of functional loggers
    * **type:** `<str>`
    * **default:** `names of registered functions`
* **loglvl:** optionally pass in your own log level this can also be an integer. Check out the defined [log levels](https://docs.python.org/3/library/logging.html#logging-levels) 
  * **type:** `<int>` 
  * **default:** `logging.INFO`
* **filename:** defines name of log file instances
  * **type:** `<str>`
  * **default:** `datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')`
* **filepath:** defines path for log files
  * **type:** `<str>`, `<Path>`
  * **default:** `logs/name_of_logger/filename`
* **filefmt:** defines the log format for the file handler 
  * **type:** `<Formatter>` 
  * **default:** `logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')`
* **fhandler:** define a custom file handler
  * **type:** `<FileHandler>` 
  * **default:** `logging.FileHandler(filepath, 'w')`
* **filecap:** defines a file cap, removing oldest files when cap is reached
  * **type:** `<int>` 
  * **default:** `None`
* **filetimeout:** defines a file time out period 
  * **type:** `<str>` 
  * **default:** `None`
  * **usage:** define a timeout period by combining time unit characters with the desired integer for a specified time unit i.e. `(10m = 10 minute, 2h = 2 hours, ...)`
  * **unit key:** `{'m': 'minutes', 'h': 'hours', 'd': 'days', 'o':'months', 'y': 'years'}`
* **file:** define if file logging is enabled 
  * **type:** `<bool>`
  * **default:** `True`
* **streamfmt:** defines the log format for the stream handler 
  * **type:** `<str>` 
  * **default:** `logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')`
* **shandler:** define a custom stream handler 
  * **type:** `<StreamHandler>`
  * **default:** `logging.StreamHandler()`
* **stream:** define if stream logging is enabled 
  * **type:** `<bool>` 
  * **default:** `False`

***

## Logger Usage Examples

</br>

***

## TO-DO
* build tests
* write git action
* document
* add version badge
* add pipeline passing / failing badge