# https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting

import logging, os, argparse, datetime, inspect

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M-%S")

# DL = DeepLogger('connection',['decrypt','socket','connect'])
# decryptLogger = DL.getLogger('decrypt')
# socketLogger = DL.getLogger('socket')
# connectLogger = DL.getLogger('connect')

# print(os.path.basename(inspect.stack()[-1].filename)[:-3])

class Init:
    def __init__(self, log_name=None, loggers=None):

        # self.args, self.parser = self._cli_config()

        # if not log_name:
        #     self.log_name = os.path.basename(inspect.stack()[-1].filename)[:-3]
        # else:
        #     self.log_name = log_name

        # if not loggers:
        #     self.loggers = ['default']
        # else:
        #     self.loggers = loggers

        # root = logging.getLogger()
        # root.setLevel(logging.DEBUG)
        # self.log_lvl = self.args.log_level
        # self._logging_config()



        self.args, self.parser = self._cli_config()
        if not self.args.command:
            self.loggers = loggers

            if not log_name:
                self.log_name = os.path.basename(inspect.stack()[-1].filename)[:-3]
            else:
                self.log_name = log_name

            root = logging.getLogger()
            root.setLevel(logging.DEBUG)
            self.console_logger = logging.getLogger(f'console_{self.log_name}')
            sh = logging.StreamHandler()
            sh.setLevel(logging.INFO)
            self.console_logger.addHandler(sh)
        else:
            self.log_lvl = self.args.log_level
            self.loggers = loggers
            self.log_name = log_name
            self._logging_config()

        

    def getLogger(self,logger_name):
        return logging.getLogger(logger_name)
    def _logging_config(self):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        if not os.path.exists('logs'):
            os.mkdir('logs')
        if not os.path.exists(f'logs/{self.log_name}'):
            os.mkdir(f'logs/{self.log_name}')
        fh = logging.FileHandler(f'logs/{self.log_name}/{self.log_name}_{now}.log','w')
        fh.setLevel(self.log_lvl)
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
        fh.setFormatter(formatter)
        for log in self.loggers:
            logger = logging.getLogger(f'{log}')
            logger.addHandler(fh)
        # self.console_logger = logging.getLogger(f'console_{self.log_name}')
        # sh = logging.StreamHandler()
        # sh.setLevel(logging.INFO)
        # self.console_logger.addHandler(sh)
    def _cli_config(self):
        def _add_options(parser):
            parser.add_argument('-v', '--verbose', help='adds verbose logging to output logs', action='store_const', dest='log_level', const=logging.DEBUG, default=logging.INFO)

        parser = argparse.ArgumentParser(description= f'EZ Logger and CLI')
        subparser = parser.add_subparsers(dest='command', metavar= '<command>', help='valid choices: {log} options: {-v}')

        self.log_command = subparser.add_parser('log')
        self.log_command.add_argument('log', help='output logs', action= 'store_true')
        _add_options(self.log_command)

        return parser.parse_args(), parser

class DeepLogger:
    def __init__(self,log_name,loggers):
        self.args, self.parser = self._cli_config()
        if not self.args.command:
            self.loggers = loggers
            self.log_name = log_name
            root = logging.getLogger()
            root.setLevel(logging.DEBUG)
            self.console_logger = logging.getLogger(f'console_{self.log_name}')
            sh = logging.StreamHandler()
            sh.setLevel(logging.INFO)
            self.console_logger.addHandler(sh)
        else:
            self.log_lvl = self.args.log_level
            self.loggers = loggers
            self.log_name = log_name
            self._logging_config()
    def getLogger(self,logger_name):
        return logging.getLogger(logger_name)
    def _logging_config(self):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        if not os.path.exists('logs'):
            os.mkdir('logs')
        if not os.path.exists(f'logs/{self.log_name}'):
            os.mkdir(f'logs/{self.log_name}')
        fh = logging.FileHandler(f'logs/{self.log_name}/{self.log_name}_{now}.log','w')
        fh.setLevel(self.log_lvl)
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
        fh.setFormatter(formatter)
        for log in self.loggers:
            logger = logging.getLogger(f'{log}')
            logger.addHandler(fh)
        self.console_logger = logging.getLogger(f'console_{self.log_name}')
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        self.console_logger.addHandler(sh)
    def _cli_config(self):
        def _add_options(parser):
            parser.add_argument('-v', '--verbose', help='adds verbose logging to output logs', action='store_const', dest='log_level', const=logging.DEBUG, default=logging.INFO)

        parser = argparse.ArgumentParser(description= f'EZ Logger and CLI')
        subparser = parser.add_subparsers(dest='command', metavar= '<command>', help='valid choices: {log} options: {-v}')

        self.log_command = subparser.add_parser('log')
        self.log_command.add_argument('log', help='output logs', action= 'store_true')
        _add_options(self.log_command)

        return parser.parse_args(), parser