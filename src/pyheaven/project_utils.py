from .file_utils import *

def DLProjectTemplate(root, template=None):
    """Build a deep learning project from a given template under directory `root`.

    Args:
        root: The root directory of the project.
        template: The template (todo).
    Returns:
        None
    """
    CreateFolder(pjoin(root,"data"))
    CreateFolder(pjoin(root,"models"))
    # TODO