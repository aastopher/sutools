import time

class Benchy:
    '''decorator class for collecting benchmark reports'''
    def __init__(self):
        self.report = {}

    @staticmethod
    def summarize(data):
        '''summarize iterable data'''
        if hasattr(data, '__iter__'):
            return {'type': type(data).__name__, 'length': len(data)}
        else:
            return {'type': type(data).__name__, 'value': data}

    def func_meta(self, data):
        '''collect args / kwargs meta info & summarize inputs'''
        if not data:
            return None
        elif isinstance(data, dict):
            return {k: self.summarize(v) for k, v in data.items()}
        else:
            return [self.summarize(arg) for arg in data]

    def __call__(self, func):
        '''benchmark and store report for called function'''

        # collect original function if already wrapped
        original_func = getattr(func, "__wrapped__", func)

        def wrapper(*args, **kwargs):

            # benchmark the function
            start_time = time.perf_counter()
            result = original_func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            # check if report exists for func
            if original_func.__name__ not in self.report:
                self.report[original_func.__name__] = []

            # collect benchmark, args, kwargs, results summaries
            self.report[original_func.__name__].append({
                'benchmark': elapsed_time,
                'args': self.func_meta(args),
                'kwargs': self.func_meta(kwargs),
                'result': self.summarize(result)
            })

            return result

        # re-wrap original function
        wrapper.__wrapped__ = original_func
        return wrapper