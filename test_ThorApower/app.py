# -*- coding: utf-8 -*-

__author__ = 'chenjiwen'


#导入程序运行必须模块

from fileinput import filename
from logging import exception
import sys
from telnetlib import PRAGMA_HEARTBEAT
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import os
import time
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中

from PyQt5.QtWidgets import *

#导入designer工具生成的login模块

from ui import Ui_Test_power

from PyQt5.QtCore import QThread, pyqtSignal,pyqtSlot
import Test
import Find_PG
import PGtest_log
import zhexiantu

nowtime = time.localtime()
strftime = time.strftime("%Y%m%d", nowtime)
logfile = ('pytest-' + strftime + '.log')
log = PGtest_log.Logger(logfile, level='info')

file_name = ''

def time_monitor():
    print('************')
    nowtime = time.localtime()
    strftime_1 = time.strftime("%Y%m%d-%H-%M-%S", nowtime)
    file_1 = os.getcwd()
    name = file_1+'\\电源测试数据\\电源测试{}.csv'.format(strftime_1)
    global file_name
    file_name = name
    print(file_name)
    



class MyMainForm(QtWidgets.QTableWidget, Ui_Test_power):
    def __init__(self, parent=None):

        super(MyMainForm, self).__init__(parent)

        self.setupUi(self)
        self.work = WorkThread(main_win = self)
        self.startputten.clicked.connect(self.test)
        self.exitputten.clicked.connect(self.close)
        self.open_csv.clicked.connect(self.openfile)
        self.work.signal.connect(self.signal_check)
        self.tcpcheck.clicked.connect(self.check_tcp)
    
    def check_tcp(self):
        self.set_btn()
        tcp_ip = Find_PG.pg_ip()
        if tcp_ip:
            self.tcpcheck.setStyleSheet("background: rgb(0,255,0)")
        else:
            self.tcpcheck.setStyleSheet("background: rgb(255,0,0)")
            self.message_warning()
    
    def csv_reader(self):
        df = zhexiantu.line_chart(file_name)
        df.drew()
    
        
    def test(self):
        self.startputten.setEnabled(False)

        global ch,v_min,v_max,step

        ch = self.channl.text()
        v_min = self.startvolt.text()
        v_max = self.finvolt.text()
        step = self.step.text()

        self.work.start()

        '''try:
            M_work = Test.Test_power(ch,v_min,v_max,step)
            ret_pro = M_work.main()
            for i in ret_pro:
                self.signal_check(i)
        except Exception as e:
            log.logger.error('run:%s', e)
            self.signal_check(-1)'''


    def openfile(self):
        try:
            self.csv_reader()
            os.startfile(file_name)
        except Exception as e:
            log.logger.error('file:%s', e)
            self.message_warning()

    def signal_check(self,ret):
        if ret == 100:
            self.set_probar(100)
            self.message_done()
        elif ret == -1:
            self.set_probar(0)
            self.message_warning()
        else:
            self.set_probar(ret)

    def set_btn(self):
        self.startputten.setEnabled(True)
    
    def set_probar(self,value=0):
        self.progressBar.setProperty("value", value)
        QApplication.processEvents()


    def message_warning(self):
     #提示
     msg_box = QMessageBox(QMessageBox.Warning, '警告', '系统异常')
     msg_box.exec_()
     self.set_btn()
     self.set_probar(0)

    def message_done(self):
     #提示
     msg_box = QMessageBox(QMessageBox.Information, '提示', '测试完成')
     msg_box.exec_()
     self.set_btn()

    def close(self):
        sys.exit(app.exec_())

class WorkThread(QThread):
    signal = pyqtSignal(int)

    def __init__ (self,*args,**kwargs):
        super(WorkThread, self).__init__()
        self.main_win = kwargs.get('main_win')
    def run(self):
        try:
            time_monitor()
            M_work = Test.Test_power(ch,v_min,v_max,step,file_name)
            for i in M_work.main():
                self.signal.emit(i)
        except Exception as e:
            log.logger.error('run:%s', e)
            self.signal.emit(-1)





if __name__ == "__main__":

    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行

    app = QApplication(sys.argv)

    #初始化

    myWin = MyMainForm()

    #将窗口控件显示在屏幕上

    myWin.show()

    #程序运行，sys.exit方法确保程序完整退出。

    sys.exit(app.exec_())