from .file_utils import *
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

class Plotter(object):
    """A wrapped pyplot pipeline with seaborn styling.
    """
    def __init__(self, figsize=(8,6), dpi=300, path=None, legend=True, sns_style='darkgrid'):
        self.figsize = figsize; self.dpi = dpi; self.path = path; self.legend = legend; self.sns_style = sns_style

    def __enter__(self):
        sns.set(style=self.sns_style)
        fig,axe = plt.subplots(figsize=self.figsize,dpi=self.dpi)
        return (fig,axe)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.legend:
            plt.legend()
        if self.path is not None:
            CreateFile(self.path); plt.savefig(self.path)
        else:
            plt.show()
        plt.close()