from .file_utils import *
import io
import torch
import numpy as np
from torch.utils.data import Dataset, Subset, ConcatDataset, DataLoader

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

def DumpsTorch(obj, pickle_protocol:Optional[int]=None, _use_new_zipfile_serialization:bool=True):
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

class HeavenDataset(Dataset):
    def __init__(self, dataset, name="HeavenDataset"):
        self.dataset = dataset; self.name=name; self.__index__ = 0
    
    def __getitem__(self, i):
        if isinstance(i, int):
            return self.dataset[i]
        else:
            indices = np.array([j for j in range(len(self.dataset))])[i]
            return HeavenDataset(Subset(self, indices.tolist()),name=self.name)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
    
    def __next__(self):
        if self.__index__>=len(self):
            raise StopIteration
        else:
            data = self[self.__index__]; self.__index__ += 1; return data

    def rename(self, name="HeavenDataset"):
        self.name = name
    
    def __len__(self):
        return len(self.dataset)
    
    def __or__(self, b):
        return HeavenDataset(ConcatDataset([self,b]),name=self.name+(","+b.name if hasattr(b,"name") else ""))

    def __str__(self):
        return ("{"+self.name+"}" if ',' in self.name else self.name)+f"(len={len(self)})"

class HeavenDataLoader:
    def __init__(self, dataloader, dataset=None):
        self.dataset = dataset
        self.dataloader = dataloader
        self.iterator = iter(dataloader)

    def __iter__(self):
        while True:
            for data in self.dataloader:
                yield data

    def __next__(self):
        try:
            data = next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.dataloader)
            data = next(self.iterator)
        return data

    def __len__(self):
        return len(self.dataloader)