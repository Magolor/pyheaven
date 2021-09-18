from .file_utils import *
from .misc_utils import Clipped
import PySide6

from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLayout,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QProgressDialog,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QSpinBox,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from PySide6 import QtGui
from PySide6.QtGui import (
    QFont,
    QIcon,
)

from PySide6 import QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QRect,
    Qt,
)

from functools import partial

def QWrapped(widget):
    grid = QGridLayout()
    widget.setLayout(grid)
    widget.setMaximumSize(65536, 65536)
    widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    grid.setContentsMargins(10, 10, 10, 10)
    grid.setSpacing(2)
    return widget

def QAdd(widget, module, pos, span, **args):
    instance = module(widget, **args)
    widget.layout().addWidget(instance, pos[0], pos[1], span[0], span[1])
    instance.setMaximumSize(65536, 65536)
    instance.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    return instance

def QGetInput(base, title, question, default=None):
    answer, done = QInputDialog.getText(base, title, question)
    return answer if done else default

def QGetFolder(base, title, default):
    folder = QFileDialog.getExistingDirectory(base, title, default)
    return folder if folder!="" and ExistFolder(folder) else None

def QGetFile(base, title, default, filter="All Files (*)"):
    file, file_type = QFileDialog.getOpenFileName(base, title, default, filter=filter)
    return file if file!="" and file_type!="" and ExistFile(file) else None

def QGetNewFile(base, title, default="C:/", filter="All Files (*)"):
    file, file_type = QFileDialog.getSaveFileName(base, title, default, filter=filter)
    return file if file!="" and file_type!="" else None

class QWaiter(QProgressDialog):
    def __init__(self, base, title, min_dur=1000):
        super(QProgressDialog, self).__init__(base)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModal)
        self.setCancelButton(None)
        self.setMinimumDuration(min_dur)
        self.setRange(0, 100)

def QWait(base, title, label, generator, min_dur=1000, default_label="", **args):
    waiter = QWaiter(base, title, min_dur, **args)
    waiter.setLabelText(default_label)
    return_value = None
    for (elapsed,total,done,info) in generator:
        waiter.setLabelText(label.format(elapsed,total,done,info))
        waiter.setValue(Clipped(int(float(elapsed)/float(total)*100),0,99))
        if done:
            return_value = info; break
    waiter.setValue(100)
    waiter.hide()
    waiter.close()
    return return_value

def QHint(base, title, message):
    hint = QMessageBox(base)
    hint.setWindowTitle(title)
    hint.setWindowModality(Qt.WindowModal)
    hint.setText(message)
    hint.exec()

def QConfirm(base, title, message):
    return (QMessageBox.question(base, title, message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes)

