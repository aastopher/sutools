import logging, os, datetime, warnings, atexit, sys
from types import SimpleNamespace
from pathlib import Path

class Logger:
    '''object designed for swift granular logging configuration'''

    def __init__(self, name, loggers, loglvl, filename, filepath, filefmt, fhandler, filecap, filetimeout, file, streamfmt, shandler, stream):
        """Constructor method for the Logger class

        :param name: the name of the logger (str)
        :param loggers: list of names of the loggers to create (list)
        :param loglvl: the logging level to use (int)
        :param filename: the name of the log file (str)
        :param filepath: the full path of the log file (str)
        :param filefmt: the format of the log file (logging.Formatter)
        :param fhandler: the file handler to use for logging (logging.FileHandler)
        :param filecap: the maximum size of the log file in bytes (int)
        :param filetimeout: the time interval after which a new log file should be created (int)
        :param file: whether to log to a file or not (bool)
        :param streamfmt: the format of the stream (logging.Formatter)
        :param shandler: the stream handler to use for logging (logging.StreamHandler)
        :param stream: whether to log to the stream or not (bool)
        """

        # set properties
        self.name = name
        self.loggers = {}
        self.filename = filename
        self.filepath = filepath
        self.loglvl = loglvl
        self.file = file
        self.stream = stream
        self.rootlogger = logging.getLogger()
        self.filefmt = filefmt
        self.fhandler = fhandler
        self.streamfmt = streamfmt
        self.shandler = shandler

        # iterate through loggers and add each to the root logger
        for log in loggers:
            logger = logging.getLogger(log)
            logger.setLevel(loglvl)  # set logger level
            self.loggers[log] = logger
            self.rootlogger.addHandler(logger)

        # convert logger dict to namespace for easy access dot syntax
        self.loggers = SimpleNamespace(**self.loggers)
        # print(self.loggers) # debug
        self.rootlogger.setLevel(loglvl) # set default log level

        # if file property enabled create file logger
        if self.file:
            self.fhandler.setLevel(self.loglvl) # set the level of the file handler
            self.fhandler.setFormatter(self.filefmt) # set the formatter for the file handler
            for log in vars(self.loggers).keys():
                logger = logging.getLogger(log)
                logger.addHandler(self.fhandler) # add the file handler to the logger
                logger.propagate = False # disable propagation of log messages to ancestor loggers
            atexit.register(self.out) # register out function at interpreter exit
            

        # if stream property enabled create stream logger
        if self.stream:
            self.shandler.setLevel(self.loglvl) # set the log level for the stream handler
            self.shandler.setFormatter(self.streamfmt) # set the formatter for the stream handler
            for log in vars(self.loggers).keys():
                logger = logging.getLogger(log)
                logger.addHandler(self.shandler) # add the stream handler to the logger
                logger.propagate = False # disable propagation of log messages to ancestor loggers

        # if a file cap is defined and type is int run cap function
        if filecap and isinstance(filecap, int):
            self.cap(filecap) # pragma: no cover

        # if a file timout is defined and type is str run filetimeout function
        if filetimeout and isinstance(filetimeout, str):
            self.timeout(filetimeout) # pragma: no cover

    def cap(self, filecap):
        '''delete any file outside of range based on file age'''

        # parent_folder = Path(self.filepath).parent # collect the parent folder for the log path
        parent_folder = os.path.dirname(self.filepath)

        # create list of tuples with filename and its creation time for all files ending with '.log' in parent folder
        logs = [(os.path.join(parent_folder, f), os.path.getctime(os.path.join(parent_folder, f))) for f in os.listdir(parent_folder) if f.endswith('.log')]
        logs.sort(key=lambda x: x[1], reverse=True) # sort the logs by their creation time in descending order

        # if files have exceeded the cap
        if len(logs) > filecap:
            logs_to_remove = len(logs) - filecap # calculate the number of logs to remove
            for log in logs[filecap:]:
                os.remove(log[0]) # remove file
            if logs_to_remove > 1:
                print(f'filecap removed {logs_to_remove} logs') # print the number of removed files if greater than 1
            else:
                print("filecap reached") # print if filecap is reached

    def timeout(self, filetimeout):
        '''delete any file outside given time range'''
        try:
            # get the path of the parent folder and find all log files in it
            # parent_folder = Path(self.filepath).parent
            parent_folder = os.path.dirname(self.filepath)
            logs = [os.path.join(parent_folder, f) for f in os.listdir(parent_folder) if f.endswith('.log')]

            # define time units and extract the amount and unit of the file timeout.
            time_units = {'m': 'minutes', 'h': 'hours', 'd': 'days', 'o':'months', 'y': 'years'}
            time_unit = time_units[filetimeout[-1]]
            time_amount = int(filetimeout[:-1])

            # get the current time and calculate the time threshold based on the file timeout
            now = datetime.datetime.now()
            if time_unit == 'years':
                time_threshold = now - datetime.timedelta(days=time_amount*365)
            elif time_unit == "minutes":
                time_threshold = now - datetime.timedelta(minutes=time_amount)
            elif time_unit == 'months':
                time_threshold = now - datetime.timedelta(days=time_amount*30)
            else:
                time_threshold = now - datetime.timedelta(**{time_unit: time_amount})

            # remove all logs that are older than the time threshold and count the number of logs removed
            logs_removed = 0
            for log in logs:
                if os.path.getctime(log) < time_threshold.timestamp():
                    os.remove(log)
                    logs_removed += 1
            
            # print the number of logs that were removed if any
            if logs_removed > 0:
                print(f'timeout removed {logs_removed} logs')

        except KeyError:
            # warn the user if an invalid time unit is provided
            warnings.warn(f"Invalid time unit: {filetimeout[-1]}", Warning)
    
    def out(self):
        """
        Check all loggers in the loggers namespace object for existing logs.
        If none exist, close the file fhandlers and remove the empty file
        """
        # check each logger for existing handlers and set to null if they exist
        for log in vars(self.loggers).values():
            if log.hasHandlers():
                for fhandler in log.handlers:
                    fhandler.close()
                log.handlers = []
        
        # check if the log file is empty and remove it
        try:
            file_size = os.path.getsize(self.filepath)
            if file_size == 0:
                os.remove(self.filepath)
        except Exception as e: # pragma: no cover
            # print an error message if the file cannot be removed
            print(f"Failed to remove file: {e}") # pragma: no cover

        # check if the module folder is empty and remove it
        try:
            m_folder = os.path.dirname(self.filepath)
            if not os.listdir(m_folder): # check if folder is empty
                os.rmdir(m_folder) # remove empty folder # pragma: no cover
        except Exception as e: # pragma: no cover
            # print an error message if the folder cannot be removed
            print(f"Failed to remove module folder: {e}") # pragma: no cover

        # check if the log folder is empty and remove it
        try:
            l_folder = os.path.dirname(os.path.dirname(self.filepath))
            if not os.listdir(l_folder): # check if folder is empty
                os.rmdir(l_folder) # remove empty folder # pragma: no cover
        except Exception as e: # pragma: no cover
            # print an error message if the folder cannot be removed
            print(f"Failed to remove log folder: {e}") # pragma: no cover

    def __enter__(self): # pragma: no cover
        if not self.rootlogger.handlers: # pragma: no cover
            self.rootlogger.addHandler(logging.NullHandler()) # pragma: no cover
        return self # pragma: no cover

    def __exit__(self, exc_type, exc_value, traceback): # pragma: no cover
        logging.shutdown() # pragma: no cover