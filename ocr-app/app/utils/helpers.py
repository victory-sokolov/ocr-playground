import base64
import time
from functools import wraps
from typing import Callable


def is_base64(sb: str) -> bool:
    sb_bytes = None
    try:
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, "ascii")
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
    except Exception:
        return False
    return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes


def clean(txt_data: list[dict[str, str]]):
    for index, txt in enumerate(txt_data):
        data = " ".join(txt["text"].split())
        txt_data[index]["text"] = data

    return txt_data


def timeit(func: Callable):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper
