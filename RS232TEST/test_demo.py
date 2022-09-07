# -*- coding:utf-8 -*-

    ###########################串口通讯自动化脚本####################################################

import time
import sys
import os
import RS232

g_pg = RS232.Communication("COM13", 115200, 0.5)

class test_m695():
    def __init__(self,num):
        num = 0x01
        

    def POWER_ON(self):
        data = (0xAA,0x01,0xC3,0x33,0x00,0x00,0x55) #开电
        g_pg.Send_data(data)

    def POWER_OFF(self):
        data = (0xAA,0x01,0xC3,0x66,0x00,0x00,0x55) #关电
        g_pg.Send_data(data)

    def Sleep_IN(self):
        data = (0xAA,0x01,0xC3,0x44,0x00,0x00,0x55) #sleep in
        g_pg.Send_data(data)

    def Sleep_OUT(self):
        data = (0xAA,0x01,0xC3,0x88,0x00,0x00,0x55) #sleep out
        g_pg.Send_data(data)

    def Show_VOLT(self):
        data = (0xAA,0x01,0xC3,0x55,0x00,0x00,0x55) #volt
        g_pg.Send_data(data)
        g_pg.Recive_data(1)

def test():  
    pg = g_pg

    pg.Print_Name()  # 打印设备基本信息
    ####pg.Open_Engine()  #打开串口


    while True:
        

        time.sleep(1)
        POWER_ON()
        pg.Recive_data(1)
        Show_VOLT()

        data = (0xAA,0x01,0xC3,0x00,0x00,0x00,0x55) #白画面
        pg.Send_data(data)
        pg.Recive_data(1) #接受数据
        time.sleep(1)
        Show_VOLT()
        time.sleep(2)

        data = (0xAA,0x01,0xC3,0x01,0x00,0x00,0x55) #黑画面
        pg.Send_data(data)
        pg.Recive_data(1) #接受数据
        time.sleep(1)
        Show_VOLT()
        time.sleep(2)

        data = (0xAA,0x01,0xC3,0x02,0x00,0x00,0x55) #L4灰阶
        pg.Send_data(data)
        pg.Recive_data(1) #接受数据
        time.sleep(1)
        Show_VOLT()
        time.sleep(2)

        data = (0xAA,0x01,0xC3,0x03,0x00,0x00,0x55) #L8灰阶
        pg.Send_data(data)
        pg.Recive_data(1) #接受数据
        time.sleep(1)
        Show_VOLT()
        time.sleep(2)

        data = (0xAA,0x01,0xC3,0x04,0x00,0x00,0x55) #L12灰阶
        pg.Send_data(data)
        pg.Recive_data(1) #接受数据
        time.sleep(1)
        Show_VOLT()
        time.sleep(2)


        Sleep_IN()
        pg.Recive_data(1)
        time.sleep(2)
        Show_VOLT()
        time.sleep(2)

        data = (0xAA,0x01,0xC3,0x05,0x00,0x00,0x55) #标定图
        pg.Send_data(data)
        pg.Recive_data(1) #接受数据
        time.sleep(1)
        Show_VOLT()
        time.sleep(2)

        Sleep_OUT()
        pg.Recive_data(1)
        time.sleep(2)
        Show_VOLT()

        time.sleep(3)
        
        POWER_OFF()
        pg.Recive_data(1) #接受数据
        Show_VOLT()
        time.sleep(3)

        
        

if __name__ == "__main__":
    tm_begin = time.time()

    try:
        test()
    except Exception as e:
        print("---异常---：", e)
        print("测试失败")
        print(time.time() - tm_begin )
    ###############################################################################
################################################################################