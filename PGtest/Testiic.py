# -*- coding: UTF-8 -*-
from socket import *

import pg_cmd
import time

busId = 1
slaAttr = (0x76, 7)
readlen = 10
data_b = (0x00,0x01,0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09)
data_a = (0x00,0x3e)
data_check = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t'

def print_hex(bytes):
    l = [hex(int(i)) for i in bytes]
    print(" ".join(l))

def Read_EDID(data):
    pg.iicSend(busId,slaAttr,data_a + data)
    msg_r = pg.iicQuery(busId, slaAttr, readlen,data_a)
    print_hex(msg_r)
    return  msg_r

if __name__ == "__main__":
    tm_begin = time.time()
    ip = "192.168.1.103"
    times = 500
    error_times = 0
    try:
        pg = pg_cmd.ServPg(ip)
        pg.open()
        for i in range(times):
            if (i % 2) == 0:
                msg_r = Read_EDID(data_b)

                if msg_r != data_check:
                    error_times += 1
                    print("iic error:",error_times)
                
                time.sleep(1)
            else:
                msg_r = Read_EDID(data_b[::-1])
                
                if msg_r != data_check[::-1]:
                    error_times += 1
                    print("iic error:",error_times)
                    
                time.sleep(1)
            
            print('测试次数：%s'%(i+1))

        print('测试完成')
        print('失败次数：',error_times)
    except Exception as e:
        print("---异常---：", e)
        print("测试失败")
    print("测试时间")
    print(time.time() - tm_begin)
    pg.close