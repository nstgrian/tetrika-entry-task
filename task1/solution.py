from functools import wraps
from inspect import signature


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        annotations = func.__annotations__.copy()
        if "return" in annotations:
            annotations.pop('return')

        for param_name, expected_type in annotations.items():
            actual_value = bound.arguments[param_name]
            if type(actual_value) is not expected_type:
                raise TypeError(
                    f"Argument '{param_name}' must be {expected_type.__name__}, "
                    f"got {type(actual_value).__name__}"
                )

        return func(*args, **kwargs)

    return wrapper
