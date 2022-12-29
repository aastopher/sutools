import argparse
import functools
import os
import inspect


#### TEST CLI ####

# Create the top-level parser
parser = argparse.ArgumentParser(prog='PROG')
subparsers = parser.add_subparsers(title='commands', dest='command')

# Create the parser for the "echo" command
parser_echo = subparsers.add_parser('echo', help='Echo a string')
parser_echo.add_argument('string', type=str)

# Create the parser for the "add" command
parser_add = subparsers.add_parser('add', help='Add two integers')
parser_add.add_argument('x', type=int)
parser_add.add_argument('y', type=int)

# Parse the arguments
args = parser.parse_args()

# Execute the appropriate command
if args.command == 'echo':
    print(args.string)
elif args.command == 'add':
    print(args.x + args.y)


# swift cli could wrap argparse to dynamically create command parsers for each given function
# defining the program name as the file name and the function name as the command 
# as well as defining the function input requirements as the arguments

# this would be the ideal swift cli definition for a series of functions
# scli([echo, add])
