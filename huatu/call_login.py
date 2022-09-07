# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'

#

# Created by: PyQt5 UI code generator 5.11.3

#

# WARNING! All changes made in this file will be lost!

#导入程序运行必须模块

import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中

from PyQt5.QtWidgets import QApplication, QMainWindow

#导入designer工具生成的login模块

from login import Ui_Form

from PyQt5.QtCore import QThread

#huatu

import huatutest

class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):

        super(MyMainForm, self).__init__(parent)

        self.setupUi(self)

        self.d = Draw(main_win = self)

        self.drew.clicked.connect(self.click_event)

        self.exit.clicked.connect(self.close)

    def click_event(self):
        self.d.start()

    def close(self):

        sys.exit(app.exec_())

class Draw(QThread):
    signal = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(Draw,self).__init__()
        self.main_win = kwargs.get('main_win')
        self.signal.connect(self.refresh)

    def run(self):

        ret = 0
        x = self.main_win.x_line.text()
        y = self.main_win.y_line.text()
        
        self.main_win.textBrowser.setText('画图中:' + x + '*' + y + '\n' +
                                'Start Gen Test Screen Files ...'+'\n')
        self.main_win.textBrowser.repaint()

        ret = huatutest.draw(x, y)
        if ret == 1:
            ret = 0
            self.main_win.textBrowser.setText('错误，请重新输入正确的分辨率')
            self.main_win.textBrowser.repaint()
        else:
            self.main_win.textBrowser.setText('Generate Success!\n'+'保存路径：D:\pattern')

    def refresh(self, m):
        self.main_win.line_edit.setText(str(m))


if __name__ == "__main__":

    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行

    app = QApplication(sys.argv)

    #初始化

    myWin = MyMainForm()

    #将窗口控件显示在屏幕上

    myWin.show()

    #程序运行，sys.exit方法确保程序完整退出。

    sys.exit(app.exec_())