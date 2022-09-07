# -*- coding:utf-8 -*-
import sys
import time
import pg_cmd
import Find_PG
from MegaGateway import *
import RS232


class Test_power(object):
    def __init__(self, com1="COM26" ,com2="COM21"):
        self.pg = pg_cmd.ServPG()
        self.rs1=RS232.Communication(com1,115200,15)
        self.rs2=RS232.Communication(com2,115200,15)

    def find_pg(self):
        ip = Find_PG.pg_ip()

    def Coarse_tuning(self):
        self.pg.open()
        print('给被校准电源上接上0.0091mA的负载')
        ch = str(input('输入校准电路：'))
        v = float(input('输入电压值：'))
        self.pg.powerVolt(ch,v)
        time.sleep(0.3)
        self.pg.powerRelayON(ch)
        time.sleep(0.3)
        self.pg.powerDCENON(ch)
        time.sleep(0.3)

        adc_bs=input('选择大小电流档位(S/B)')
        self.pg.ADC_CUR_SWITCH(ch,adc_bs)

        adc_d = str(input('输入S6寄存器地址：'))
        print('开始回读ADC码值')
        adc = [0 for x in range(1000)]
        for i in range(1000):
            adc_num = self.pg.read_s6(adc_d)
            adc_num = adc_num.split('H')[1]
            adc[i]= int(adc_num,16)
            time.sleep(0.003)
        adc.sort()
        num = 0
        for x in range(400,800):
            num = adc[x]+num
        adc_small = num/400
        print("adc_small = %f" % adc_small)

        input('给被校准电源上接上1.1485mA的负载')
        print('开始回读ADC码值')
        adc = [0 for x in range(1000)]
        for i in range(1000):
            adc_num = self.pg.read_s6(adc_d)
            adc_num = adc_num.split('H')[1]
            adc[i]= int(adc_num,16)
            time.sleep(0.003)
        adc.sort()
        num = 0
        for x in range(400,800):
            num = adc[x]+num
        adc_big = num/400
        print("adc_big = %f" % adc_big)

        k = 0
        k = (adc_big - adc_small)/(1.1485-0.0091)
        b = adc_big-(k*1.1485)
        print("k=%f,b=%f" % (k,b))

        self.pg.ADCLC_write(ch,k,b)

    
    def Fine_tuning(self):
        self.pg.open()
        input("首先接上屏幕（用BOE Nova标定的屏）")
        mipi = input("选择上电口：1/2")
        input("点亮屏幕")
        pw_on = (0xAA,0x01,0xC3,0x33,0x00,0x00,0x55) #开电
        sle_in = (0xAA,0x01,0xC3,0x44,0x00,0x00,0x55) #进入睡眠模式
        sle_out = (0xAA,0x01,0xC3,0x88,0x00,0x00,0x55) #退出睡眠模式
        if mipi == '1':
            self.rs1.Send_data(pw_on)
            strRet = self.rs1.Read_Line()
            strRet = strRet.split('\r')[0]
            if strRet == 'Display_on':
                print("开电成功，等待一分钟")
                time.sleep(20)
                pass
            else:
                print('开电失败')
                sys.exit()
        elif mipi == "2":
            self.rs2.Send_data(pw_on)
            strRet = self.rs2.Read_Line()
            strRet = strRet.split('\r')[0]
            if strRet == 'Display_on':
                print("开电成功，等待一分钟")
                time.sleep(20)
                pass
            else:
                print('开电失败')
                sys.exit()

        ret = input("请输入(A/B) A:校准工作电流 B:校准睡眠电流")
        ch = input("输入校准电路：")
        if ret == "A":#####A大电流
            self.pg.ADC_CUR_SWITCH(ch,'B')
            i_read=[0 for x in range(1000)]
            for i in range(1000):
                i_data = self.pg.powerQBcurrent(ch)
                i_read[i] = i_data
            k,b = self.pg.ADCHC_read(ch)
        elif ret =='B':#####B小电流
            self.pg.ADC_CUR_SWITCH(ch,'S')

            if mipi == '1':
                self.rs1.Send_data(sle_in)
                time.sleep(2)
                strRet = self.rs1.Read_Line()
                strRet = strRet.split('\r')[0]
            elif mipi == "2":
                self.rs2.Send_data(sle_in)
                time.sleep(2)
                strRet = self.rs1.Read_Line()
                strRet = strRet.split('\r')[0]
            else:
                print('输出错误，退出')
                sys.exit()
            
            i_read=[0 for x in range(1000)]
            for i in range(1000):
                i_data = self.pg.powerQScurrent(ch)
                i_read[i] = i_data
            k,b = self.pg.ADCLC_read(ch)

        i_read.sort()
        num = 0
        for x in range(400,800):
            num = i_read[x]+num
        Itest=(num/400)
        print("Itest = %f"% (Itest*1000))
        print("k=%f,b=%f"%(k,b))

        Ith = float(input("输入理论电流值Ith："))/1000

        pw_dir = input("输入校准方向（左/右）：")
        if pw_dir == "左":
            direction = 1
        elif pw_dir == "右":
            direction = -1
        else:
                print('输出错误，退出')
                sys.exit()
        
        b_c = abs(Ith - Itest)/1000*direction*k

        Cal_B = b + b_c

        print("Cal_B= %f"% Cal_B)

        if ret == "A":#####A大电流，B小电流
            self.pg.ADCHC_write(ch,k,Cal_B)
        elif ret == "B":
            self.pg.ADCLC_write(ch,k,Cal_B)
        else:
                print('输出错误，退出')
                sys.exit()

        self.disp_off()
        
    def disp_off(self):
        pw_off = (0xAA,0x01,0xC3,0x66,0x00,0x00,0x55) #关电
        self.rs1.Send_data(pw_off)
        self.rs2.Send_data(pw_off)
    

if __name__ == "__main__":
    test = Test_power(com1="COM26" ,com2="COM21")
    x = input('选择小档位粗调或细调模式（A/B）')
    if x == "A":
        test.Coarse_tuning()
    elif x == "B":
        test.Fine_tuning()