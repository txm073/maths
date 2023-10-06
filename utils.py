from typing import Iterable, Callable, Any, Optional, Union

Number = Union[int, float, complex]

def overload(*functions: Iterable[Callable]) -> Callable:
    def wrapper(*args: Iterable[Any], **kwargs: dict[Any, Any]) -> Callable:
        # Match correct overload from functions list
        arg_values = list(args) + list(kwargs.values())
        arg_types = [type(arg) for arg in arg_values]
        copy = list(functions)
        copy = list(filter(lambda fn: len(fn.__annotations__) - 1 == len(arg_values), copy))
        for fn in copy:
            annotations = fn.__annotations__
            if annotations.get("return"):
                annotations.pop("return")
            is_match = True
            for expected_type, actual_type in zip(annotations.values(), arg_types):
                if isinstance(expected_type, actual_type):
                    is_match = False
                    break
            if is_match:
                return fn(*args, **kwargs)    
        raise TypeError(
            "no overloaded function matched the given arguments"
        )
    return wrapper
