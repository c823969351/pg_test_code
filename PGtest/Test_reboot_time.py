# -*- coding:utf-8 -*-
from socket import *
import pg_cmd
import time
from Find_PG import *
### 删除list指定值的所有元素

def reboot_test(ip):
    udpip = list()
    pg.reboot()  ##重启
    time.sleep(3)
    while 1:
        if udpip == ip:
            break
        else:
            udpip = mrgFindGateWay()
            udpip = " ".join(udpip)
            print("重启中")



if __name__ == "__main__":

    tm_begin = time.time()
    ip = "10.10.10.10"
    try:
        pg = pg_cmd.ServPg(ip)
        pg.open()
        IDN = pg.idn()
        print(IDN)
        #pg.powerOn("ALL",True) ##True = ON
        #time.sleep(5)
        #pg.powerOn("ALL",False) ##False = OFF
        reboot_test(ip)
    except Exception as e:
        print("---异常---：", e)
        print("测试失败")
    print("测试时间")
    print(time.time() - tm_begin)
    pg.close