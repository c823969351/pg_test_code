#__author__ = 'cjw'
#coding=utf-8
import visa

class RigolTest(object):

    def __init__(self,usb='USB0::0x2A8D::0x0101::MY60009631::INSTR'):
        self.usb = usb
        try:
            # 打开电流表，得到电流表对象
            self.rm = visa.ResourceManager()#电流表参数
            # 判断是否打开成功
            self.rigol = self.rm.open_resource(self.usb)

        except Exception as e:
            print("---异常---：%s", e)
            
    def open(self):
        self.rigol.write("*IDN?")#查询ID
        return self.rigol.read()

    def as_num(self,x):
        y = '{:.16f}'.format(x)
        return y
    
    
    def Qcurr(self):
        self.rigol.write(":MEASure:CURRent:DC?")#查询直流电流单位A
        return self.as_num(float(self.rigol.read()))
    
    def Qvolt(self):
        self.rigol.write(":MEASure:VOLTage:DC?")#查询直流电压单位V
        return self.as_num(float(self.rigol.read()))

if __name__ == '__main__' :

    rigol = RigolTest()
    print(rigol.open())
    print(rigol.Qcurr())
    print(rigol.Qvolt())


    '''import visa;
    rm = visa.ResourceManager()
    #reslist = rm.list_resources();
    #inst = rm.open_resource('USB0::0x1AB1::0x0C94::DM3O140400007::INSTR')#RIGOL
    inst = rm.open_resource('USB0::0x2A8D::0x0101::MY60009631::INSTR')
    inst.write("*IDN?")
    print(inst.read())
    #inst.write(":SOURce:FREQuency 1GHz");#设置频率
    #inst.write(":SOURce:LEVel -10dBm");#设置幅度
    #inst.write(":OUTPut:STATe ON");#打开RF开关
    inst.write(":MEASure:CURRent:DC?")#查询直流电流单位A
    #inst.write(":MEASure:VOLTage:DC?")#查询直流电压单位V
    #inst.write(":MEASure:FRESistance?")#
    ret = inst.read()
    ret = as_num(float(ret))
    print(ret)
    #print(float(ret))
    rm.close()'''
    

