# -*- coding:utf-8 -*-

import sys
import os
pwd = os.path.abspath(os.path.dirname(__file__))
sys.path.append( pwd + "/../../lib/python")
from MegaGateway import *

if __name__ == "__main__":
###############################################################################
###############################################################################
    ### 查找设备
    deviceList = mrgFindGateWay()
    deviceCount = len(deviceList)
    if deviceCount == 0:
        print("Device Not Found!")
        sys.exit(-1)
    
    ### 选择设备
    if deviceCount == 1:
        device_index = '0'
    else:
        for index in range(deviceCount):
            dev = deviceList[index]
            visa =  mrgOpenGateWay(dev, 800)
            print( "%02d: DEVICE:[%s],\tIDN:[%s]" % (index, dev, mrgGateWayIDNQuery(visa) ) )
            ret =  mrgCloseGateWay(visa)

        device_index = input("please select DEVICE:")
        if device_index == "" or int(device_index) < 0 or int(device_index) >= deviceCount:
            print("input error")
            sys.exit(0)

    ### 打开设备
    thorPG = deviceList[int(device_index)]
    visa =  mrgOpenGateWay(thorPG, 800)
    IDN = mrgGateWayIDNQuery(visa)
    print("ThorPG Open[%s]: %s" % (visa, IDN))

###############################################################################
    print("########### 开始测试 ###########")

    cmd = "POWEr:OUTPUT? ALL"
    strRet = mrdQuery(visa, cmd)
    print("PowerOutput: ", strRet)


    cmd = "POWEr:VOLT? ALL"
    strRet = mrdQuery(visa, cmd)
    print("PowerVolt: ", strRet)


    cmd = "POWEr:VOLT VDD1,3"
    mrdSend(visa, cmd)

    time.sleep(1)

    cmd = "POWEr:VOLT? VDD1"
    strRet = mrdQuery(visa, cmd)
    print("Power VDD1: ", strRet)




    print("########### 测试结束 ###########")
###############################################################################
    ret =  mrgCloseGateWay(visa)
    print("device close:", visa, ret)
################################################################################