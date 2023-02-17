import inspect, os, argparse, logging, sys

class CLI:
  '''object designed for swift module CLI configuration'''

  def __init__(self, desc, logs, log_obj = None):
    '''init top-level parser'''

    # define the name of the cli application as the file name of the module which is importing this class
    self.name = os.path.basename(inspect.stack()[1].filename)[:-3] # define the name of the cli application
    self.parser = argparse.ArgumentParser(prog = self.name, description = desc) # define root parser
    self.subparsers = self.parser.add_subparsers(title='commands', dest='command') # add commands subparser
    self.func_dict = {} # init empty func dict
    self.log_obj = log_obj # store copy of the log object for logging compatibility
    self.log = log_obj.loggers # extract functional logger list

    # toggles logs for cli commands
    if not logs:
      for logger in vars(self.log).values(): # iterates through all loggers
        logger.setLevel(logging.CRITICAL+1) # sets logs to 1 above critical i.e. 51

  def add_funcs(self, func_dict):
      '''add registered functions to the cli'''

      self.func_dict = func_dict # assign function dictionary property

      # iterate through registered functions
      for func_name, items in func_dict.items():


        # define sub-parsers:
        # if doc string exists define it as the help string 
        # else use a default structure
        if len(items) == 4:
          subp = self.subparsers.add_parser(func_name, help=items[-1])
        else:
          subp = self.subparsers.add_parser(func_name, help=f'execute {func_name} function')

        names = items[1] # collect arg names
        types = items[2] # collect types of arg

        # define args for sub-parser:
        # if types are provided include type requirements and a help string 
        # otherwise just add each arg with just a name
        if types:
          for name, type in zip(names, types):
            subp.add_argument(name, type=type, help=str(type))
        else:
          for name in names:
            subp.add_argument(name)
  
  def parse(self):
    '''initialize parsing args'''

    self.input = self.parser.parse_args() # parse

    # if command in input namespace
    if self.input.command:
        func_tup = self.func_dict[self.input.command] # retrieve function and arg names for given command
        func, arg_names = func_tup[0], func_tup[1] # unpack just the args and function
        args = [getattr(self.input, arg) for arg in arg_names] # collect given args from namespace
        func(*args) # run function with given args
        sys.exit() # exit the interpreter so the entire script is not run