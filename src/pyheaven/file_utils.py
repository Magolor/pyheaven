from .basic_utils import *
from .misc_utils import FlattenList
from pathlib import PurePosixPath as PurePosixPath
from pathlib import Path as Path
from copy import deepcopy
import os
import shutil
import zipfile
Import("send2trash.send2trash@send2trash",globals())
Import("jsonlines",globals())

# Modified from https://stackoverflow.com/questions/21799210/python-copy-larger-file-too-slow
def _copyfileobj_patched(fsrc, fdst, length=64*1024*1024):
    """Patches shutil method to hugely improve copy speed"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
shutil.copyfileobj = _copyfileobj_patched

def PathToString(path="./", as_folder:bool=False):
    """Convert any representation of a path (either a `pathlib.Path` or a str) to a str, with trailing slashes for folder.

    Args:
        path: The path to be converted to string format.
        as_folder (bool): If True, force to treat it as a folder, otherwise ignored. This is useful when, for example, the desired folder does not exist.
    Returns:
        str: The result string.
    """
    path = Path(path); r = str(PurePosixPath(path/'@'))[:-1] if as_folder or path.is_dir() else str(PurePosixPath(path)); return r if r!="" else "./"

def p2s(p="./", f:bool=False):
    """Convert any representation of a path (either a `pathlib.Path` or a str) to a str, with trailing slashes for folder.

    This is a short alias for `PathToString`.

    Args:
        p: The path to be converted to string format.
        f (bool): If True, force to treat it as a folder, otherwise ignored. This is useful when, for example, the desired folder does not exist.
    Returns:
        str: The result string.
    """
    path = Path(p); r = str(PurePosixPath(path/'@'))[:-1] if f or path.is_dir() else str(PurePosixPath(path)); return r if r!="" else "./"

def p2abs(p="./"):
    """Convert a path to absolute format.

    Args:
        p: The path to be converted.
    Returns:
        str: The result string.
    """
    path = Path(p); return p2s(path.absolute())

def p2par(p="./", l:int=1):
    """Get the parent (ancestor) of a path. Note that for a relative path string, it can not trace beyond the root path.

    Args:
        p: The path to be queried.
        l (int): The number of levels of parents to jump.
    Returns:
        str: The result string.
    """
    path = Path(p)
    for _ in range(l):
        path = path.parent
    return p2s(path)

def p2stem(p="./"):
    """Get the stem of a path.

    Args:
        p: The path to be queried.
    Returns:
        str: The result string.
    """
    return Path(p2s(p)).stem

def p2name(p="./"):
    """Get the name of a path.

    Args:
        p: The path to be queried.
    Returns:
        str: The result string.
    """
    return Path(p2s(p)).name

def pjoin(*plist):
    """Concatenate a list of string or paths to a path.

    Args:
        *plist (Iterable): The list to be converted.
    Returns:
        str: The result string.
    """
    path = Path()
    for p in plist:
        path = path/Path(p)
    return p2s(path)

def Prefix(path):
    """Get the prefix of a path, return the folder itself for a folder.

    Args:
        path: The path.
    Returns:
        str: The result string.
    """
    path = p2s(path); parts = path.split('.'); return path if ExistFolder(path) else ('.'.join(parts[:-1] if len(parts)>1 else parts))

def Suffix(path):
    """Get the suffix of a path, return empty string "" for a folder.

    Args:
        path: The path.
    Returns:
        str: The result string.
    """
    path = p2s(path); parts = path.split('.'); return "" if ExistFolder(path) else (parts[-1] if len(parts)>1 else "")

def Format(path):
    """Get the format of a path.

    This is an alias for `Suffix`.

    Args:
        path: The path.
    Returns:
        str: The result string.
    """
    path = p2s(path); parts = path.split('.'); return "" if ExistFolder(path) else (parts[-1] if len(parts)>1 else "")

def AsFormat(path, format):
    """Get the file with the same name as path but with the desired format.

    Args:
        path: The path.
    Returns:
        str: The result string.
    """
    return (Prefix(path)+'.'+format) if format!="" else Prefix(path)
    
def ExistPath(path):
    """Check whether a file or folder exists.

    Args:
        path: The path.
    Returns:
        bool: True if the file or folder exists otherwise False.
    """
    return Path(path).exists()
    
def ExistFolder(path):
    """Check whether a folder exists.

    Args:
        path: The path.
    Returns:
        bool: True if the folder exists otherwise False.
    """
    return Path(path).is_dir()

def ExistFile(path):
    """Check whether a file exists.

    Args:
        path: The path.
    Returns:
        bool: True if the file exists otherwise False.
    """
    return Path(path).is_file()

def BY_NAME_CRITERIA(s):
    return s[1]
def BY_CTIME_CRITERIA(s):
    return os.path.getctime(s[1])
def BY_MTIME_CRITERIA(s):
    return os.path.getmtime(s[1])
def BY_ATIME_CRITERIA(s):
    return os.path.getatime(s[1])
def BY_SIZE_CRITERIA(s):
    return os.path.getsize(s[1])
def BUILTIN_LISTPATHS_SORT_CRITERIA():
    return {
        'BY_NAME_CRITERIA':BY_NAME_CRITERIA,
        'BY_CTIME_CRITERIA':BY_CTIME_CRITERIA,
        'BY_MTIME_CRITERIA':BY_MTIME_CRITERIA,
        'BY_ATIME_CRITERIA':BY_ATIME_CRITERIA,
        'BY_SIZE_CRITERIA':BY_SIZE_CRITERIA,
    }
def EXISTS_FILTER(s):
    return ExistPath(s[1])
def IS_FOLDER_FILTER(s):
    return ExistFolder(s[1])
def IS_FILE_FILTER(s):
    return ExistFile(s[1])
def BUILTIN_LISTPATHS_FILTER_FUNCTIONS():
    return {
        'EXISTS_FILTER':EXISTS_FILTER,
        'IS_FOLDER_FILTER':IS_FOLDER_FILTER,
        'IS_FILE_FILTER':IS_FILE_FILTER,
    }
def ListPaths(path="./", ordered:bool=False, with_path:bool=False, filter_function=None, **sort_args):
    """Return a list of subpaths under the given path.

    Args:
        path: The path.
        ordered (bool): If True, sort subpaths by criteria specified in `sort_args`, otherwise in original order from `os.listdir()`.
        with_path (bool): If True, pre-attach the given path to all subpaths, otherwise ignored.
        filter_function: Filter subpaths in format of (path, full_path). Please refer to function `BUILTIN_LISTPATHS_FILTER_FUNCTIONS()` for built-in criteria.
        sort_args: Args for calling `sorted` on the subpaths in format of (path, full_path), only works if `ordered` is True. Please refer to function `BUILTIN_LISTPATHS_SORT_CRITERIA()` for built-in criteria.
    Returns:
        List[str]: The result strings.
    """
    path = p2s(path); subpaths = [(p2s(subpath),pjoin(path,subpath)) for subpath in os.listdir(path)]
    subpaths = list(filter(filter_function, subpaths)) if filter_function is not None else subpaths
    subpaths = sorted(subpaths, **sort_args) if ordered else subpaths
    return [subpath[with_path] for subpath in subpaths]
    
def ListFolders(path="./", ordered:bool=False, with_path=False, **sort_args):
    """Return a list of folders under the given path.

    This is an alias for `ListPaths(filter_function=IS_FOLDER_FILTER)`.

    Args:
        path: The path.
        ordered (bool): If True, sort subpaths by criteria specified in `sort_args`, otherwise in original order from `os.listdir()`.
        with_path (bool): If True, pre-attach the given path to all subpaths, otherwise ignored.
        sort_args: Args for calling `sorted` on the subpaths in format of (path, full_path), only works if `ordered` is True. Please refer to function `BUILTIN_LISTPATHS_SORT_CRITERIA()` for built-in criteria.
    Returns:
        List[str]: The result strings.
    """
    return ListPaths(path, ordered=ordered, with_path=with_path, filter_function=IS_FOLDER_FILTER, **sort_args)
    
def ListFiles(path="./", ordered:bool=False, with_path=False, **sort_args):
    """Return a list of files under the given path.

    This is an alias for `ListPaths(filter_function=IS_FILE_FILTER)`.

    Args:
        path: The path.
        ordered (bool): If True, sort subpaths by criteria specified in `sort_args`, otherwise in original order from `os.listdir()`.
        with_path (bool): If True, pre-attach the given path to all subpaths, otherwise ignored.
        sort_args: Args for calling `sorted` on the subpaths in format of (path, full_path), only works if `ordered` is True. Please refer to function `BUILTIN_LISTPATHS_SORT_CRITERIA()` for built-in criteria.
    Returns:
        List[str]: The result strings.
    """
    return ListPaths(path, ordered=ordered, with_path=with_path, filter_function=IS_FILE_FILTER, **sort_args)

def EnumPaths(path="./", relpath="./", ordered:bool=False, filter_function=None, **sort_args):
    """Return a list of subpaths recursively under the given path. Since this is wrapped upon `os.walk`, `with_path` is forced. (TODO: fix)

    Args:
        path: The path.
        relpath: The output result would be converted to relative to the given path. Use None for non-relative path.
        ordered (bool): If True, sort subpaths by criteria specified in `sort_args`, otherwise in original order from `os.listdir()`.
        filter_function: Filter subpaths in format of (full_path, full_path). Notice that the filter function will only be applied at the base level instead of applied recursively. Please refer to function `BUILTIN_LISTPATHS_FILTER_FUNCTIONS()` for built-in criteria.
        sort_args: Args for calling `sorted` on the subpaths in format of (full_path, full_path), only works if `ordered` is True. Notice that the sort function will only be applied at the base level instead of applied recursively. PPlease refer to function `BUILTIN_LISTPATHS_SORT_CRITERIA()` for built-in criteria.
    Returns:
        List[str]: The result strings.
    """
    path = p2s(path); subpaths = []
    for root, dirs, files in os.walk(path):
        subpaths.append(root); subpaths.extend([pjoin(root, file) for file in files])
    subpaths = [(subpath,subpath) for subpath in subpaths]
    subpaths = list(filter(filter_function, subpaths)) if filter_function is not None else subpaths
    subpaths = sorted(subpaths, **sort_args) if ordered else subpaths
    return [(subpath[1] if relpath is None else p2s(os.path.relpath(subpath[1], relpath))) for subpath in subpaths]

def EnumFolders(path="./", relpath="./", ordered:bool=False, **sort_args):
    """Return a list of folders recursively under the given path.

    This is an alias for `EnumPaths(filter_function=IS_FOLDER_FILTER)`.

    Args:
        path: The path.
        relpath: The output result would be converted to relative to the given path. Use None for non-relative path.
        ordered (bool): If True, sort subpaths by criteria specified in `sort_args`, otherwise in original order from `os.listdir()`.
        filter_function: Filter subpaths in format of (path, full_path). Notice that the filter function will only be applied at the base level instead of applied recursively. Please refer to function `BUILTIN_LISTPATHS_FILTER_FUNCTIONS()` for built-in criteria.
        sort_args: Args for calling `sorted` on the subpaths in format of (path, full_path), only works if `ordered` is True. Notice that the sort function will only be applied at the base level instead of applied recursively. PPlease refer to function `BUILTIN_LISTPATHS_SORT_CRITERIA()` for built-in criteria.
    Returns:
        List[str]: The result strings.
    """
    return EnumPaths(path, relpath=relpath, ordered=ordered, filter_function=IS_FOLDER_FILTER, **sort_args)

def EnumFiles(path="./", relpath="./", ordered:bool=False, **sort_args):
    """Return a list of files recursively under the given path.

    This is an alias for `EnumPaths(filter_function=IS_FILE_FILTER)`.

    Args:
        path: The path.
        relpath: The output result would be converted to relative to the given path. Use None for non-relative path.
        ordered (bool): If True, sort subpaths by criteria specified in `sort_args`, otherwise in original order from `os.listdir()`.
        filter_function: Filter subpaths in format of (path, full_path). Notice that the filter function will only be applied at the base level instead of applied recursively. Please refer to function `BUILTIN_LISTPATHS_FILTER_FUNCTIONS()` for built-in criteria.
        sort_args: Args for calling `sorted` on the subpaths in format of (path, full_path), only works if `ordered` is True. Notice that the sort function will only be applied at the base level instead of applied recursively. PPlease refer to function `BUILTIN_LISTPATHS_SORT_CRITERIA()` for built-in criteria.
    Returns:
        List[str]: The result strings.
    """
    return EnumPaths(path, relpath=relpath, ordered=ordered, filter_function=IS_FILE_FILTER, **sort_args)
    
def CreateFolder(path):
    """Create the given path as folder, parents will be automatically built.

    Args:
        path: The path.
    Returns:
        bool: True if the folder is created, otherwise already exists.
    """
    if not ExistPath(path):
        Path(path).mkdir(parents=True,exist_ok=False); return True
    else:
        return False
    
def CreateFile(path):
    """Create the given path as file, parents will be automatically built.

    Args:
        path: The path.
    Returns:
        bool: True if the file is created, otherwise already exists.
    """
    if not ExistPath(path):
        Path(p2par(path)).mkdir(parents=True,exist_ok=True)
        if Suffix(path)!='':
            Path(path).touch(exist_ok=False)
        return True
    else:
        return False

def Delete(path, rm=False):
    """Delete the given path.

    Args:
        path: The path.
        rm (bool): If True, use `shutil` to enforce remove, otherwise `send2trash` only.
    Returns:
        bool: True if the path is deleted, otherwise it does not exist.
    """
    if ExistPath(path):
        path = p2s(path); (shutil.rmtree(path) if ExistFolder(path) else os.remove(path)) if rm else send2trash(path); return True
    else:
        return False

def ClearFolder(path, rm=False):
    """Clear the given folder if it exists, create if it does not exist.

    Args:
        path: The path.
        rm (bool): If True, use `shutil` to enforce remove, otherwise `send2trash` only.
    Returns:
        None
    """
    Delete(path,rm=rm); CreateFolder(path)

def ClearFile(path, rm=False):
    """Clear the given file if it exists, create if it does not exist.

    Args:
        path: The path.
        rm (bool): If True, use `shutil` to enforce remove, otherwise `send2trash` only.
    Returns:
        None
    """
    Delete(path,rm=rm); CreateFile(path)

def CopyFile(src, dst, rm=False):
    """Copy file from src to dst, notice that dst will be deleted if exists.

    Args:
        src: The source path.
        dst: The destination path.
        rm (bool): If True, use `shutil` to enforce remove (if `dst` exists), otherwise `send2trash` only.
    Returns:
        None
    """
    ClearFile(dst, rm=rm); shutil.copyfile(p2s(src), p2s(dst))

def ReplaceFile(src, dst, rm=False):
    """Replace file from src to dst, notice that dst will be deleted if exists.

    This is an alias for `CopyFile`.

    Args:
        src: The source path.
        dst: The destination path.
        rm (bool): If True, use `shutil` to enforce remove (if `dst` exists), otherwise `send2trash` only.
    Returns:
        None
    """
    ClearFile(dst, rm=rm); shutil.copyfile(p2s(src), p2s(dst))

def CopyFolder(src, dst, rm=False):
    """Copy folder from src (folder name included) to dst (folder name included). Only existing files will be deleted if exists.

    Warning: This code is buggy. TODO: debug.

    This is NOT the same as `ReplaceFolder`, which does not merge `src` to `dst`, instead, it deletes the entire `dst` directory if exists.

    Args:
        src: The source path.
        dst: The destination path.
        rm (bool): If True, use `shutil` to enforce remove (if conflict arises), otherwise `send2trash` only.
    Returns:
        None
    """
    for file in EnumFiles(src,relpath=src):
        CopyFile(pjoin(src,file),pjoin(dst,file),rm=rm)

def ReplaceFolder(src, dst, rm=False):
    """Copy folder from src (folder name included) to dst (folder name included). The entire dst directory will be deleted if exists.

    This is NOT the same as `CopyFolder`, which merges `src` to `dst`.

    Args:
        src: The source path.
        dst: The destination path.
        rm (bool): If True, use `shutil` to enforce remove (if `dst` exists), otherwise `send2trash` only.
    Returns:
        None
    """
    CreateFolder(dst); Delete(dst, rm=rm); shutil.copytree(p2s(src,f=True), p2s(dst,f=True))

def MoveFile(src, dst, rm=False):
    """Move file from src (folder name included) to dst (folder name included). The entire dst directory will be deleted if exists.

    This is NOT the same as `shutil.move`, which will raise an error when `dst` is an existing file.

    Args:
        src: The source path.
        dst: The destination path.
        rm (bool): If True, use `shutil` to enforce remove (if `dst` exists), otherwise `send2trash` only.
    Returns:
        None
    """
    ClearFile(dst); shutil.move(p2s(src,f=True), p2s(dst,f=True))

def MoveFolder(src, dst, rm=False):
    """Move folder from src (folder name included) to dst (folder name included). The entire dst directory will be deleted if exists.

    This is NOT the same as `shutil.move`, which will move the `src` into `dst` if `dst` is an existing folder

    Args:
        src: The source path.
        dst: The destination path.
        rm (bool): If True, use `shutil` to enforce remove (if `dst` exists), otherwise `send2trash` only.
    Returns:
        None
    """
    CreateFolder(dst); Delete(dst, rm=rm); shutil.move(p2s(src,f=True), p2s(dst,f=True))

def Zip(src, dst):
    """Zip a directory `src` to a `.zip` file.

    Args:
        src: The source directory.
        dst: The target `.zip` file.
    Returns:
        None
    """
    dst = p2s(dst); shutil.make_archive(dst[:-4] if dst.endswith('.zip') else dst, format='zip', root_dir=p2s(src))

def Unzip(src, dst):
    """Unzip a `.zip` file to a directory `src`.

    Args:
        src: The source `.zip` file.
        dst: The targert directory.
    Returns:
        None
    """
    shutil.unpack_archive(p2s(src), extract_dir=dst, format='zip')

from os.path import expanduser
PYHEAVEN_PATH = pjoin(expanduser("~"), ".pyheaven")