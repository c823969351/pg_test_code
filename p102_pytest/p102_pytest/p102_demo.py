# -*- coding:utf-8 -*-

    ###########################串口通讯自动化脚本####################################################

import time
import sys
import os
import RS232

#################################################
g_pg = None
logfile = None
logfilename = ""

DELAY = 2

#################################################
def print_log(*args):
    strTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print( strTime + ": ", end="")
    print(args)

    global logfile
    global logfilename
    if logfile == None:
        logfilename = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) +".log"
        logfile = open(logfilename, "wt")

    logfile.write( strTime + ": ")
    logfile.write(str(args) + '\n')
    logfile.flush()


################################################################################
def POWER_ON():
    data = (0xAA,0x01,0xC3,0x33,0x00,0x00,0x55) #开电
    g_pg.Send_data(data)
    strRet = g_pg.Read_Line()
    print_log("Recv:", strRet)
    return strRet

def POWER_OFF():
    data = (0xAA,0x01,0xC3,0x66,0x00,0x00,0x55) #关电
    g_pg.Send_data(data)
    strRet = g_pg.Read_Line()
    print_log("Recv:", strRet)
    return strRet

def Sleep_IN():
    data = (0xAA,0x01,0xC3,0x44,0x00,0x00,0x55) #sleep in
    g_pg.Send_data(data)
    
    strRet = g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    print_log("Recv:", strRet)
    return strRet

def Sleep_OUT():
    data = (0xAA,0x01,0xC3,0x88,0x00,0x00,0x55) #sleep out
    g_pg.Send_data(data)
    strRet = g_pg.Read_Line()
    print_log("Recv:", strRet)
    return strRet

def Show_VOLT():
    data = (0xAA,0x01,0xC3,0x55,0x00,0x00,0x55) #volt
    g_pg.Send_data(data)

    strRet = g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    strRet += g_pg.Read_Line()
    print_log("Recv:", strRet)
    return strRet


def SHOW_PATTERN(index):
    data = (0xAA,0x01,0xC3,index,0x00,0x00,0x55) 
    g_pg.Send_data(data)
    strRet = g_pg.Read_Line()
    print_log("Recv:", strRet)
    return strRet

def delay_time(time_s):
    time.sleep(time_s)

################################################################################

def test():  
    pg = g_pg
    #pg.Print_Name()  # 打印设备基本信息

    while True:

        strRet = POWER_ON()
        if strRet[:-2] != "Display_on":
            time.sleep(2)
            strRet = POWER_ON()
            if strRet[:-2] != "Display_on":
                raise Exception("开电失败")

        # strRet = SHOW_PATTERN(0x00) #白
        # delay_time(DELAY)
        # Show_VOLT()

        strRet = SHOW_PATTERN(0x01) #黑
        delay_time(DELAY)

        #strRet = SHOW_PATTERN(0x02) #L4灰阶
        #delay_time(DELAY)

        # strRet = SHOW_PATTERN(0x03) #L8灰阶
        # delay_time(DELAY)

        # strRet = SHOW_PATTERN(0x04) #L12灰阶
        # delay_time(DELAY)

        strRet = SHOW_PATTERN(0x05) #标定图
        delay_time(DELAY)

        Show_VOLT()
        delay_time(DELAY)

        strRet = Sleep_IN()
        delay_time(DELAY)

        strRet = Sleep_OUT()
        delay_time(DELAY)

        strRet = SHOW_PATTERN(0x00) #白
        delay_time(DELAY)

        strRet = SHOW_PATTERN(0x01) #黑
        delay_time(DELAY)

        # strRet = SHOW_PATTERN(0x02) #L4灰阶
        # delay_time(DELAY)

        #strRet = SHOW_PATTERN(0x03) #L8灰阶
        #delay_time(DELAY)

        # strRet = SHOW_PATTERN(0x04) #L12灰阶
        # delay_time(DELAY)

        strRet = SHOW_PATTERN(0x05) #标定图
        delay_time(DELAY)
        
        Show_VOLT()
        delay_time(DELAY)

        strRet = POWER_OFF()
        delay_time(3)




################################################################################        
if __name__ == "__main__":

    argc = len(sys.argv)

    com = "COM26"    
    if argc > 1:
        com = sys.argv[1]

    print_log("COM: " + com)

    g_pg = RS232.Communication(com, 115200, 10)

    tm_begin = time.time()
    print_log(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    try:
        test()
    except Exception as e:
        print_log("---异常---：", e)
        print_log("测试失败")
        print_log(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print_log(time.time() - tm_begin )
        os.system("pause")


################################################################################