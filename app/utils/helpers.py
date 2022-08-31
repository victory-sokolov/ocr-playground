import time
from functools import wraps


def clean(txt_data):
    for index, txt in enumerate(txt_data):
        data = " ".join(txt["text"].split())
        txt_data[index]["text"] = data

    return txt_data



def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper
