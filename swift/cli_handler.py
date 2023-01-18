import inspect, os, argparse

class Init:
  def __init__(self, desc=None, logger=None):
    '''init top-level parser'''
    # name the program the file name of the module which is importing this class
    self.filename = os.path.basename(inspect.stack()[1].filename)[:-3]
    self.parser = argparse.ArgumentParser(prog = self.filename, description = desc) 
    self.subparsers = self.parser.add_subparsers(title='commands', dest='command') # add commands subparser
    self.func_dict = {}
    self.logger = logger

  # def add(self, func):
  #   '''create subparsers for the given function 
  #   then add arguments for each input'''

  #   # if the doc string is not empty use that to define the help string else use the default structure
  #   if func.__doc__:
  #     semip = self.subparsers.add_parser(func.__name__, help=func.__doc__)
  #   else:
  #     semip = self.subparsers.add_parser(func.__name__, help=f'execute {func.__name__} function')

  #   names = inspect.getfullargspec(func).args # collect arg names
  #   types = list(inspect.getfullargspec(func).annotations.values()) # collect types of args

  #   self.func_dict.update({func.__name__: (func, names)}) # collect function and arg names for given function

  #   # if types are provided include type requirements and a help string otherwise just add each arg with name
  #   if types:
  #     for name, type in zip(names, types):
  #       semip.add_argument(name, type=type, help=str(type))
  #   else:
  #     for name in names:
  #       semip.add_argument(name)

  #   return func
  
  def add_funcs(self, func_dict):
      self.func_dict = func_dict
      for func_name, items in func_dict.items():
        # if the doc string is not empty use that to define the help string else use the default structure
        if len(items) == 4:
          semip = self.subparsers.add_parser(func_name, help=items[-1])
        else:
          semip = self.subparsers.add_parser(func_name, help=f'execute {func_name} function')

        names = items[1] # collect arg names
        types = items[2] # collect types of arg

        # if types are provided include type requirements and a help string otherwise just add each arg with name
        if types:
          for name, type in zip(names, types):
            semip.add_argument(name, type=type, help=str(type))
        else:
          for name in names:
            semip.add_argument(name)
  
  def parse(self):
    '''initialize parsing args'''
    self.input = self.parser.parse_args()
    if self.input.command:
        func_tup = self.func_dict[self.input.command] # retrieve function and arg names for given command
        func, arg_names = func_tup[0], func_tup[1] # unpack just the args and function
        args = [getattr(self.input, arg) for arg in arg_names] # collect given args from namespace
        func(*args) # run function with given args
