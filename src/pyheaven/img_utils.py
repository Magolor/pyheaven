from .file_utils import *
from PIL import Image
import numpy as np

def GrayScale(r, g, b):
    """Fast computation of gray scale given red, green, and blue data, each could be a value or an array of arbitrary shape, as long as the shape is the same.

    The computation is not accurate, instead, it uses fixed finite 1e-3 precision. The reason is to speedup computation using only integer:

    GrayScale(r,g,b) = floor((r * 299 + g * 587 + b * 114 + 500) / 1000)

    Args:
        r: The red channel of the image.
        g: The green channel of the image.
        b: The blue channel of the image.
    Returns:
        Any: The gray scale computed from r, g, b data, with finite 1e-3 precision.
    """
    r = np.array(r, dtype=int); g = np.array(g, dtype=int); b = np.array(b, dtype=int)
    return np.array(np.floor((r * 299 + g * 587 + b * 114 + 500) / 1000), dtype=np.uint8)

def DataToImg(data):
    """Convert an array-like data (values in 0 ~ 255) to image.

    Args:
        data: The array-like data.
    Returns:
        Image: The converted image.
    """
    return data if isinstance(data, Image.Image) else Image.fromarray(np.uint8(data))

def d2i(data):
    """Convert an array-like data (values in 0 ~ 255) to image.

    This is a short alias for `DataToImg`.

    Args:
        data: The array-like data.
    Returns:
        Image: The converted image.
    """
    return data if isinstance(data, Image.Image) else Image.fromarray(np.uint8(data))

def ImgToData(data):
    """Convert a PIL Image to array-like data.

    Args:
        img: The PIL Image.
    Returns:
        np.ndarray: The converted data.
    """
    return data if isinstance(data, np.ndarray) else np.array(data)

def i2d(data):
    """Convert a PIL Image to array-like data.

    This is a short alias for `ImgToData`.

    Args:
        img: The PIL Image.
    Returns:
        np.ndarray: The converted data.
    """
    return data if isinstance(data, np.ndarray) else np.array(data)

def DebugImgData(data):
    """Show an array-like data (values in 0 ~ 255) as image.

    Args:
        data: The array-like data.
    Returns:
        None
    """
    img = d2i(data); img.show(); img.close()

def SaveImgData(data, path, compress_level=0):
    """Save an array-like data (values in 0 ~ 255) as image, with no image compression.

    Args:
        data: The array-like data.
        path: The target image path.
        compress_level (bool): The `compress_level` of `Image.save`.
    Returns:
        None
    """
    img = d2i(data); img.save(p2s(path), compress_level=compress_level); img.close()

def RGBImg(img, transparent=np.array([0,0,0],dtype=float)):
    """Convert an image to image of 3 channels. Assuming the input image are RGB if it is already a 3-channel image, and RGBA if it is a 4-channel image.

    Supported image shapes are: (W,H), (W,H,1), (W,H,3), (W,H,4).

    Args:
        img: The image to be converted.
        transparent: The transparent color in RGB form (used for converting RGBA), e.g.: `np.array([255,255,255],dtype=float)` stands for white.
    Returns:
        np.ndarray: The converted image data.
    """
    img = deepcopy(i2d(img))
    if len(img.shape) == 2:
        img = np.stack([img, img, img], axis=(-1))
    elif img.shape[(-1)] == 1:
        img = np.concatenate([img, img, img], axis=(-1))
    elif img.shape[(-1)] == 3:
        pass
    elif img.shape[(-1)] == 4:
        img = img.astype(np.float); bg = np.broadcast_to(transparent,img[:,:,:3].shape)
        alpha = np.stack([img[:, :, 3], img[:, :, 3], img[:, :, 3]], axis=(-1)) / 255
        img = np.array((np.uint8((img[:, :, :3]*alpha+bg*(1-alpha)))), dtype=(np.uint8))
    else:
        raise SystemError
    return img