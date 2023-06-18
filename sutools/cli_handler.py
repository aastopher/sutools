import inspect, os, argparse, logging, sys, asyncio


class CLI:
    """object designed for swift module CLI configuration"""

    def __init__(self, desc, logs, log_obj=None):
        """init top-level parser"""

        # define the name of the cli application as the file name of the module which is importing this class
        self.name = os.path.basename(inspect.stack()[-1].filename)[:-3]
        # define root parser
        self.parser = argparse.ArgumentParser(prog=self.name, description=desc)
        # add commands subparser
        self.subparsers = self.parser.add_subparsers(title="commands", dest="command")
        self.func_dict = {}  # init empty func dict
        self.log_obj = log_obj  # store copy of the log object for logging compatibility
        self.input = None

        if log_obj:
            self.log = log_obj.loggers  # extract functional logger list

        # toggles logs for cli commands
        if not logs and log_obj:
            for logger in vars(self.log).values():  # iterates through all loggers
                logger.setLevel(
                    logging.CRITICAL + 1
                )  # sets logs to 1 above critical i.e. 51

    def add_funcs(self, func_dict):
        """add registered functions to the cli"""

        self.func_dict = func_dict  # assign function dictionary property

        # iterate through registered functions
        for func_name, items in func_dict.items():
            names = items['names']  # collect arg names
            types = items['types']  # collect types of arg
            arg_types = [types.get(name, None) for name in names]
            defaults = items['defaults']  # collect default args

            # init arg help and arg description
            ahelp = f"execute {func_name} function"

            # collect command description
            signature = inspect.signature(func_dict[func_name]['func'])

            # collect names and params for a given function
            params = []
            for name, param in signature.parameters.items():
                
                # check if function contains annotations
                if param.annotation != inspect.Parameter.empty:
                    # if default arg exists display in docs
                    if param.default != inspect.Parameter.empty:
                        params.append(
                            f"{name}: {param.annotation.__name__} = {param.default!r}"
                        )
                    else:
                        params.append(f"{name}: {param.annotation.__name__}")
                else:
                    if param.default != inspect.Parameter.empty:
                        params.append(f"{name} = {param.default!r}")
                    else:
                        params.append(f"{name}")

            # define return type if exists for docs
            if "return" in types:
                adesc = f"{func_dict[func_name]['func'].__name__}({', '.join(params)}) -> {str(types['return'].__name__)}"
            else:
                adesc = f"{func_dict[func_name]['func'].__name__}({', '.join(params)})"

            # define help string
            if items['desc'] is not None:
                ahelp = items['desc']

            # init sub parser
            subp = self.subparsers.add_parser(
                func_name,
                help=ahelp,
                description=adesc,
                argument_default=argparse.SUPPRESS,
                add_help=False,
            )

            # create abbreviations for named short name
            abbrevs = set()
            for name, atype in zip(names, arg_types):
                # if arg is contains a default define a short name
                if name in defaults:
                    # default abbreviation is the first 2 characters
                    short_name = name[:2]
                    # if space is taken define short name as just the list character
                    if short_name in abbrevs:
                        short_name = name[-1]
                    abbrevs.add(short_name)

                    # if there exists a short name with the same first and 
                    # last chars do not define one
                    try:
                        subp.add_argument(
                            f"-{short_name}",
                            f"--{name}",
                            metavar=str(atype) if atype is not None else None,
                            type=atype,
                            default=defaults[name],
                            help=f"default: {defaults[name]}",
                        )
                    except argparse.ArgumentError:
                        subp.add_argument(
                            f"--{name}",
                            metavar=str(atype) if atype is not None else None,
                            type=atype,
                            default=defaults[name],
                            help=f"default: {defaults[name]}",
                        )
                else:
                    # if variadic allow any number of args
                    if items['variadic']:
                        subp.add_argument(
                            name, nargs='*', type=atype, help=str(atype) if atype is not None else None
                        )
                    else:
                        subp.add_argument(
                            name, type=atype, help=str(atype) if atype is not None else None
                        )

            # overide help & place at end of options
            subp.add_argument(
                "-h", "--help", action="help", help="Show this help message and exit."
            )

    def parse(self):
        """initialize parsing args"""

        self.input = self.parser.parse_args()

        # if command in input namespace
        if self.input.command:
            # retrieve function and arg names for given command
            func_meta = self.func_dict[self.input.command]
            args = []
            kwargs = {}

            # if variadic define args and kwargs
            if func_meta['variadic']:
                func = func_meta['func']
                try:
                    for arg in vars(self.input)['*args']:
                        if '=' in arg:
                            k,v = arg.split('=')
                            kwargs[k] = v
                        else:
                            args.append(arg)
                except KeyError:
                    # pass because args & kwargs are already defined empty
                    pass
            else:

                # unpack just the args and function
                func, arg_names = (
                    func_meta['func'],
                    func_meta['names'],
                )
            
                # collect args from input namespace
                args = [getattr(self.input, arg) for arg in arg_names]
            
            # run function with given args and collect any returns
            if asyncio.iscoroutinefunction(func):
                returned = asyncio.run(func(*args, **kwargs))
            else:
                returned = func(*args, **kwargs)

            # print return if not None
            if returned:
                print(returned)

            # exit the interpreter so the entire script is not run
            sys.exit() 
