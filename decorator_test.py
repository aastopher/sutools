import argparse
import functools
import os
import inspect

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        print(func.__doc__)
        print(os.path.basename(__file__)[:-3])
        print(inspect.getfullargspec(func).annotations)
        func(*args, **kwargs)
    return wrapper


@my_decorator
def echo(string: str):
    '''echo a string'''
    print(string)

@my_decorator
def add(x : int, y : int):
    '''add two integers'''
    print(x + y)

echo('something')
add(1,2)