import sys
from importlib import import_module
from subprocess import Popen, PIPE, STDOUT
try:
    from typing import Union, Literal, Optional, List, Dict
except ImportError:
    from typing import Union, Optional, List, Dict
    from typing_extensions import Literal

def CMD(command:str, wait:bool=True, shell:bool=True, sudo:bool=False, **args):
    """Call system cmd console to execute a command (`subprocess.Popen`).

    Args:
        command (str): The command to be executed. Should be a str of can be converted to str.
        wait (bool): If True, wait until the command finishes and return the handle, otherwise directly return the handle.
        shell (bool): If True, display shell for `subprocess.Popen`, otherwise ignored.
        sudo (bool): If True, pre-attach "sudo" in front of the command, otherwise ignored.
        args: Custom args for `Popen` to be appended.
    Returns:
        Return the handle created by `subprocess.Popen`.
    """
    sudo_command = ("sudo " if sudo else "")+str(command)
    h = Popen(sudo_command,shell=shell,**args)
    if wait:
        h.wait()
    return h

def BUILTIN_PIP_SOURCES():
    return {
        "": "",
        "aliyun": "http://mirrors.aliyun.com/pypi/simple/",
        "douban": "http://pypi.douban.com/simple/",
        "tuna": "http://pypi.tuna.tsinghua.edu.cn/simple/",
        "ustc": "http://pypi.mirrors.ustc.edu.cn/simple/",
    }
def PIP(package:str, source:str="", pip3:bool=True, upgrade:bool=False, force:bool=False, force_deps:bool=False, https:bool=False, args:str=""):
    """Install a python package by pip (or pip3), with built-in sources and other settings wrapped. Please refer to function `BUILTIN_PIP_SOURCES()` for built-in sources.

    Args:
        package (str): The package name to be installed.
        source (str): "--index-url" and "--trusted-host" setting. There are some built-in sources, but you could also specify your own sources by passing the url. The url should be valid and starts with "http://" or "https://".
        pip3 (bool): If True, use "pip3", otherwise "pip".
        upgrade (bool): If True, use "--upgrade", otherwise ignored.
        force (bool): If True, use "--force-reinstall", otherwise ignored.
        force_deps (bool): If False and "force" is set to True, use "--no-deps", otherwise ignored.
        https (bool): If True, replace built-in sources to corresponding https version, it does NOT work for custom sources.
        args (str): Custom args for pip (or pip3) to be appended.
    Returns:
        None
    """
    package = str(package).lower()  # Pypi is case insensitive
    index_url = BUILTIN_PIP_SOURCES()[source].replace("http://", "https://" if https else "http://") if source in BUILTIN_PIP_SOURCES() else source
    trusted_host = index_url.split("https://" if https else "http://")[-1].split("/")[0]
    source_command = f"--index-url {index_url} --trusted-host {trusted_host} " if source!="" else ""
    upgrade_command = "--upgrade " if upgrade else ""
    reinstall_command = "--force-reinstall " if force else ""
    nodeps_command = "--no-deps " if (force and not force_deps) else ""
    pip_command = "pip3" if pip3 else "pip"
    CMD(f"{pip_command} install {package} {source_command}{upgrade_command}{reinstall_command}{nodeps_command}{args}",wait=True)

def RSYNC(src:str, dst:str, wait:bool=True, args:str="-r -vP"):
    """Call system cmd console to execute `rsync` command (`subprocess.Popen`).

    Args:
        src (str): The source path of `rsync`.
        dst (str): The destination path of `rsync`.
        wait (bool): If True, wait until the command finishes and return the handle, otherwise directly return the handle.
        args: Custom args for `Popen` to be appended.
    Returns:
        Return the handle created by `subprocess.Popen`.
    """
    return CMD(
        f"rsync {args} {src} {dst}", wait=wait
    )

def __import_unsafe__(name:str, alias:str, module_globals:Dict, force_reimport:bool=False):
    if force_reimport or (alias not in module_globals):
        if (alias is None) and ("." in name):
            __import_unsafe__(name.split('.')[0], name.split('.')[0], module_globals=module_globals, force_reimport=force_reimport)
        else:
            if alias is None:
                alias = name
            try:
                module = import_module(name)
                module_globals.update({alias:module})
                return
            except:
                pass
            
            try:
                if "." in name:
                    parent, mod = ".".join(name.split('.')[:-1]), name.split('.')[-1]
                    module = import_module(parent).__dict__[mod]
                    module_globals.update({alias:module})
                    return
            except:
                pass
            
            raise ImportError(name)

def USEFUL_PYTHON_PACKAGES_BUILTIN():
    """List of useful packages in python standard libraries, encoded as a comma separated string."""
    return "re,os,sys,pdb,glob,math,time,json,copy,types,random,shutil,string,pickle,zipfile,marshal,logging,pathlib,inspect,"\
        +  "argparse,itertools,subprocess,collections,PIL.Image.Image@Image,collections.defaultdict@defaultdict,"\
        +  "collections.abc.Iterable@iterable,copy.copy@copy,copy.deepcopy@deepcopy,pathlib.Path@Path,"\
        +  "pathlib.PurePosixPath@PurePosixPath"
def USEFUL_PYTHON_PACKAGES_EXTRA():
    """List of useful packages NOT in python standard libraries, encoded as a comma separated string."""
    return "tqdm,jsonlines,requests,sklearn,numpy@np,pandas@pd,seaborn@sns,matplotlib@mpl,matplotlib.pyplot@plt"
def USEFUL_PYTHON_PACKAGES_TORCH():
    """List of useful packages in pytorch, encoded as a comma separated string."""
    return "torch,torch,torch.nn@nn,torch.nn.init@nninit,torch.nn.functional@F,torch.optim@optim,torch.optim.lr_scheduler@sched,"\
        +  "torch.utils.data@TUD,torch.utils.data.DataLoader@DataLoader,torch.utils.data.Dataset@Dataset,torch.nn.parallel.DistributedDataParallel@DDP,"\
        +  "torchvision,torchvision.datasets@TVD,torchvision.transforms@TVT"

def Import(packages:Union[List[str],str], module_globals, mode:Literal['strict','install_strict','install_ignore','ignore']='ignore', force_reimport:bool=False, **install_args):
    """Dynamically import packages.

    Args:
        packages (str or List[str]): The package or packages to be imported. Use "@" for alias. Order matters: please place parent packages before their children.
        module_globals: The `globals()` of the module that performs the import. You should almost always put `module_globals=globals()` here.
        mode (str): If set to "strict", failures directly result in `ImportError`.
                    If set to "install_strict", try to install missing packages using `PIP` with arguments in `install_args`, and then failures result in `ImportError`.
                    If set to "install_ignore", try to install missing packages using `PIP` with arguments in `install_args`, and then failures are ignored.
                    If set to "ignore", failures are ignored.
        force_reimport (bool): If True, force import even if the module is already imported, otherwise ignored.
        install_args: Arguments for calling `PIP`. Only useful for "install_strict" or "install_ignore" mode.
    Returns:
        List[str]: Packages or functions that failed to be imported.
    """
    packages = [package for package in packages] if not isinstance(packages, str) else packages.split(','); failures = []; errors = []
    for package in packages:
        if package!="":
            failed = False; error = None
            if package.count('@')>1:
                failed = True
            else:
                name, alias = package.split('@') if package.count('@')==1 else (package, None)
                try:
                    __import_unsafe__(name, alias, module_globals=module_globals, force_reimport=force_reimport)
                    failed = False
                except Exception as e:
                    if "install" in mode:
                        try:
                            PIP(name, **install_args)
                            __import_unsafe__(name, alias, module_globals=module_globals, force_reimport=force_reimport)
                            failed = False
                        except:
                            failed = True; error = e
                    else:
                        failed = True; error = e
            if failed:
                failures.append(package)
                errors.append(error)
    if ("strict" in mode) and len(failures)>0:
        raise ImportError(list(zip(failures, errors)))
    else:
        return failures

def ForName(cls:str):
    """Return a class by class name.

    Args:
        cls (str): Class name.
    Returns:
        type: The class.
    """
    return sys.modules[cls]