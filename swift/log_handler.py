import logging, os, datetime
from types import SimpleNamespace

class Logger:
    def __init__(self, module_name, logger_names, filefmt, loglvl, formatter):
        self.module_name = module_name
        self.loggers = {}
        self.loglvl = loglvl
        self.root_logger = logging.getLogger()
        self.formatter = formatter
        for name in logger_names:
            logger = logging.getLogger(name)
            self.loggers[name] = logger
            self.root_logger.addHandler(logger)

        now = datetime.datetime.now()
        now = now.strftime(filefmt)
        self.root_logger.setLevel(loglvl)
        if not os.path.exists('logs'):
            os.mkdir('logs')
        if not os.path.exists(f'logs/{self.module_name}'):
            os.mkdir(f'logs/{self.module_name}')
        fh = logging.FileHandler(f'logs/{self.module_name}/{now}.log','w')
        # fh = logging.TimedRotatingFileHandler(f'logs/{self.module_name}/{now}.log','w', when='midnight')
        fh.setLevel(self.loglvl)
        fh.setFormatter(self.formatter)
        for log in self.loggers.keys():
            logger = logging.getLogger(log)
            logger.addHandler(fh)
            logger.propagate = False
        self.loggers = SimpleNamespace(**self.loggers)