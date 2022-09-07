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

DELAY = 1

csv_file = None

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

    global csv_file
    if csv_file == None:
        csv_file = open(logfilename + ".csv", "wt")

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
    elvdd_info = g_pg.Read_Line()
    strRet += elvdd_info
    strRet += g_pg.Read_Line()
    print_log("Recv:", strRet)

    csv_file.write(elvdd_info.replace("\r\n", "\n").replace(" ", ", ")  )
    csv_file.flush()

    return strRet

def Sleep_OUT():
    data = (0xAA,0x01,0xC3,0x88,0x00,0x00,0x55) #sleep out
    g_pg.Send_data(data)
    strRet = g_pg.Read_Line()
    print_log("Recv:", strRet)

    csv_file.write(strRet.replace("\r\n", "\n"))
    csv_file.flush()

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

        # delay_time(DELAY)
        Sleep_IN() 

        delay_time(DELAY)
        strRet = POWER_OFF()
        delay_time(2)




################################################################################        
if __name__ == "__main__":

    argc = len(sys.argv)

    com = "COM17"    
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