
from .cache_logic import cache_logic
from .utils import get_args_to_hash
# Dictionary are not hasable and the python hash is not consistent
# between runs so we have to use an external dictionary hasing package
# else we will not be able to load the saved caches.
from dict_hash import sha256

def decore_function(func, load, dump, function_info, cache_path, args_to_ignore, args_name):
    def wrapped(*args, **kwargs):
        to_hash = get_args_to_hash(args_name, args, kwargs, args_to_ignore)
        # Hash the arguments and function informations
        _hash = sha256({"params":to_hash, "function_info":function_info})
        # Compute the path of the cache for these parameters
        path = cache_path.format(
            _hash=_hash,
            function_name=func.__name__,
            **function_info,
            **to_hash
            )
        return cache_logic(path, func, args, kwargs, load, dump)
    return wrapped

def decore_method(func, load, dump, function_info, cache_path, args_to_ignore, args_name):
    def wrapped(self, *args, **kwargs):
        to_hash = get_args_to_hash(args_name, args, kwargs, args_to_ignore)
        # Hash the arguments and function informations
        _hash = sha256({"params":to_hash, "function_info":function_info})
        # Compute the path of the cache for these parameters
        path = cache_path.format(
            _hash=_hash,
            function_name=func.__name__,
            **function_info,
            **to_hash,
            **vars(self)
            )
        # merge self to the other args
        args = [self] + list(args)
        return cache_logic(path, func, args, kwargs, load, dump)
    return wrapped
