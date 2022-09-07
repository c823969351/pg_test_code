# -*- coding: utf-8 -*-

__author__ = 'chenjiwen'


#导入程序运行必须模块

from logging import exception
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中

from PyQt5.QtWidgets import *

#导入designer工具生成的login模
from ui import Ui_Form
from PyQt5 import QtCore

from PyQt5.QtCore import QThread, pyqtSignal,pyqtSlot


class MyMainForm(QtWidgets.QTableWidget, Ui_Form):
    def __init__(self, parent=None):

        super(MyMainForm, self).__init__(parent)

        self.setupUi(self)



if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行

    app = QApplication(sys.argv)

    #初始化

    myWin = MyMainForm()

    #将窗口控件显示在屏幕上

    myWin.show()

    #程序运行，sys.exit方法确保程序完整退出。

    sys.exit(app.exec_())