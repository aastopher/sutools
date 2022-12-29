import inspect
import os

class CLI:
  def __init__(self):
    self.functions = []
    self.docs = []
    self.files = []
    self.dtypes = []
    
  def add(self, func):
    self.functions.append(func.__name__)
    self.docs.append(func.__doc__)
    self.files.append(os.path.basename(inspect.getfile(func))[:-3])
    self.dtypes.append(inspect.getfullargspec(func).annotations.values())
    # print(os.path.basename(__file__)[:-3])
    return func

cli = CLI()

@cli.add
def echo(string: str):
    '''echo a string'''
    print(string)

@cli.add
def add(x : int, y : int):
    '''add two integers'''
    print(x + y)

print(cli.functions)
print(cli.docs)
print(cli.files)
print(cli.dtypes)
