from .file_utils import *
from .args_utils import MemberDict
from .misc_utils import Clipped
import PySide6

from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDialog,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
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
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGuiApplication,
    QIcon,
    QLinearGradient,
    QPalette,
    QPainter,
    QPixmap,
    QRadialGradient
)

from PySide6 import QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QTimer,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QUrl,
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

def QGetFolder(base, title, default=""):
    folder = QFileDialog.getExistingDirectory(base, title, default)
    return folder if folder!="" and ExistFolder(folder) else None

def QGetFile(base, title, default="C:/", filter="All Files (*)"):
    file, file_type = QFileDialog.getOpenFileName(base, title, default, filter=filter)
    return file if file!="" and file_type!="" and ExistFile(file) else None

def QGetFiles(base, title, default="C:/", filter="All Files (*)"):
    files, file_types = QFileDialog.getOpenFileNames(base, title, default, filter=filter)
    result = [(file if file!="" and file_type!="" and ExistFile(file) else None) for (file, file_type) in zip(files, file_types)]
    return result if len(result)>0 else None

def QGetNewFile(base, title, default="C:/", filter="All Files (*)"):
    file, file_type = QFileDialog.getSaveFileName(base, title, default, filter=filter)
    return file if file!="" and file_type!="" else None

def QHint(base, title, message):
    hint = QMessageBox(base)
    hint.setWindowTitle(title)
    hint.setWindowModality(Qt.WindowModal)
    hint.setText(message)
    hint.exec()

def QConfirm(base, title, message):
    return (QMessageBox.question(base, title, message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes)

# Modified from https://github.com/Wanderson-Magalhaes/Python_PySide2_Circular_ProgressBar_Modern_GUI
class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen, **args):
        if SplashScreen.objectName():
            SplashScreen.setObjectName(u"SplashScreen")
        SplashScreen.resize(360, 360)
        self.centralwidget = QWidget(SplashScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.circularProgressBarBase = QFrame(self.centralwidget)
        self.circularProgressBarBase.setObjectName(u"circularProgressBarBase")
        self.circularProgressBarBase.setGeometry(QRect(10, 10, 320, 320))
        self.circularProgressBarBase.setFrameShape(QFrame.NoFrame)
        self.circularProgressBarBase.setFrameShadow(QFrame.Raised)
        self.circularProgress = QFrame(self.circularProgressBarBase)
        self.circularProgress.setObjectName(u"circularProgress")
        self.circularProgress.setGeometry(QRect(10, 10, 300, 300))
        self.circularProgress.setStyleSheet(u"QFrame{\n"
"   border-radius: 150px;\n"
"   background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.749 rgba(255, 0, 127, 0), stop:0.750 rgba(85, 170, 255, 255));\n"
"}")
        self.circularProgress.setFrameShape(QFrame.NoFrame)
        self.circularProgress.setFrameShadow(QFrame.Raised)
        self.circularBg = QFrame(self.circularProgressBarBase)
        self.circularBg.setObjectName(u"circularBg")
        self.circularBg.setGeometry(QRect(10, 10, 300, 300))
        self.circularBg.setStyleSheet(u"QFrame{\n"
"   border-radius: 150px;\n"
"   background-color: "+args['bg_color']+";\n"
"}")
        self.circularBg.setFrameShape(QFrame.NoFrame)
        self.circularBg.setFrameShadow(QFrame.Raised)
        self.container = QFrame(self.circularProgressBarBase)
        self.container.setObjectName(u"container")
        self.container.setGeometry(QRect(20, 20, 280, 280))
        self.container.setStyleSheet(u"QFrame{\n"
"   border-radius: 135px;\n"
"   background-color: "+args['container_color']+";\n"
"}")
        self.container.setFrameShape(QFrame.NoFrame)
        self.container.setFrameShadow(QFrame.Raised)
        self.widget = QWidget(self.container)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(30, 40, 220, 210))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelTitle = QLabel(self.widget)
        self.labelTitle.setObjectName(u"labelTitle")
        font = QFont()
        font.setFamily(args['title_font_family'])
        font.setPointSize(args['title_font_size'])
        self.labelTitle.setFont(font)
        self.labelTitle.setStyleSheet(u"background-color: none;\n"
"color: #FFFFFF")
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelTitle, 0, 0, 1, 1)

        self.labelPercentage = QLabel(self.widget)
        self.labelPercentage.setObjectName(u"labelPercentage")
        font1 = QFont()
        font1.setFamily(args['percentage_font_family'])
        font1.setPointSize(args['percentage_font_size'])
        self.labelPercentage.setFont(font1)
        self.labelPercentage.setStyleSheet(u"background-color: none;\n"
"color: #FFFFFF")
        self.labelPercentage.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelPercentage, 1, 0, 1, 1)

        self.labelLoadingInfo = QLabel(self.widget)
        self.labelLoadingInfo.setObjectName(u"labelLoadingInfo")
        self.labelLoadingInfo.setMinimumSize(QSize(0, 24))
        self.labelLoadingInfo.setMaximumSize(QSize(16777215, 24))
        font2 = QFont()
        font2.setFamily(args['info_font_family'])
        font2.setPointSize(args['info_font_size'])
        self.labelLoadingInfo.setFont(font2)
        self.labelLoadingInfo.setStyleSheet(u"QLabel{\n"
"   border-radius: 10px;    \n"
"   background-color: "+args['label_color']+";\n"
"   color: #FFFFFF;\n"
"   margin-left: 0px;\n"
"   margin-right: 0px;\n"
"}")
        self.labelLoadingInfo.setFrameShape(QFrame.NoFrame)
        self.labelLoadingInfo.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelLoadingInfo, 2, 0, 1, 1)

        self.labelCredits = QLabel(self.widget)
        self.labelCredits.setObjectName(u"labelCredits")
        self.labelCredits.setFont(font2)
        self.labelCredits.setStyleSheet(u"background-color: none;\n"
"color: rgb(155, 155, 255);")
        self.labelCredits.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelCredits, 3, 0, 1, 1)

        self.circularBg.raise_()
        self.circularProgress.raise_()
        self.container.raise_()
        layout = QVBoxLayout()
        layout.addWidget(self.centralwidget)
        SplashScreen.setLayout(layout)

        self.retranslateUi(SplashScreen, **args)

        QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen, **args):
        SplashScreen.setWindowTitle(QCoreApplication.translate("SplashScreen", args['window_name'], None))
        self.labelTitle.setText(QCoreApplication.translate("SplashScreen", u"<html><head/><body><p><span style=\" font-weight:bold; color:#9b9bff;\">"+args['title']+"</span> "+args['subtitle']+"</p></body></html>", None))
        self.labelPercentage.setText(QCoreApplication.translate("SplashScreen", u"<p><span style=\" font-size:"+str(args["percentage_font_size"])+"pt;\">"+str(args['__expression__'])+"</span></p>", None))
        self.labelLoadingInfo.setText(QCoreApplication.translate("SplashScreen", args['__loading_info__'], None))
        self.labelCredits.setText(QCoreApplication.translate("SplashScreen", args['credits'], None))

class QCircularProgressDialog(QDialog):
    def __init__(self, refresh=100, cut=32, optimize=False, window_name="", title="", subtitle="", loading_info="loading...", credits="by: Wanderson M. Pimenta"):
        super().__init__()
        self.cut = max(cut,3)
        self.refresh = refresh
        self.optimize = optimize
        self.ui = Ui_SplashScreen()
        self.ui_info = MemberDict({
            'value': 0,

            'window_name': "",
            'title': title,
            'subtitle': subtitle,
            'loading_info': loading_info,
            '__loading_info__': None,
            'credits': credits,

            'title_font_family': "YaHei Consolas Hybrid",
            'title_font_size': 10,
            'info_font_size': 8,
            'info_font_family': "YaHei Consolas Hybrid",
            'percentage_font_size': 32,
            'percentage_font_family': "Consolas",

            'progress_color': "rgba(85, 170, 255, 255)",
            'container_color': "rgb(77, 77, 127)",
            'bg_color': "rgba(77, 77, 127, 120)",
            'label_color': "rgb(93, 93, 154)",

            'expression': None,
            '__expression__': None
        })
        self.ui.setupUi(self, **self.ui_info)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.circularBg.setGraphicsEffect(self.shadow)

        self.finished = False
        self.timer = QTimer()
        self.timer.timeout.connect(self._refresh)
        self.timer.start(self.refresh)
        self.setValue(0)

        self.center()
        self.show()
        self.activateWindow()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _refresh(self):
        QApplication.processEvents()

    def setUiInfo(self, infos, refresh=False):
        self.ui_info.update(infos)
        if self.ui_info.expression is None:
            self.ui_info.__expression__ = f"{self.ui_info.value}%"
        else:
            self.ui_info.__expression__ = self.ui_info.expression
        if self.ui_info.loading_info is None:
            self.ui_info.__loading_info__ = None
        else:
            self.ui_info.__loading_info__ = self.ui_info.loading_info if len(self.ui_info.loading_info)<self.cut else "..."+self.ui_info.loading_info[-self.cut+3:]
        if self.finished:
            return
        if self.ui_info.value >= 100:
            self.finished = True
            self.timer.stop()
            self.close()
        else:
            progress = (100 - self.ui_info.value) / 100.0
            stop_1 = str(progress - 0.001); stop_2 = str(progress)
            styleSheet = """
            QFrame{
                border-radius: 150px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} {COLOR});
            }
            """
            newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2).replace('{COLOR}', self.ui_info.progress_color)
            self.ui.circularProgress.setStyleSheet(newStylesheet); self.ui.retranslateUi(self, **self.ui_info); QApplication.processEvents()

    def setValue(self, value):
        self.setUiInfo({'value':Clipped(int(value), 0, 100)})

    def terminate(self):
        self.finished = True
        self.timer.stop()
        self.close()

