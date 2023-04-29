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
            names = items[1]  # collect arg names
            types = items[2]  # collect types of arg
            arg_types = [types.get(name, None) for name in names]
            defaults = items[3]  # collect default args

            # init arg help and arg description
            ahelp = f"execute {func_name} function"

            # collect command description
            signature = inspect.signature(func_dict[func_name][0])
            params = []
            for name, param in signature.parameters.items():
                if param.annotation != inspect.Parameter.empty:
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
            if "return" in types:
                adesc = f"{func_dict[func_name][0].__name__}({', '.join(params)}) -> {str(types['return'].__name__)}"
            else:
                adesc = f"{func_dict[func_name][0].__name__}({', '.join(params)})"

            # if docstring assign arg help
            if items[-1] is not None:
                ahelp = items[-1]

            # init sub parser
            subp = self.subparsers.add_parser(
                func_name,
                help=ahelp,
                description=adesc,
                argument_default=argparse.SUPPRESS,
                add_help=False,
            )

            abbrevs = set()
            for name, atype in zip(names, arg_types):
                if name in defaults:
                    short_name = name[:2]
                    if short_name in abbrevs:
                        short_name = name[-1]
                    abbrevs.add(short_name)
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
            func_tup = self.func_dict[self.input.command]

            # unpack just the args and function
            func, arg_names = (
                func_tup[0],
                func_tup[1],
            )
            # collect given args from namespace
            args = [getattr(self.input, arg) for arg in arg_names]
            
            # run function with given args and collect any returns
            if asyncio.iscoroutinefunction(func):
                returned = asyncio.run(func(*args))
            else:
                returned = func(*args)

            # print return if not None
            if returned:
                print(returned)
            sys.exit()  # exit the interpreter so the entire script is not run
