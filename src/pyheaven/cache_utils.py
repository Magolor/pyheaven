from .file_utils import *
from .misc_utils import MD5, Attempt
from .serialize_utils import LoadPickle, SavePickle, LoadJson, SaveJson

def CacheInit(path, clear=True, rm=False):
    """Initialize a cache path.
    
    Args:  
        path (str): The cache path.
        clear (bool): Whether to clear the cache directory.
        rm (bool): If True, use `shutil` to enforce remove, otherwise `send2trash` only.
    Returns:
        None
    """
    if clear:
        ClearFolder(path, rm=rm)
    else:
        CreateFolder(path)
        # Check for the integrity of the cache directory
        # 1. Remove all the lock files
        for file in ListFiles(path):
            if file.endswith('.lock'):
                Delete(file, rm=True)
        # 2. Make sure all key files have corresponding value files and vice versa
        for file in ListFiles(path):
            if file.endswith('.key'):
                if not ExistFile(AsFormat(file, '.value')):
                    Delete(file, rm=True)
        for file in ListFiles(path):
            if file.endswith('.value'):
                if not ExistFile(AsFormat(file, '.key')):
                    Delete(file, rm=True)
    return path

def CacheLock(path, key):
    """Lock a cache file.

    Args:
        path (str): The cache path.
        key (str): The key of the cache file.
    Returns:
        bool: True if the lock is successful, False if the cache file is already locked.
    """
    h = MD5(key)
    if ExistFile(pjoin(path, f"{h}.lock")):
        return False
    CreateFile(pjoin(path, f"{h}.lock"))
    return True


def CacheWait(path, key, retry_time=-1, retry_gap=0.0):
    """Wait until the cache file is unlocked.
    
    Args:
        path (str): The cache path.
        key (str): The key of the cache file.
        retry_time (int): The maximum number of retries. If `retry_time` is 0, the function will be executed only once. If `retry_time` is smaller than 0, the function will be executed indefinitely until it succeeds.
        retry_gap (float): The time gap between retries.
    """
    def wait_lock():
        assert CacheLock(path, key); return True
    return Attempt(wait_lock, retry_time=retry_time, retry_gap=retry_gap, default=False)

def CacheUnlock(path, key):
    """Unlock a cache file.

    Args:
        path (str): The cache path.
        key (str): The key of the cache file.
    Returns:
        None
    """
    h = MD5(key)
    if ExistFile(pjoin(path, f"{h}.lock")):
        Delete(pjoin(path, f"{h}.lock"), rm=True)

def CacheExist(path, key):
    """Check if the cache file exists.

    Args:
        path (str): The cache path.
        key (str): The key of the cache file.
    Returns:
        bool: True if the cache file exists, False otherwise.
    """
    h = MD5(key)
    return ExistFile(pjoin(path, f"{h}.key"))

def CacheGet(path, key, default=None, load_func=LoadPickle, locking=False, retry_time=-1, retry_gap=0.0):
    """Get the content of a cache file.

    Args:
        path (str): The cache path.
        key (str): The key of the cache file.
        default: The default value if the cache file does not exist.
        load_func: The function to load the cache file. Default is `LoadPickle`.
        locking: If True, use lock to prevent multiple processes from writing the cache file at the same time.
        retry_time (int): The maximum number of retries to get lock of the cache. If `retry_time` is 0, the function will be executed only once. If `retry_time` is smaller than 0, the function will be executed indefinitely until it succeeds. Only effective when `locking` is True.
        retry_gap (float): The time gap between retries to get lock of the cache. Only effective when `locking` is True.
    Returns:
        Any: The content of the cache file, or `default` if the cache file does not exist.
    """
    h = MD5(key)
    if not CacheExist(path, key):
        return default
    if locking:
        lock = CacheWait(path, key, retry_time=retry_time, retry_gap=retry_gap)
        if not lock:
            raise Exception("The cache file is used by another process for a long time. A deadlock may occur.")
    value = load_func(pjoin(path, f"{h}.value"))
    CacheUnlock(path, key)
    return value

def CacheSet(path, key, value, overwrite=True, load_func=LoadPickle, save_func=SavePickle, locking=False, retry_time=-1, retry_gap=0.0, force=False):
    """Set the content of a cache file.

    Args:
        path (str): The cache path.
        key (str): The key of the cache file.
        value: The content to be saved.
        overwrite (bool): If True, overwrite the cache file if it already exists.
        load_func: The function to load the cache file. Default is `LoadPickle`.
        save_func: The function to save the cache file. Default is `SavePickle`.
        locking: If True, use lock to prevent multiple processes from writing the cache file at the same time.
        retry_time (int): The maximum number of retries to get lock of the cache. If `retry_time` is 0, the function will be executed only once. If `retry_time` is smaller than 0, the function will be executed indefinitely until it succeeds. Only effective when `locking` is True.
        retry_gap (float): The time gap between retries to get lock of the cache. Only effective when `locking` is True.
        force (bool): If True, force to write the cache file without lock.
    Returns:
        Any: The final value cached for the key. If the cache file already exists and `overwrite` is False, the original value saved in the cache file will be returned, otherwise the new value will be returned.
    """
    h = MD5(key)
    if not overwrite and CacheExist(path, key):
        return CacheGet(path, key, default=None, load_func=load_func, save_func=save_func, locking=locking, retry_time=retry_time, retry_gap=retry_gap)
    if locking:
        lock = CacheWait(path, key, retry_time=retry_time, retry_gap=retry_gap)
        if not lock and not force:
            raise Exception("The cache file is used by another process for a long time. A deadlock may occur. Try force write the cache file by setting `force` to True.")
    save_func(key, pjoin(path, f"{h}.key"))
    save_func(value, pjoin(path, f"{h}.value"))
    CacheUnlock(path, key)
    return value

def CacheDelete(path, key, rm=True, locking=False, retry_time=-1, retry_gap=0.0, force=False):
    """Delete a cached key.

    Args:
        path (str): The cache path.
        key (str): The key of the cache file.
        rm (bool): If True, use `shutil` to enforce remove, otherwise `send2trash` only.
        locking: If True, use lock to prevent multiple processes from writing the cache file at the same time.
        retry_time (int): The maximum number of retries to get lock of the cache. If `retry_time` is 0, the function will be executed only once. If `retry_time` is smaller than 0, the function will be executed indefinitely until it succeeds. Only effective when `locking` is True.
        retry_gap (float): The time gap between retries to get lock of the cache. Only effective when `locking` is True.
        force (bool): If True, force to write the cache file without lock.
    Returns:
        None
    """
    h = MD5(key)
    if not CacheExist(path, key):
        return
    if locking:
        lock = CacheWait(path, key, retry_time=retry_time, retry_gap=retry_gap)
        if not lock:
            raise Exception("The cache file is used by another process for a long time. A deadlock may occur.")
    Delete(pjoin(path, f"{h}.key"), rm=rm)
    Delete(pjoin(path, f"{h}.value"), rm=rm)
    Delete(pjoin(path, f"{h}.lock"), rm=True)

def CacheKeys(path, load_func=LoadPickle):
    """Get all cached keys.

    Args:
        path (str): The cache path.
        load_func: The function to load the cache file. Default is `LoadPickle`.
    Returns:
        List[str]: A list of all keys.
    """
    keys = []
    for file in ListFiles(path, ordered=True):
        if file.endswith('.key'):
            keys.append(load_func(pjoin(path, file)))
    return keys

def CacheItems(path, load_func=LoadPickle, locking=False, retry_time=-1, retry_gap=0.0):
    """Get all cached key-value pairs.

    Args:
        path (str): The cache path.
        load_func: The function to load the cache file. Default is `LoadPickle`.
        locking: If True, use lock to prevent multiple processes from writing the cache file at the same time.
        retry_time (int): The maximum number of retries to get lock of the cache. If `retry_time` is 0, the function will be executed only once. If `retry_time` is smaller than 0, the function will be executed indefinitely until it succeeds. Only effective when `locking` is True.
        retry_gap (float): The time gap between retries to get lock of the cache. Only effective when `locking` is True.
    Returns:
        List[Tuple(Any, Any)]: A list of all key-value pairs.
    """
    for file in ListFiles(path, ordered=True):
        if file.endswith('.key'):
            key = load_func(pjoin(path, file))
            value = CacheGet(path, key, load_func=load_func, locking=locking, retry_time=retry_time, retry_gap=retry_gap)
            yield (key, value)
    return