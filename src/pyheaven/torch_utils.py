from .file_utils import *
import io
import torch
import numpy as np
import torch.nn as nn
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
    def __init__(self, dataloader, dataset=None, eternal=False):
        self.dataset = dataset
        self.dataloader = dataloader
        self.iterator = iter(dataloader)
        self.eternal = eternal

    def __iter__(self):
        for data in self.dataloader:
            yield data
        while self.eternal:
            for data in self.dataloader:
                yield data

    def __next__(self):
        try:
            data = next(self.iterator)
        except StopIteration:
            if self.eternal:
                self.iterator = iter(self.dataloader)
                data = next(self.iterator)
            else:
                raise StopIteration
        return data

    def __len__(self):
        return len(self.dataloader)

Import("timm.create_model@create_model",globals())
Import("torchvision.models._utils@TV_U",globals())

class TimmBackbone(nn.Module):
    def __init__(self,
        model_type="",
        input_layer_getter=lambda n:n.conv1,
        modify_input_channels=None,
        output_layer_name="fc",
        embedding_dim=2048,
        **model_args
    ):
        super(TimmBackbone, self).__init__()
        self.net = create_model(model_type, **model_args)

        layer = input_layer_getter(self.net); device = layer.weight.device
        if modify_input_channels and modify_input_channels!=layer.in_channels:
            layer.in_channels = modify_input_channels
            shape = layer.weight.shape; shape = torch.Size([shape[0],modify_input_channels,shape[2],shape[3]])
            layer.weight = nn.Parameter(torch.zeros(shape)).to(device)
            nninit.xavier_uniform_(layer.weight)
        layer = input_layer_getter(self.net)
        self.in_channels = layer.in_channels
        
        self.net = TV_U.IntermediateLayerGetter(self.net, return_layers={output_layer_name:"out"})
        self.net._modules[output_layer_name] = nn.Linear(self.net._modules[output_layer_name].in_features,embedding_dim,bias=True)
        self.net.to(device)

    def forward(self, data):
        return self.net(data)['out']

class FC(nn.Module):
    def __init__(
        self,
        input_dim:int,
        output_dim:int,
        bias=True,
        norm_layer=None,
        activation=nn.Identity(),
        dropout:Optional[int]=None,
        dropout_inplace:bool=True,
    ):
        super(FC, self).__init__()
        self.input_dim = input_dim; self.output_dim = output_dim
        self.layers = nn.Sequential(*(
            ([nn.Dropout(p=dropout,inplace=dropout_inplace)] if dropout is not None else [])
        +   ([nn.Linear(input_dim,output_dim,bias=bias)])
        +   ([norm_layer] if norm_layer is not None else [])
        +   ([activation] if activation is not None else [])
        ))
    
    def forward(self, data):
        return self.layers(torch.flatten(data,start_dim=1))

class CONV(nn.Module):
    def __init__(
        self,
        in_channels:int,
        out_channels:int,
        kernel_size:int,
        stride:int=1,
        padding:int=0,
        dilation:int=1,
        groups:int=1,
        padding_mode:str='zeros',
        bias:bool=True,
        norm_layer=None,
        activation=nn.Identity(),
        dropout:Optional[int]=None,
        dropout_inplace:bool=True,
    ):
        super(CONV, self).__init__()
        self.in_channels = in_channels; self.out_channels = out_channels
        self.layers = nn.Sequential(*(
            ([nn.Dropout(p=dropout,inplace=dropout_inplace)] if dropout is not None else [])
        +   ([nn.Conv2d(in_channels=in_channels,out_channels=out_channels,kernel_size=kernel_size,stride=stride,padding=padding,dilation=dilation,groups=groups,padding_mode=padding_mode,bias=bias)])
        +   ([norm_layer] if norm_layer is not None else [])
        +   ([activation] if activation is not None else [])
        ))
    
    def forward(self, data):
        return self.layers(data)