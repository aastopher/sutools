import inspect
import os
import argparse

class CLI():
  def __init__(self, desc=None):
    '''init top-level parser'''
    # name the program the file name of the module which is importing this class
    self.filename = os.path.basename(inspect.stack()[1].filename)[:-3]
    self.parser = argparse.ArgumentParser(prog = self.filename, description = desc) 
    self.subparsers = self.parser.add_subparsers(title='commands', dest='command') # add commands subparser
    self.func_dict = {}
    self.args_dict = {}

  def parse(self, func):
    '''create subparsers for the given function 
    then add arguments for each input'''

    # if the doc string is not empty use that to define the help string else use the default structure
    if func.__doc__:
      semip = self.subparsers.add_parser(func.__name__, help=func.__doc__)
    else:
      semip = self.subparsers.add_parser(func.__name__, help=f'execute {func.__name__} function')

    names = inspect.getfullargspec(func).args # collect arg names
    types = list(inspect.getfullargspec(func).annotations.values()) # collect types of args

    self.func_dict.update({func.__name__: func})
    self.args_dict.update({func.__name__: names})

    # if types are provided include type requirements and a help string otherwise just add each arg with name
    if types:
      for name, type in zip(names, types):
        semip.add_argument(name, type=type, help=str(type))
    else:
      for name in names:
        semip.add_argument(name)

    return func
  
  def init_parser(self):
    '''initialize parsing args'''
    self.input = self.parser.parse_args()

    func = self.func_dict[self.input.command] # collect the function
    arg_names = self.args_dict[self.input.command] # collect arg names for given command
    args = [getattr(self.input, arg) for arg in arg_names] # collect given args from namespace in list
    func(*args) # run function with given args
