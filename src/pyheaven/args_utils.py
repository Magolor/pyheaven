from .file_utils import *
from .serialize_utils import DumpsJson, LoadJson
import argparse

class MemberDict(dict):
    """A dict object whose items can be accessed using `.`.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def view(self, backend='json', indent=4):
        return DumpsJson(dict(self),backend=backend,indent=indent)
    
    def __add__(self, b):
        d = MemberDict(self)
        for key in b:
            if key in d:
                d[key] += b[key]
            else:
                d[key] = b[key]
        return d
    
    def __or__(self, b):
        d = MemberDict(self)
        for key in b:
            d[key] = b[key]
        return d
    
    def __mul__(self, b):
        d = MemberDict(self)
        for key in d:
            d[key] *= b
        return d

    def __div__(self, b):
        d = MemberDict(self)
        for key in d:
            d[key] /= b
        return d

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, state):
        self.__dict__ = state

class ArgumentDescriptor(object):
    """The base descriptor that wraps arguments of `add_argument` for `argparse.ArgumentParser`.
    """
    def __init__(self, dest:str, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        
        Args:
            dest (str): The `dest` arg of `add_argument`.
            full (str): The full name (i.e.: `--`) of the argument.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        dest = dest.replace('-','_')
        if full is None:
            full = dest.replace('_','-')
        if short is None:
            short = full[0]
        short = "-"+short; full = "--"+full
        self.name = (dest, ) if required else (short, full)
        self.args = {} if required else {'dest':dest}
        self.args.update(kwargs)

    def register(self, parser):
        """Register the argument described by the descriptor to `parset`.

        Args:
            parser: The parser object that this argument will be registered to.
        """
        parser.add_argument(
            *self.name,
            **self.args
        )

class IntArgumentDescriptor(ArgumentDescriptor):
    """The descriptor for arguments of `type` equal to `int`.
    """
    def __init__(self, dest:str, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        4. The `type` argument will be set to `int` by default (and `type` specifier in `kwargs` will be override).

        Args:
            dest (str): The `dest` arg of `add_argument`.
            full (str): The full name (i.e.: `--`) of the argugment.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        kwargs['type'] = int; super(IntArgumentDescriptor, self).__init__(dest=dest, full=full, short=short, required=required, **kwargs)

class StrArgumentDescriptor(ArgumentDescriptor):
    """The descriptor for arguments of `type` equal to `str`.
    """
    def __init__(self, dest:str, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        4. The `type` argument will be set to `str` by default (and `type` specifier in `kwargs` will be override).

        Args:
            dest (str): The `dest` arg of `add_argument`.
            full (str): The full name (i.e.: `--`) of the argugment.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        kwargs['type'] = str; super(StrArgumentDescriptor, self).__init__(dest=dest, full=full, short=short, required=required, **kwargs)

class BoolArgumentDescriptor(ArgumentDescriptor):
    """The descriptor for arguments of `type` equal to `bool`.
    """
    def __init__(self, dest:str, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        4. The `type` argument will be set to `bool` by default (and `type` specifier in `kwargs` will be override).

        Args:
            dest (str): The `dest` arg of `add_argument`.
            full (str): The full name (i.e.: `--`) of the argugment.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        kwargs['type'] = bool; super(BoolArgumentDescriptor, self).__init__(dest=dest, full=full, short=short, required=required, **kwargs)

class FloatArgumentDescriptor(ArgumentDescriptor):
    """The descriptor for arguments of `type` equal to `float`.
    """
    def __init__(self, dest:str, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        4. The `type` argument will be set to `float` by default (and `type` specifier in `kwargs` will be override).

        Args:
            dest (str): The `dest` arg of `add_argument`.
            full (str): The full name (i.e.: `--`) of the argugment.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        kwargs['type'] = float; super(FloatArgumentDescriptor, self).__init__(dest=dest, full=full, short=short, required=required, **kwargs)

class SwitchArgumentDescriptor(ArgumentDescriptor):
    """The descriptor for arguments of `action` equal to `store_true` or `store_false`.
    """
    def __init__(self, dest:str, to:bool=True, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        4. The `action` argument will be set to 'store_true'/'store_false' by default (and `action` specifier in `kwargs` will be override).

        Args:
            dest (str): The `dest` arg of `add_argument`.
            to (bool): If True, the `action` is set to 'store_true', otherwise 'store_false'.  
            full (str): The full name (i.e.: `--`) of the argugment.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        kwargs['action'] = 'store_'+['false','true'][to]; super(SwitchArgumentDescriptor, self).__init__(dest=dest, full=full, short=short, required=required, **kwargs)

class ConstArgumentDescriptor(ArgumentDescriptor):
    """The descriptor for arguments of `action` equal to `store_const`.
    """
    def __init__(self, dest:str, const, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        4. The `action` argument will be set to 'store_const' and the `const` argument will be set to `const` by default (and `action` and `const` specifier in `kwargs` will be override).

        Args:
            dest (str): The `dest` arg of `add_argument`.
            const: The const value to be stored.  
            full (str): The full name (i.e.: `--`) of the argugment.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        kwargs['action'] = 'store_const'; kwargs['const'] = const; super(ConstArgumentDescriptor, self).__init__(dest=dest, full=full, short=short, required=required, **kwargs)

class LiteralArgumentDescriptor(ArgumentDescriptor):
    """The descriptor for arguments with finite `choices`.
    """
    def __init__(self, dest:str, choices:List, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        4. The `choices` argument will be set to `choices` by default (and `choices` specifier in `kwargs` will be override).

        Args:
            dest (str): The `dest` arg of `add_argument`.
            choices (List): The options specified for the argument.  
            full (str): The full name (i.e.: `--`) of the argugment.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        kwargs['choices'] = choices; super(LiteralArgumentDescriptor, self).__init__(dest=dest, full=full, short=short, required=required, **kwargs)

class ListArgumentDescriptor(ArgumentDescriptor):
    """The descriptor for arguments of `action` equal to `extend`.
    """
    def __init__(self, dest:str, full:str=None, short:str=None, required:bool=False, **kwargs):
        """The following are different from `add_argument`:
        1. '-' in `dest` will be replaced to '_'.
        2. All unnecessary arguments are represented as both short name (i.e.: `-`) and full name (i.e.: `--`), the full name is  `dest` ('_' will be replaced to '-') by default, and the short name is the first character of full name by default. Please specify `short` manually when conflict occurs. 
        3. All necessary arguments are represented with `dest` ('-' will be replaced to '_'). Arguments are determined necessary if and only if `required` is set to True.
        4. The `type` argument will be set to `int` by default (and `type` specifier in `kwargs` will be override).

        Args:
            dest (str): The `dest` arg of `add_argument`.
            full (str): The full name (i.e.: `--`) of the argugment.
            short (str): The short name (i.e.: `-`) of the argugment.
            required (bool): If True, the argument is necessary, otherwise unnecessary.
        """
        kwargs['action'] = 'extend'; kwargs['nargs'] = kwargs['nargs'] if 'nargs' in kwargs else '*'; kwargs['default'] = kwargs['default'] if 'default' in kwargs else list()
        super(ListArgumentDescriptor, self).__init__(dest=dest, full=full, short=short, required=required, **kwargs)

class HeavenArguments(MemberDict):
    """An argument dict extended from `MemberDict`.
    """
    def __iter__(self):
        for key in sorted(self.keys()):
            yield key, self[key]

    def __str__(self):
        return DumpsJson(dict(self),indent=4)

    @classmethod
    def from_parser(cls, descriptors:List, **parser_args):
        """Construct arguments from a list of argument descriptors and `argparse`.

        Notice that this function will construct argparser and parse all input args.

        Args:
            descriptors (List): The list of argument descriptors.
            parser_args: Arguments for constructing `argparse.ArgumentParser`.
        Returns:
            Arguments: The parsed arguments.
        """
        parser = argparse.ArgumentParser(**parser_args)
        for descriptor in descriptors:
            descriptor.register(parser)
        return cls(vars(parser.parse_args()))
    
    @classmethod
    def from_json(cls, path, backend='json'):
        """Construct arguments from a json file.

        Args:
            path: The json file path.
            backend (str): Specify backend for saving an object in str format. Please refer to function `BUILTIN_JSON_BACKENDS()` for built-in backends.
        Returns:
            Arguments: The parsed arguments.
        """
        return cls(LoadJson(path,backend=backend))
    
    @classmethod
    def from_object(cls, object):
        """Construct arguments from an object.

        Args:
            obj: The object.
        Returns:
            Arguments: The parsed arguments.
        """
        return cls(vars(object))
    
    @classmethod
    def from_properties(cls, path, errors:Literal['interupt','strict','ignore']='interupt'):
        """Construct arguments from a properties file.

        Args:
            path: The properties file path.
            errors (str): Specify behavior when encountering errors.
                          If 'interupt', an Exception will be raised immediately at the error line.
                          If 'strict', a ValueError will be raised to report all error lines.
                          If 'ignore', all error lines will be skipped.
        Returns:
            Arguments: The parsed arguments.
        """
        args = {}; failures = []
        with open(path,"r") as f:
            i = 0
            for line in f:
                try:
                    if line.strip()!='':
                        property = line.strip().split('#')[0]
                        key, value = property.strip().split(' ')
                        args.update(key.strip(),value.strip())
                except Exception as e:
                    if errors=="interupt":
                        raise e
                    failures.append((i,line,e))
                i += 1
        if errors=="strict":
            raise ValueError("\n".join(failures))
        return cls(args)