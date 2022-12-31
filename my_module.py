"""This module does random stuff."""


import cli as sw
import inspect

# scli = sw.CLI()
scli = sw.CLI(__doc__)
# scli = sw.CLI('custom desc')

@scli.parse
def echo(string: str):
    '''echo a string'''
    print(string)

@scli.parse
def add(x : int, y : int):
    '''add two integers'''
    print(x + y)

@scli.parse
def minus(x : int, y : int):
    print(x - y)

@scli.parse
def do():
  print(f'do {inspect.stack()[0][3]}')

scli.init_parser()

# print('debug this')

if __name__ == '__main__':
    pass