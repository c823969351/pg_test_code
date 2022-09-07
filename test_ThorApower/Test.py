# -*- coding:utf-8 -*-

import numpy as np
import time
import write_excel
import pg_cmd
import Find_PG
from MegaGateway import *


def find_pg():
    ip = Find_PG.pg_ip()
    return ip

class Test_power(object):
    def __init__(self, channl='ELVDD', volt_min=1, volt_max=20, num=1 ,filename=r'D:\testCode\test_ThorApower\电源测试数据\电源测试.csv'):
        self.pg = pg_cmd.ServPG(serv=find_pg())
        self.ch = channl
        self.v_min = float(volt_min)
        self.v_max = float(volt_max)
        self.n = float(num)
        self.filename = filename
    
    def power_on(self,i):
        '''self.pg.powerRelayON(self.ch)
        time.sleep(0.2)
        self.pg.powerVolt(self.ch, i)
        time.sleep(0.5)
        self.pg.powerDCENON(self.ch)
        time.sleep(0.2)'''
        #开电
        self.pg.powerOn(self.ch)
        time.sleep(0.2)
        self.pg.powerVolt(self.ch, i)
        time.sleep(0.5)
    
    def power_off(self):
        '''self.pg.powerDCENOff(self.ch)
        time.sleep(0.2)
        self.pg.powerRelayOff(self.ch)
        time.sleep(0.2)
        self.pg.powerVolt(self.ch, self.v_min)
        time.sleep(0.2)'''
        #关电
        self.pg.powerOff(self.ch)
        time.sleep(0.2)
        self.pg.powerVolt(self.ch, self.v_min)
        time.sleep(0.2)

    def test_volt_1(self):  #步进与电压符号相同
        self.pg.open()
        for i in np.arange(self.v_min, self.v_max + self.n, self.n):
            i = float('%g'%i) ###小数整形
            if i == self.v_min:
                self.power_on(i)
            ##################打印电压值###################################
            else:
                self.pg.powerVolt(self.ch, i)
            time.sleep(1)
            strRet_v = self.pg.powerQvolt(self.ch)
            print("PowerVolt: ", strRet_v)
            write_excel.excel_writevolt(self.ch, strRet_v, i, self.v_min, self.filename)
            ret = abs(((i / self.v_max) * 100))
            yield ret
        self.power_off()

    def test_volt_2(self):  #步进与电压符号相反
        self.pg.open()
        for i in np.arange(self.v_max, self.v_min + self.n, self.n):
            i = float('%g'%i)###小数整形
            if i == self.v_max:
                self.power_on()
            ##################打印电压值###################################
            else:
                self.pg.powerVolt(self.ch, i)
            time.sleep(0.5)
            strRet_v = self.pg.powerQvolt(self.ch)
            print("PowerVolt: ", strRet_v)
            write_excel.excel_writevolt(self.ch, strRet_v, i, self.v_max, self.filename)
            ret = abs(((i / self.v_min) * 100))
            yield ret
        self.power_off()

    def main(self):
        if (self.v_min * self.n >= 0):
            ret = self.test_volt_1()
            for i in ret:
                yield i
        else:
            ret = self.test_volt_2()
            for i in ret:
                yield i


if __name__ == "__main__":
    print('Hello mega')
    ch = input('输入电路：')
    min_v = int(input('输入开始电压：'))
    max_v = int(input('输入结束电压：'))
    n = float(input('输入步进：'))
    test = Test_power(ch, min_v, max_v, n)
    num = test.main()
    for i in num:
        print(i)