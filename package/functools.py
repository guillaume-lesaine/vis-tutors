import inspect
import pandas as pd

def show_function(func):
    '''Decorator to print function call details - parameters names and effective values'''

    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments 
        func_args = list(func_args.items())
        func_args = [(x[0], 'HIDDEN') if isinstance(x[1], pd.DataFrame) else x for x in func_args]
        func_args_str =  ', '.join('{} = {!r}'.format(*item) for item in func_args) # Avoid the dataframe
        print(f'-------------- {func.__qualname__} ( {func_args_str} )')
        return func(*args, **kwargs)

    return wrapper
