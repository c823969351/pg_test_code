from http import server
import threading
from ui import Ui_Update_FPGA
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import os
import Find_PG
import main
from PG_server import ServPg

paths = []

class MyMainForm(QtWidgets.QTableWidget, Ui_Update_FPGA):

    def __init__(self, parent=None):

        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.tcpcheck.setStyleSheet("background: rgb(128,128,128)")
        self.toolButton.clicked.connect(self.input_path)
        self.tcpcheck.clicked.connect(self.check_tcp)
        self.startputten.clicked.connect(self.progressbar_busy)
        self.exitputten.clicked.connect(self.progressbar_reset)
        self.k160Button.setChecked(True)
        self.state = 'k160'
        self.k160Button.toggled.connect(lambda : self.btnstate())
        self.startputten.clicked.connect(self.btnFunc)
        self.exitputten.clicked.connect(self.close)
    
    def check_tcp(self):
        self.set_btn()
        tcp_ip = Find_PG.pg_ip()
        if tcp_ip:
            self.tcpcheck.setStyleSheet("background: rgb(0,255,0)")
            msg_box = QMessageBox(QMessageBox.Information, '提示', 'PG已连接')
            msg_box.exec_()
            pg = ServPg()
            pg.open()
            k160num = pg.k160_version(4)
            ZU7num = pg.ZU7_version()
            self.k160number.setText(str(k160num)[1:-1])
            self.ZU7number.setText(ZU7num)
            pg.close()
            self.progressbar_reset()
        else:
            self.tcpcheck.setStyleSheet("background: rgb(255,0,0)")
            self.message_warning()
            self.progressbar_reset()
    
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

    def message_done(self):
        #提示
        msg_box = QMessageBox(QMessageBox.Information, '提示', '测试完成')
        msg_box.exec_()
        self.set_btn()
    
    def input_path(self):
        fileName,fileType=QtWidgets.QFileDialog.getOpenFileName(None,"选取文件",os.getcwd(),"BIN Files(*.bin);;All Files(*)")
        paths.append(fileName)
        self.Edit_path.setText(fileName)

    def progressbar_busy(self):
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
    
    def progressbar_reset(self):
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)

    def btnstate(self):
        if self.k160Button.isChecked():
            print('k160')
            self.state = 'k160'
        elif self.ZU7Button.isChecked():
            print('ZU7')
            self.state = 'ZU7'
    
    def btnFunc(self):
        self.thread1 = threading.Thread(target= self.work)
        self.thread1.start()
    
    def work(self):
        amain = main.Update_FPGA(self.Edit_path.text(),self.state)
        amain.transfer()
        amain.reboot()
        self.progressbar_reset()
        self.Edit_path.setText('')

    
    def close(self):
        sys.exit(app.exec_())
        


if __name__ == '__main__':
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行

    app = QApplication(sys.argv)

    #初始化

    myWin = MyMainForm()

    #将窗口控件显示在屏幕上

    myWin.show()

    #程序运行，sys.exit方法确保程序完整退出。

    sys.exit(app.exec_())