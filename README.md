# Description
**su (Super User) tools**

Per module utilities, designed to be lightweight, easy to configure, and reduce boilerplate code.

***

## Install
```
pip install sutools
```
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
* **name:** name of root module logger defines the name of log subfolder | `<str>` | default = `module file name`
* **loggers:** names of functional loggers | `<str>` | default = `names of registered functions`
* **loglvl:** optionally pass in your own log level this can also be an integer. Check out the defined [log levels](https://docs.python.org/3/library/logging.html#logging-levels) | `<int>` | default = `logging.INFO`
* **filename:** defines name of log file instances | `<str>` | default = `datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')`
* **filepath:** defines path for log files | `<str>`, `<Path>` | default = `logs/name_of_logger/filename`
* **filefmt:** defines the log format for the file handler | `<Formatter>` | default = `logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')`
* **fhandler:** define a custom file handler | `<FileHandler>` | default = `logging.FileHandler(filepath, 'w')`
* **filecap:** defines a file cap, removing oldest files when cap is reached | `<int>` | default = `None`
* **filetimeout:** defines a file time out period | `<str>` | default = `None`
  * define a timeout period by combining time unit characters with the desired integer for a specified time unit i.e. (10m = 10 minute, 2h = 2 hours, ...)
  * time_units = {'m': 'minutes', 'h': 'hours', 'd': 'days', 'o':'months', 'y': 'years'}
* **file:** define if file logging is enabled | `<bool>` | default = `True`
* **streamfmt:** defines the log format for the stream handler | `<str>` | default = `logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')`
* **shandler:** define a custom stream handler | `<StreamHandler>` | default = `logging.StreamHandler()`
* **stream:** define if stream logging is enabled | `<bool>` | default = `False`

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