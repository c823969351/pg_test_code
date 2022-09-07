# -*- coding:utf-8 -*-

    ###########################串口通讯自动化脚本####################################################

import time
import sys
import os
import RS232



g_pg = RS232.Communication("COM28", 115200, 10)

################################################################################
def POWER_ON():
    data = (0xAA,0x01,0xC3,0x33,0x00,0x00,0x55) #开电
    g_pg.Send_data(data)
    strRet = g_pg.Read_Line()
    return strRet

def POWER_OFF():
    data = (0xAA,0x01,0xC3,0x66,0x00,0x00,0x55) #关电
    g_pg.Send_data(data)
    strRet = g_pg.Read_Line()
    return strRet

################################################################################        
if __name__ == "__main__":
    tm_begin = time.time()
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    try:
        POWER_ON()
        time.sleep(5)
    except Exception as e:
        print("---异常---：", e)
        print("测试失败")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print(time.time() - tm_begin )


################################################################################