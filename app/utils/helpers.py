import base64
import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar


def is_base64(sb: str | bytes) -> bool:
    """Return True if the input is a valid base64-encoded byte sequence.

    Accepts either str (ASCII) or bytes input. Returns False on any decode error.
    """
    try:
        if isinstance(sb, str):
            sb_bytes = sb.encode("ascii")
        elif isinstance(sb, bytes):
            sb_bytes = sb
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


def clean(txt_data: list[dict[str, str]]) -> list[dict[str, str]]:
    for index, txt in enumerate(txt_data):
        data = " ".join(txt["text"].split())
        txt_data[index]["text"] = data

    return txt_data


P = ParamSpec("P")
T = TypeVar("T")


def timeit(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def timeit_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper
