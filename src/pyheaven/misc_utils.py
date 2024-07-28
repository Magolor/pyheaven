from .basic_utils import *
import re
import time
import string
import random
import hashlib
Import("tqdm",globals())
Import("requests",globals())

def RandString(length:int, charset:str=string.ascii_uppercase + string.digits):
    """Return a random string.

    Args:
        length (int): Length of the random string.
        charset (str): The alphabet. Notice that if a word appears multiple times, the probability that it is chosen also multiples.
    Returns:
        str: A random string of length `length`, with all characters chosen from `charset`.
    """
    return ''.join(random.choice(charset) for _ in range(length))

def LineToFloats(line:str):
    """Read all float numbers from a line of text.

    Args:
        line (str): A line of text.
    Returns:
        List: All float numbers find in the line.
    """
    return [float(s) for s in re.findall(r"(?<!\w)[-+]?\d*\.?\d+(?!\d)",line)]

def FlattenList(L:List):
    """Flatten an embedded list to a 1D list.

    Args:
        L: The embedded list to be flattened.
    Returns:
        List: The flattened list.
    """
    F = lambda x:[e for i in x for e in F(i)] if isinstance(x,list) else [x]; return F(L)

def IP():
    """Return IP address string of the current device.

    Args:
        None
    Returns:
        str: The IP address string of the current device.
    """
    return requests.get('https://api.ipify.org').text

def FORMATTED_TIME(format="[%Y-%m-%d_%H.%M.%S]"):
    """Return the formatted current time.

    Args:
        format (str): The time format.
    Returns:
        str: The formatted current time.
    """
    return time.strftime(format,time.localtime(time.time()))

def Clipped(value, l, u):
    """Return a clipped value between lower bound `l` and upper bound `u` (closed).

    Args:
        value: A value.
        l: The lower bound.
        u: The upper bound.
    Returns:
        Any: The clipped value.
    """
    return min(max(value,l),u)

def Unique(ls:List, **sort_args):
    """Return a sorted list of unique elements.

    Args:
        ls (List): The input list (or other iterable).
        sort_args: Args for calling `sorted` on the subpaths in format of (path, full_path), only works if `ordered` is True. Notice that the sort function will only be applied at the base level instead of applied recursively. PPlease refer to function `BUILTIN_LISTPATHS_SORT_CRITERIA()` for built-in criteria.
    Returns:
        List: The sorted list of unique elements.
    """
    return sorted(list(set(ls)), **sort_args)

def TQDM(obj, **args):
    """Return a tqdm pbar, both iterable and int are supported for obj.

    Args:
        ls (List): The object to be tracked using tqdm.
        args: args for calling `tqdm.tqdm` on the object (or range).
    Returns:
        tqdm.tqdm: The tqdm pbar.
    """
    if 'dynamic_ncols' not in args:
        args['dynamic_ncols'] = True
    if isinstance(obj, int):
        return tqdm.tqdm(range(obj), **args)
    else:
        return tqdm.tqdm(obj, **args)


def PrintFile(file_handle, *args, **kwargs):
    """Print to a file_handle with auto-flush.

    Args:
        *args, **kwargs: arguments used in `print`.
    Returns:
        None
    """
    if 'flush' not in kwargs:
        kwargs['flush'] = True
    print(args, file=file_handle, **kwargs)


def PrintConsole(*args, **kwargs):
    """Print to stdout with auto-flush.

    Args:
        *args, **kwargs: arguments used in `print`.
    Returns:
        None
    """
    if 'flush' not in kwargs:
        kwargs['flush'] = True
    print(args, file=sys.stdout, **kwargs)


def PrintError(*args, **kwargs):
    """Print to stderr with auto-flush.

    Args:
        *args, **kwargs: arguments used in `print`.
    Returns:
        None
    """
    if 'flush' not in kwargs:
        kwargs['flush'] = True
    print(args, file=sys.stderr, **kwargs)


def Attempt(f, retry_time=1, retry_gap=0.0, default=None, verbose=False, *args, **kwargs):
    """Attempt to run a function with retry.
    
    Args:
        f: The function to be attempted.
        retry_time (int): The maximum number of retries. If `retry_time` is 0, the function will be executed only once. If `retry_time` is smaller than 0, the function will be executed indefinitely until it succeeds.
        retry_gap (float): The time gap between retries.
        default: The default return value if all retries fail.
        verbose (bool): If True, print the error message.
        *args, **kwargs: The arguments for the function.
    Returns:
        Any: The return value of the function. If all retries fail, return `default`.
    """
    while retry_time != 0:
        try:
            return f(*args, **kwargs)
        except KeyboardInterrupt as e:
            exit(0)
        except Exception as e:
            if verbose:
                print(e)
            if retry_gap > 0.0:
                time.sleep(retry_gap)
            retry_time -= 1
    return default


def PartialFormat(string, **kwargs):
    """Partially format a string.
    
    Args:
        string (str): The string to be formatted.
        **kwargs: The key-value pairs to be replaced.
    Returns:
        str: The formatted string.
    """
    for key, value in kwargs.items():
        string = string.replace(f"{{{key}}}", f'{value}')
    return string


def NORMAL(obj):
    """Format an object into string of normal color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return str(obj)


def ERROR(obj):
    """Format an object into string of error color (red) in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;31m' + str(obj) + '\x1b[0m'


def SUCCESS(obj):
    """Format an object into string of success color (green) in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;32m' + str(obj) + '\x1b[0m'


def WARNING(obj):
    """Format an object into string of warning color (yellow) in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;33m' + str(obj) + '\x1b[0m'


def COLOR1(obj):
    """Format an object into string of highlight color 1 (blue) in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;34m' + str(obj) + '\x1b[0m'


def COLOR2(obj):
    """Format an object into string of highlight color 2 (magenta) in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;35m' + str(obj) + '\x1b[0m'


def COLOR3(obj):
    """Format an object into string of highlight color 3 (cyan) in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;36m' + str(obj) + '\x1b[0m'


def BLACK(obj):
    """Format an object into string of black color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;30m' + str(obj) + '\x1b[0m'


def RED(obj):
    """Format an object into string of red color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;31m' + str(obj) + '\x1b[0m'


def GREEN(obj):
    """Format an object into string of green color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;32m' + str(obj) + '\x1b[0m'


def YELLOW(obj):
    """Format an object into string of yellow color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;33m' + str(obj) + '\x1b[0m'


def BLUE(obj):
    """Format an object into string of blue color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;34m' + str(obj) + '\x1b[0m'


def MAGENTA(obj):
    """Format an object into string of magenta color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;35m' + str(obj) + '\x1b[0m'


def CYAN(obj):
    """Format an object into string of cyan color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;36m' + str(obj) + '\x1b[0m'


def WHITE(obj):
    """Format an object into string of white color in console.

    Args:
        obj: the object to be formatted.
    Returns:
        None
    """
    return '\x1b[1;37m' + str(obj) + '\x1b[0m'


def MD5(key, salt=None):
    """Generate the integer md5 hash value for an arbitrary key.
    It is recommended that the `key` supports string conversion. Otherwise, the same `key` with different memory addresses will have different hash values.
    
    Args:
        key: The key to be hashed.
        salt: The salt to be added to the key before hashing.
    Returns:
        int: The integer hash value.
    """
    return int(hashlib.md5((f"{key}" if salt is None else f"{key}|{salt}").encode('utf-8')).hexdigest(), 16)
