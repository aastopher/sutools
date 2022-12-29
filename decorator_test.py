import argparse
import functools
import os
import inspect

class CLI():
    def __init__(self):
        self.args = []

cli = CLI()

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        print(func.__doc__)
        print(os.path.basename(__file__)[:-3])
        print(inspect.getfullargspec(func).annotations)
        func(*args, **kwargs)
    return wrapper

def add_arg(func):
    cli.args.append(func.__name__)

@add_arg
def echo(string: str):
    '''echo a string'''
    print(string)

@add_arg
def add(x : int, y : int):
    '''add two integers'''
    print(x + y)

# echo('something')
# add(1,2)

print(cli.args)


#### TEST CLI ####

# # Create the top-level parser
# parser = argparse.ArgumentParser(prog='PROG')
# subparsers = parser.add_subparsers(title='commands', dest='command')

# # Create the parser for the "echo" command
# parser_echo = subparsers.add_parser('echo', help='Echo a string')
# parser_echo.add_argument('string', type=str, help='The string to echo')

# # Create the parser for the "add" command
# parser_add = subparsers.add_parser('add', help='Add two integers')
# parser_add.add_argument('x', type=int, help='The first integer')
# parser_add.add_argument('y', type=int, help='The second integer')

# # Parse the arguments
# args = parser.parse_args()

# # Execute the appropriate command
# if args.command == 'echo':
#     print(args.string)
# elif args.command == 'add':
#     print(args.x + args.y)


# swift cli could wrap argparse to dynamically create command parsers for each given function
# defining the program name as the file name and the function name as the command 
# as well as defining the function input requirements as the arguments

# this would be the ideal swift cli definition for a series of functions
# scli([echo, add])
