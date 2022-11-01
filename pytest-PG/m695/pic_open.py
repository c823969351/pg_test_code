import re
import cv2
import time
import pandas as pd
import numpy as np
from PIL import Image


class Video_get(object):

    def __init__(self):
        self.cap = cv2.VideoCapture()  # 准备获取图像
        self.CAM_NUM = 0

    def camera_check(self):
        flag = self.cap.open(self.CAM_NUM)
        if not flag:
            msg = "未检测到相机，请确定是否连接正确"
            print(msg)
            return 0
        else:
            time.sleep(1)
            msg = "相机状态正确"
            print(msg)
            return 1

    def camera_show(self):
        while True:
            #for i in range(2):
            flag, self.image = self.cap.read()
            self.image = cv2.flip(self.image, 1)  # 左右翻转
            #self.takePhoto()
            #print(self.image)
            show = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            show = cv2.cvtColor(self.image, cv2.COLOR_BGR2)
            cv2.imshow("win1", cv2.resize(show, (640, 480)))
            cv2.waitKey(1)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def takePhoto(self):
        flag, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        now_time = time.strftime('%Y-%m-%d-%H-%M-%S',
                                 time.localtime(time.time()))
        print(now_time)
        cv2.imwrite('pic_' + str(now_time) + '.bmp', self.image)
        pic_name = 'pic_' + str(now_time) + '.bmp'
        return pic_name

    def checkdianliang(self):

        find_xiangji = self.camera_check()

        pic_name = self.takePhoto()
        im = Image.open(pic_name)
        array = np.array(im)

        rows = len(array)
        cols = len(array[0])
        #print('长度{col}'.format(col = cols))
        #print('宽度{row}'.format(row = rows))

        #print('屏幕的颜色',array[256,171])
        #print(list(array))

        new_col = int(cols / 2) - 50
        new_row = int(rows / 2) - 50

        #black_slice = array[new_row:(new_row+100),new_col:(new_col+100)]
        black_slice = array[new_col:(new_col + 100), new_row:(new_row + 100)]
        print(list(black_slice))
        black_mask = black_slice <= 150  #此参数卡控灰度值
        jieguo = pd.DataFrame(black_mask)
        jieguo.to_csv('图片数据.csv')
        #print(jieguo.size)

        df = jieguo
        num = 0
        for x in range(0, len(df.index)):
            for j in range(0, len(df.columns)):
                if df.loc[x, j]:
                    #print(df.loc[x,j])
                    num = num + 1
        sum = (num / jieguo.size)
        if sum > 0.85:
            print('未点亮')
            result = False
        else:
            print('点亮')
            result = True
        print('黑画面占比{sum:.2f}%'.format(sum=sum * 100))

        return result, sum


if __name__ == '__main__':
    pic = Video_get()
    # a = pic.camera_check()
    # pic.camera_show()
    result, black_sum = pic.checkdianliang()
    print(black_sum)
