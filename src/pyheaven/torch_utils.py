from .file_utils import *
import io
import torch

def SaveTorch(obj, path, pickle_protocol:Optional[int]=None, _use_new_zipfile_serialization:bool=True):
    """Save an object as torch file.

    Args:
        obj: The object to be saved.
        path: The save path.
        pickle_protocol (int/None): The `pickle_protocol` argument for `torch.save`.
        _use_new_zipfile_serialization (int/None): The `_use_new_zipfile_serialization` argument for `torch.save`.
    Returns:
        None
    """
    CreateFile(path); path = p2s(path)
    torch.save(obj, path, pickle_protocol=pickle_protocol, _use_new_zipfile_serialization=_use_new_zipfile_serialization)

def LoadTorch(path, map_location=None):
    """Load an object from existing torch file.

    Args:
        path: The load path.
        map_location: The `map_location` argument for `torch.load`.
    Returns:
        Any: The loaded object.
    """
    assert (ExistFile(path)), (f"Path '{path}' does not exist!"); path = p2s(path)
    return torch.load(path, map_location=map_location)

def DumpsTorch(obj, pickle_protocol:Optional[int]=None, _use_new_zipfile_serialization:bool=True)
    """Save an object as torch bytearray.

    Args:
        obj: The object to be saved.
        pickle_protocol (int/None): The `pickle_protocol` argument for `torch.save`.
        _use_new_zipfile_serialization (int/None): The `_use_new_zipfile_serialization` argument for `torch.save`.
    Returns:
        None
    """
    buff = io.BytesIO()
    torch.save(obj, buff, pickle_protocol=pickle_protocol, _use_new_zipfile_serialization=_use_new_zipfile_serialization)
    buff.seek(0); return buff.read()