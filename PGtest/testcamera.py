from sys import argv,exit
import time
import cv2

class Ui_MainWindow(object):
    def __init__(self):

        self.cap = cv2.VideoCapture() # 准备获取图像
        self.CAM_NUM = 0



    def camera_check(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
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
            flag, self.image = self.cap.read()
            self.image=cv2.flip(self.image, 1) # 左右翻转  
            show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB) 
            gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
            self.takePhoto()
            cv2.imshow("win1",cv2.resize(self.image,(640,480)))
            cv2.imshow("win2",cv2.resize(show,(640,480)))
            cv2.imshow("win3",cv2.resize(gray,(640,480)))
            cv2.waitKey(5)
            if cv2.waitKey(5) & 0xFF==ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()      
    
    def takePhoto(self):
        now_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        print(now_time)
        cv2.imwrite('pic_'+str(now_time)+'.bmp',self.image)

        '''cv2.putText(self.image, 'The picture have saved !',
                    (int(self.image.shape[1]/2-130), int(self.image.shape[0]/2)),
                    cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
                    1.0, (255, 0, 0), 1)'''

if __name__ == '__main__':
    cam = Ui_MainWindow()
    print(ord('q'))
    cam.camera_check()
    cam.camera_show()