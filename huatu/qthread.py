import time

import sys
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtCore import QThread


# 装饰器，用于测量阻塞计时
def test_time(func1):
    def train(self):
        start_time = time.time()
        res = func1(self)
        end_time = time.time()
        print(end_time - start_time)
        # logger.info(f'the ocr parse time is {end_time-start_time} s')
        return res

    return train


class pictureOCR(QThread):
    """
    对图片进行ocr识别，，功能服务，可单独放一个文件
    """
    signal = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(pictureOCR, self).__init__()
        self.main_win = kwargs.get('main_win')
        self.signal.connect(self.refresh)

    @test_time
    def run(self):
        m = 0
        while True:
            time.sleep(2)  # 制造阻塞
            m += 1
            self.signal.emit(m)
            print('任务执行中')

    def refresh(self, m):
        self.main_win.line_edit.setText(str(m))


class MainWindow(QtWidgets.QMainWindow):
    """pyqt主界面"""


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.setupUi(self)
        self.resize(500, 300)

        self.p = pictureOCR(main_win=self)  # 把主函数对象传给服务，方便服务操作控件

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText('开始异步任务')
        self.pushButton.clicked.connect(self.click_event)

        self.line_edit = QtWidgets.QLineEdit(self)
        self.line_edit.move(200,0)

    def click_event(self):
        self.p.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
