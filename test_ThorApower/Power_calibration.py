# -*- coding:utf-8 -*-
import pg_cmd
import Find_PG
from MegaGateway import *


class Test_power(object):
    def __init__(self, channl='ELVDD', volt_min=1, volt_max=20, num=1):
        self.pg = pg_cmd.ServPG()
        self.ch = channl
        self.v_min = float(volt_min)
        self.v_max = float(volt_max)
        self.n = float(num)

    def find_pg(self):
        ip = Find_PG.pg_ip()

    def Coarse_tuning(self):
        self.pg.open()
        print('给被校准电源上接上0.0091mA的负载')
        ch = str(input('输入校准电路：'))
        v = float(input('输入电压值：'))
        self.pg.powerVolt(ch,v)
        adc_d = str(input('输入S6寄存器地址：'))
        print('开始回读ADC码值')
        adc = [0 for x in range(1000)]
        for i in range(1000):
            adc_num = self.pg.read_s6(adc_d)
            adc_num = adc_num.split('H')[1]
            adc[i]= int(adc_num,16)
        adc.sort()
        num = 0
        for x in range(400,800):
            num = adc[x]+num
        adc_small = num/400
        print("adc_small = %g" % adc_small)

        input('给被校准电源上接上1.1485mA的负载')
        print('开始回读ADC码值')
        adc = [0 for x in range(1000)]
        for i in range(1000):
            adc_num = self.pg.read_s6(adc_d)
            adc_num = adc_num.split('H')[1]
            adc[i]= int(adc_num,16)
        adc.sort()
        num = 0
        for x in range(400,800):
            num = adc[x]+num
        adc_big = num/400
        print("adc_big = %g" % adc_big)

        k = 0
        k = (adc_big - adc_small)/(1.1485-0.0091)
        b = adc_big-(k*1.1485)
        print("k=%g,b=%g" % (k,b))
        #self.pg.ADCLC_write(ch,k,b)

    
    def Fine_tuning(self):
        self.pg.open()
        input("首先接上屏幕（用BOE Nova标定的屏）")
        input("点亮屏幕")
        


if __name__ == "__main__":
    test = Test_power(1,2,3,4)
    test.Coarse_tuning()