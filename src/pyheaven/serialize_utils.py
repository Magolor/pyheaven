from .file_utils import *
import json
import pickle
import os
Import("demjson",globals())
Import("jsonlines",globals())
Import("simplejson",globals())
Import("jsonpickle",globals())

def BUILTIN_JSON_BACKENDS():
    return ['json','jsonl','demjson','simplejson','jsonpickle']
def BUILTIN_JSON_PRETTIFY_BACKENDS():
    return ['json',        'demjson','simplejson','jsonpickle']

# Load default encoding from config file
DEFAULT_ENCODING_CONFIG_PATH = pjoin(PYHEAVEN_PATH, "encoding_config.json")
def load_default_encoding():
    if not os.path.exists(DEFAULT_ENCODING_CONFIG_PATH):
        CreateFile(DEFAULT_ENCODING_CONFIG_PATH)
        with open(DEFAULT_ENCODING_CONFIG_PATH, 'w') as f:
            json.dump({"default_encoding": "utf-8"}, f)
    with open(DEFAULT_ENCODING_CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config.get("default_encoding", "utf-8")
def set_default_encoding(encoding: str="utf-8"):
    with open(DEFAULT_ENCODING_CONFIG_PATH, 'w') as f:
        json.dump({"default_encoding": encoding}, f)

def SaveJson(obj, path, backend:Literal['json','jsonl','demjson','simplejson','jsonpickle']='json', indent:Optional[int]=None, append:bool=False, encoding:str=None, *args, **kwargs):
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
    if encoding is None:
        encoding = load_default_encoding()  # Load from config
    assert (backend in BUILTIN_JSON_BACKENDS()), (f"backend not found! Supported backends: {BUILTIN_JSON_BACKENDS()}")
    CreateFile(path); path = p2s(path)
    if backend=='jsonl':
        assert (indent is None), ("'jsonl' format does not support parameter 'indent'!")
        with open(path, "a" if append else "w", encoding=encoding) as f:
            writer = jsonlines.Writer(f)
            for data in obj:
                writer.write(data)
            writer.close()
    else:
        assert (append is False), ("'json' format does not support parameter 'append'!")
        module = globals()[backend]
        with open(path, "w", encoding=encoding) as f:
            if backend in ['json','simplejson']:
                module.dump(obj, f, indent=indent, ensure_ascii=False, *args, **kwargs)
            else:
                f.write(module.dumps(obj, indent=indent, ensure_ascii=False, *args, **kwargs))

def LoadJson(path, backend:Literal['json','jsonl','demjson','simplejson','picklejson']='json', encoding:str=None, *args, **kwargs):
    """Load an object from existing json (or jsonl) file.

    Args:
        path: The load path.
        backend (str): Specify backend for loading an object in json format. Please refer to function `BUILTIN_JSON_BACKENDS()` for built-in backends.
    Returns:
        Any: The loaded object.
    """
    if encoding is None:
        encoding = load_default_encoding()  # Load from config
    assert (backend in BUILTIN_JSON_BACKENDS()), (f"backend not found! Supported backends: {BUILTIN_JSON_BACKENDS()}")
    assert (ExistFile(path)), (f"Path '{path}' does not exist!"); path = p2s(path)
    if backend=='jsonl':
        with open(path, "r", encoding=encoding) as f:
            return [data for data in jsonlines.Reader(f, *args, **kwargs)]
    else:
        module = globals()[backend]
        with open(path, "r", encoding=encoding) as f:
            if backend in ['json','simplejson']:
                return module.load(f, *args, **kwargs)
            else:
                return module.loads(f.read(), *args, **kwargs)

def DumpsJson(obj, backend:Literal['json','jsonl','demjson','simplejson','jsonpickle']='json', indent:Optional[int]=None, encoding:str=None, *args, **kwargs):
    """Save an object as json (or jsonl) str.

    Args:
        obj: The object to be saved.
        backend (str): Specify backend for saving an object in str format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
        indent (int/None): The `indent` argument for saving in json format, only works if backend is not "jsonl".
    Returns:
        str: The json str.
    """
    if encoding is None:
        encoding = load_default_encoding()  # Load from config
    assert (backend in BUILTIN_JSON_BACKENDS()), (f"backend not found! Supported backends: {BUILTIN_JSON_BACKENDS()}")
    if backend=='jsonl':
        return "\n".join(json.dumps(o, indent=indent, ensure_ascii=False, *args, **kwargs) for o in obj)
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


def PrintJson(obj, backend:Literal['json','jsonl','demjson','simplejson','jsonpickle']='json', indent:Optional[int]=4, encoding:str=None, *args, **kwargs):
    """Print an object as json (or jsonl) str using `DumpsJson`.

    Args:
        obj: The object to be saved.
        backend (str): Specify backend for saving an object in str format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
        indent (int/None): The `indent` argument for saving in json format, only works if backend is not "jsonl".
    Returns:
        None
    """
    if encoding is None:
        encoding = load_default_encoding()  # Load from config
    print(DumpsJson(obj,backend=backend,indent=indent,*args,**kwargs))

def PrettifyJson(path, load_backend:Literal['json','demjson','simplejson','picklejson']='json', save_backend:Literal['json','demjson','simplejson','picklejson']='json', indent:Optional[int]=4, load_encoding:str=None, save_encoding:str=None, *args, **kwargs):
    """Load and re-save a existing json file.

    Args:
        path: The json file path.
        load_backend (str): Specify backend for loading an object in json format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
        save_backend (str): Specify backend for saving an object in json format. Please refer to function `BUILTIN_JSON_PRETTIFY_BACKENDS()` for built-in backends.
        indent (int/None): The `indent` argument for saving in json format.
    Returns:
        None
    """
    if load_encoding is None:
        load_encoding = load_default_encoding()  # Load from config
    if save_encoding is None:
        save_encoding = load_default_encoding()  # Load from config
    assert (ExistFile(path)), (f"Path '{path}' does not exist!"); path = p2s(path)
    SaveJson(LoadJson(path, backend=load_backend, encoding=load_encoding), path, backend=save_backend, indent=indent, encoding=save_encoding, *args, **kwargs)

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