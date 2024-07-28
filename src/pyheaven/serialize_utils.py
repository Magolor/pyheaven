from .file_utils import *
import json
import pickle
Import("demjson",globals())
Import("jsonlines",globals())
Import("simplejson",globals())
Import("jsonpickle",globals())

def BUILTIN_JSON_BACKENDS():
    return ['json','jsonl','demjson','simplejson','jsonpickle']
def BUILTIN_JSON_PRETTIFY_BACKENDS():
    return ['json',        'demjson','simplejson','jsonpickle']
def SaveJson(obj, path, backend:Literal['json','jsonl','demjson','simplejson','jsonpickle']='json', indent:Optional[int]=None, append:bool=False, *args, **kwargs):
    """Save an object as json (or jsonl) file.

    Args:
        obj: The object to be saved.
        path: The save path.
        backend (str): Specify backend for saving an object in json format. Please refer to function `BUILTIN_JSON_BACKENDS()` for built-in backends.
        indent (int/None): The `indent` argument for saving in json format, only works if backend is not "jsonl".
        append (bool): If True, use "a" mode instead of "w" mode, only works if backend is "jsonl".
    Returns:
        None
    """
    assert (backend in BUILTIN_JSON_BACKENDS()), (f"backend not found! Supported backends: {BUILTIN_JSON_BACKENDS()}")
    CreateFile(path); path = p2s(path)
    if backend=='jsonl':
        assert (indent is None), ("'jsonl' format does not support parameter 'indent'!")
        with jsonlines.open(path, "a" if append else "w") as f:
            for data in obj:
                f.write(data)
    else:
        assert (append is False), ("'json' format does not support parameter 'append'!")
        module = globals()[backend]
        with open(path, "w") as f:
            if backend in ['json','simplejson']:
                module.dump(obj, f, indent=indent, *args, **kwargs)
            else:
                f.write(module.dumps(obj, indent=indent, *args, **kwargs))

def LoadJson(path, backend:Literal['json','jsonl','demjson','simplejson','picklejson']='json', *args, **kwargs):
    """Load an object from existing json (or jsonl) file.

    Args:
        path: The load path.
        backend (str): Specify backend for loading an object in json format. Please refer to function `BUILTIN_JSON_BACKENDS()` for built-in backends.
    Returns:
        Any: The loaded object.
    """
    assert (backend in BUILTIN_JSON_BACKENDS()), (f"backend not found! Supported backends: {BUILTIN_JSON_BACKENDS()}")
    assert (ExistFile(path)), (f"Path '{path}' does not exist!"); path = p2s(path)
    if backend=='jsonl':
        with open(path, "r") as f:
            return [data for data in jsonlines.Reader(f, *args, **kwargs)]
    else:
        module = globals()[backend]
        with open(path, "r") as f:
            if backend in ['json','simplejson']:
                return module.load(f, *args, **kwargs)
            else:
                return module.loads(f.read(), *args, **kwargs)

def DumpsJson(obj, backend:Literal['json','jsonl','demjson','simplejson','jsonpickle']='json', indent:Optional[int]=None, *args, **kwargs):
    """Save an object as json (or jsonl) str.

    Args:
        obj: The object to be saved.
        backend (str): Specify backend for saving an object in str format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
        indent (int/None): The `indent` argument for saving in json format, only works if backend is not "jsonl".
    Returns:
        str: The json str.
    """
    assert (backend in BUILTIN_JSON_BACKENDS()), (f"backend not found! Supported backends: {BUILTIN_JSON_BACKENDS()}")
    if backend=='jsonl':
        return "\n".join(json.dumps(o, indent=indent, *args, **kwargs) for o in obj)
    else:
        module = globals()[backend]; return module.dumps(obj, indent=indent, *args, **kwargs)

def ReadsJson(s, backend:Literal['json','jsonl','demjson','simplejson','jsonpickle']='json', *args, **kwargs):
    """Load an object from json (or jsonl) str.

    Args:
        s: The json str.
        backend (str): Specify backend for loading an object in str format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
    Returns:
        Any: The loaded object.
    """
    assert (backend in BUILTIN_JSON_BACKENDS()), (f"backend not found! Supported backends: {BUILTIN_JSON_BACKENDS()}")
    if backend=='jsonl':
        return [json.loads(o, *args, **kwargs) for o in s.split("\n")]
    else:
        module = globals()[backend]; return module.loads(s, *args, **kwargs)


def PrintJson(obj, backend:Literal['json','jsonl','demjson','simplejson','jsonpickle']='json', indent:Optional[int]=4, *args, **kwargs):
    """Print an object as json (or jsonl) str using `DumpsJson`.

    Args:
        obj: The object to be saved.
        backend (str): Specify backend for saving an object in str format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
        indent (int/None): The `indent` argument for saving in json format, only works if backend is not "jsonl".
    Returns:
        None
    """
    print(DumpsJson(obj,backend=backend,indent=indent,*args,**kwargs))

def PrettifyJson(path, load_backend:Literal['json','demjson','simplejson','picklejson']='json', save_backend:Literal['json','demjson','simplejson','picklejson']='json', indent:Optional[int]=4, *args, **kwargs):
    """Load and re-save a existing json file.

    Args:
        path: The json file path.
        load_backend (str): Specify backend for loading an object in json format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
        save_backend (str): Specify backend for saving an object in json format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
        indent (int/None): The `indent` argument for saving in json format.
    Returns:
        None
    """
    assert (ExistFile(path)), (f"Path '{path}' does not exist!"); path = p2s(path)
    SaveJson(LoadJson(path, backend=load_backend), path, backend=save_backend, indent=indent, *args, **kwargs)

def SavePickle(obj, path, protocol:Optional[int]=None):
    """Save an object as pickle file.

    Args:
        obj: The object to be saved.
        path: The save path.
        protocol (int/None): The `protocol` argument for `pickle.dump`.
    Returns:
        None
    """
    CreateFile(path); path = p2s(path)
    with open(path, "wb") as f:
        pickle.dump(obj, f, protocol=protocol) if protocol is None else pickle.dumps(obj, protocol=protocol)

def LoadPickle(path):
    """Load an object from existing pickle file.

    Args:
        path: The load path.
    Returns:
        Any: The loaded object.
    """
    assert (ExistFile(path)), (f"Path '{path}' does not exist!"); path = p2s(path)
    return pickle.load(open(PathToString(path), "rb"))

def DumpsPickle(obj, protocol:Optional[int]=None):
    """Save an object as pickle bytearray.

    Args:
        obj: The object to be saved.
        protocol (int/None): The `protocol` argument for `pickle.dump`.
    Returns:
        bytearray: The pickle bytearray.
    """
    return pickle.dumps(obj) if protocol is None else pickle.dumps(obj, protocol=protocol)