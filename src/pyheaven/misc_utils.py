from .basic_utils import *
import re
import time
import string
import random
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

def Clipped(value, l, r):
    """Return a clipped value between lower bound `l` and upper bound `r`.

    Args:
        value: A value.
        l: The lower bound.
        u: The upper bound.
    Returns:
        Any: The clipped value.
    """
    return min(max(value,l),r)