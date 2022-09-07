# coding=utf-8
from ipaddress import ip_address
from random import randint
import clr
import socket
import json
import PGtest_log
import time
import collections
import pg_cmd

clr.AddReference('IntellVega.MegaThorProtocolFramework')
from IntellVega.MegaThorProtocolFramework import *

nowtime = time.localtime()
strftime = time.strftime("%Y%m%d",nowtime)
logfile = ('PGtest-'+strftime+'.log')
log = PGtest_log.Logger(logfile,level='info')



class Thordata(object):
    def __init__(self,serv = '127.0.0.1',port = 8089):
        self.MegaThorData = MegaThorData()
        self.host = serv
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        log.logger.info('sock.connect:%s,%s',self.host,self.port)
        pass
    
    def close(self):
        if (self.sock != None):
            self.sock.close()
            log.logger.info('sock.close:%s,%s',self.host,self.port)
        pass
        
    def send(self,data):
        if (self.sock != None):
            self.sock.send(data)
            log.logger.info('send:%s',data)
        pass
    
    def recv(self,size = 4096):
        if (self.sock != None):
            data = self.sock.recv(size)
            log.logger.info('recv:%s',data)
            return data
        pass
    
    #判断动作是否成功
    def JudgeAction(self, data):
        if data['ErrorCode'] != 0:
            #log.logger.error('%s',data['EfforMessage'])
            return data
        else:
            #log.logger.info('%s',data['EfforMessage'])
            return data


    #解析响应字节
    def parse_response(self,data):
        response = bytearray(data)
        response = MegaThorData(self.MegaThorData.HandlePrefixAndSuffix(response))
        response = bytearray(response.Message).decode('utf-8')
        response = json.loads(response)
        #print(response)
        #response = list(response)
        #response = MegaThorAck(response)
        '''print (response.Result)
        print (response.ErrorCode)
        print (response.EfforMessage)
        print (response.Content)
        print (response.PgId)'''
        return self.JudgeAction(response[0])

    #获取测试文件列表
    def ReadTestFilelist(self, id = 1):
        log.logger.info('获取测试文件列表') 
        self.send(bytearray(self.MegaThorData.GetReadTestFileListCmd(id)))
        data = bytearray(self.recv())
        return self.parse_response(data)
    
    #获取测试文件列表信息
    def ReadTestFilelistInfo(self, id = 1, flie_name = str()):
        log.logger.info('获取测试文件列表信息') 
        self.send(bytearray(self.MegaThorData.GetCurrentTestFilePanelList(id,flie_name)))
        data = bytearray(self.recv())
        return self.parse_response(data)

    #选择测试文件
    def SelectTestFile(self, id = 1, flie_name = str(), ClientId = 1):
        log.logger.info('选择测试文件') 
        self.send(bytearray(self.MegaThorData.GetSetTestFileCmd(id, flie_name, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)
    
    #开电
    def PowerOn(self, id = 1 , state = True, ClientId = 1):
        if state:
            log.logger.info('开电') 
        else:
            log.logger.info('关电')
        self.send(bytearray(self.MegaThorData.GetSwitchPowerCmd(id, state, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)

    #关电
    def PowerOff(self, id = 1 , state = False, ClientId = 1):
        log.logger.info('关电') 
        self.send(bytearray(self.MegaThorData.GetSwitchPowerCmd(id, state, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)
    
    #上切图
    def SwitchUp(self, id = 1 , cutFlag = 0, ClientId = 1):
        log.logger.info('上切图') 
        self.send(bytearray(self.MegaThorData.GetScpiCutPictureCmd(id, cutFlag, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)
    
    #下切图
    def SwitchDown(self, id = 1 , cutFlag = 1, ClientId = 1):
        log.logger.info('下切图') 
        self.send(bytearray(self.MegaThorData.GetScpiCutPictureCmd(id, cutFlag, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)
    
    #ID切图
    def SwitchID(self, id = 1 , patten_id = 1, ClientId = 1): #切图ID从1开始
        log.logger.info('ID切图') 
        self.send(bytearray(self.MegaThorData.GetScpiCutPictureByIdCmd(id, patten_id, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)

    #RGB画图
    def DrawRGB(self, id = 1 , r = 0, g = 0, b = 0, ClientId = 1):
        log.logger.info('RGB画图 R,G,B:{}'.format((r,g,b)))
        self.send(bytearray(self.MegaThorData.GetDisplayRgbCmd(id, r, g, b, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)
    
    #关闭RGB画图
    def CloseRGB(self, id = 1 , ClientId = 1):
        log.logger.info('关闭RGB画图') 
        self.send(bytearray(self.MegaThorData.GetClearRgbCmd(id, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)


    #十字光标
    def CrossCursor(self, id = 1 , crossmark =  CrossMark(True,  0,  0,  0,  0,  0), ClientId = 1):
        log.logger.info('十字光标') 
        self.send(bytearray(self.MegaThorData.GetSetCrossMarkCmd(id, crossmark, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)

    #显示字符串
    def DisplayString(self, id = 1 , displayString = DisplayString( 0, 0,  '你好镁伽2022!',  100, 0, 0, 0), ClientId = 1):
        log.logger.info('显示字符串') 
        self.send(bytearray(self.MegaThorData.GetOverlayStringCmd(id, displayString, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)
    
    #获取屏幕亮度
    def GetScreenBrightness(self, id = 1 , ClientId = 1):
        log.logger.info('获取屏幕亮度') 
        self.send(bytearray(self.MegaThorData.GetLvxy(id, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)

    #读取FMA值
    def ReadFMA(self, id = 1 , ClientId = 1):
        log.logger.info('读取FMA值') 
        self.send(bytearray(self.MegaThorData.GetFMA(id, ClientId)))
        data = bytearray(self.recv())
        return self.parse_response(data)
#############################测试用例流程##############################################

#客户要求的获取测试文件列表，获取测试文件信息，选择测试文件
def liucheng_1(identifier,ClientId):
    TestFilelist = MagaThor.ReadTestFilelist(identifier)['Content']['$values']
    TestFilelist
    MagaThor.ReadTestFilelistInfo(identifier,TestFilelist[1])
    MagaThor.SelectTestFile(identifier,TestFilelist[1],ClientId)
    #time.sleep(20)

#开关RGB测试
def liucheng_2(identifier,ClientId):
    MagaThor.PowerOn(identifier,True,ClientId)
    MagaThor.DrawRGB(identifier,255,0,0,ClientId)
    time.sleep(1)
    MagaThor.PowerOff(identifier,False,ClientId)
    time.sleep(1)
    MagaThor.PowerOn(identifier,True,ClientId)
    if pg.LPG_Q() != 'OFF\n':
        log.logger.error('error:%s','未关闭逻辑图')
    else:
        log.logger.info('%s','已关闭逻辑图')
    MagaThor.PowerOff(identifier,False,ClientId)

#十字光标延时测试
def liucheng_3(identifier,ClientId):
    for x,y in zip(range(0,3840,50),range(0,2160,20)):
        MagaThor.CrossCursor(identifier,CrossMark(True,x,y,0,0,0),ClientId)
        time.sleep(0.2)

#亮度值测试
def liucheng_4(identifier,ClientId):
    delay = 0.16
    for i in range(10):
        #MagaThor.DrawRGB(identifier,31,31,31,ClientId)
        pg.send('DISPLAY:LPG:MODE ON,OFF')
        pg.send('DISPLAY:LPG:INDEX 2,OFF')
        pg.LPG_RGB('#H7F007F007F')
        time.sleep(delay)
        data = MagaThor.GetScreenBrightness(identifier,ClientId)['Content']['Lv']
        log.logger.info('灰阶：{}，亮度 {}'.format(31,data))

        if data >3:
            raise Exception('error:%s','亮度值读取错误')

        #MagaThor.DrawRGB(identifier,255,255,255,ClientId)
        pg.send('DISPLAY:LPG:MODE ON,OFF')
        pg.send('DISPLAY:LPG:INDEX 2,OFF')
        pg.LPG_RGB('#H3FF03FF03FF')
        time.sleep(delay)
        data = MagaThor.GetScreenBrightness(identifier,ClientId)['Content']['Lv']
        log.logger.info('灰阶：{}，亮度 {}'.format(255,data))

        if data <170:
            log.logger.error('error:%s','亮度值读取错误')

def test():
    delay = 0.15
    if pg.query('DISPLAY:LPG:INDEX?') == '2\n':
        pg.LPG_RGB('#H7F007F007F')
        time.sleep(delay)
        data = MagaThor.GetScreenBrightness(identifier,ClientId)['Content']['Lv']
        log.logger.info('灰阶：{}，亮度 {}'.format(31,data))

        if data >3:
            log.logger.error('error:%s','亮度值读取错误')
            #raise Exception('error:%s','亮度值读取错误')

        pg.LPG_RGB('#H3FF03FF03FF')
        time.sleep(delay)
        data = MagaThor.GetScreenBrightness(identifier,ClientId)['Content']['Lv']
        log.logger.info('灰阶：{}，亮度 {}'.format(255,data))

        if data <170:
            log.logger.error('error:%s','亮度值读取错误')

    else:
        pg.send('DISPLAY:LPG:INDEX 2,OFF')
        pg.LPG_RGB('#H7F007F007F')
        time.sleep(delay)
        data = MagaThor.GetScreenBrightness(identifier,ClientId)['Content']['Lv']
        log.logger.info('灰阶：{}，亮度 {}'.format(31,data))

        if data >3:
            log.logger.error('error:%s','亮度值读取错误')

        pg.LPG_RGB('#H3FF03FF03FF')
        time.sleep(delay)
        data = MagaThor.GetScreenBrightness(identifier,ClientId)['Content']['Lv']
        log.logger.info('灰阶：{}，亮度 {}'.format(255,data))

        if data <170:
            log.logger.error('error:%s','亮度值读取错误')

def liucheng_4_test(identifier,ClientId):
    for i in range(100):
        if pg.query('DISPLAY:LPG:MODE?') == 'ON\n':
            test()
        else:
            pg.send('DISPLAY:LPG:MODE ON,OFF')
            test()
    pg.LPG_RGB('#H0')
    pg.send('DISPLAY:LPG:MODE OFF,OFF')
    pg.send('DISPLAY:LPG:INDEX 3,OFF')

def liucheng_5(identifier,ClientId):
    for i in range(255):
        MagaThor.DrawRGB(identifier,i,i,i,ClientId)
        time.sleep(0.20)
###############################################复现画异问题测试用例###############################################
def test_huayi_1(identifier,ClientId):
    pg.send('CONFIG:TEST:SELECT "M280.pgz"')
    while pg.TEST_LOADING() != 'DONE':
        print('正在加载文件')
        time.sleep(0.5)
        pass
    time.sleep(1)

    Result = MagaThor.PowerOn(identifier,True,ClientId)["Result"]
    if Result:
        log.logger.info('%s','开电源成功')
    else:
        log.logger.error('error:%s','开电源失败')
    
    Result = MagaThor.PowerOn(identifier,False,ClientId)["Result"]
    if Result:
        log.logger.info('%s','关电源成功')
    else:
        log.logger.error('error:%s','关电源失败')

def test_huayi_2(identifier,ClientId):
    pg.send('CONFIG:TEST:SELECT "M280.pgz"')
    while pg.TEST_LOADING() != 'DONE':
        print('正在加载文件')
        time.sleep(0.5)
        pass
    time.sleep(1)

    Result = MagaThor.PowerOn(identifier,True,ClientId)["Result"]
    if Result:
        log.logger.info('%s','开电源成功')
    else:
        log.logger.error('error:%s','开电源失败')
    
    for i in range(5):
        partten_id = randint(1,10)
        MagaThor.SwitchID(identifier,partten_id,ClientId)
        time.sleep(0.2)
    
    Result = MagaThor.PowerOn(identifier,False,ClientId)["Result"]
    if Result:
        log.logger.info('%s','关电源成功')
    else:
        log.logger.error('error:%s','关电源失败')

def test_huayi_3(identifier,ClientId):
    Result = MagaThor.PowerOn(identifier,True,ClientId)["Result"]
    if Result:
        log.logger.info('%s','开电源成功')
    else:
        log.logger.error('error:%s','开电源失败')
    
    for i in range(5):
        partten_id = randint(1,10)
        MagaThor.SwitchID(identifier,partten_id,ClientId)
        time.sleep(0.2)
    
    Result = MagaThor.PowerOn(identifier,False,ClientId)["Result"]
    if Result:
        log.logger.info('%s','关电源成功')
    else:
        log.logger.error('error:%s','关电源失败')
    
def test_huayi_4(identifier,ClientId):
    for i in range(5):
        pg.send('CONFIG:TEST:SELECT "M280.pgz"')
        while pg.TEST_LOADING() != 'DONE':
            print('正在加载文件')
            time.sleep(0.5)
            pass
        time.sleep(1)

    Result = MagaThor.PowerOn(identifier,True,ClientId)["Result"]
    if Result:
        log.logger.info('%s','开电源成功')
    else:
        log.logger.error('error:%s','开电源失败')
    
    Result = MagaThor.PowerOn(identifier,False,ClientId)["Result"]
    if Result:
        log.logger.info('%s','关电源成功')
    else:
        log.logger.error('error:%s','关电源失败')

def test_huayi_5(identifier,ClientId):
    for i in range(10):
        Result = MagaThor.PowerOn(identifier,True,ClientId)["Result"]
        if Result:
            log.logger.info('%s','开电源成功')
        else:
            log.logger.error('error:%s','开电源失败')
        
        Result = MagaThor.PowerOn(identifier,False,ClientId)["Result"]
        if Result:
            log.logger.info('%s','关电源成功')
        else:
            log.logger.error('error:%s','关电源失败')

def test_huayi_6(identifier,ClientId):
    for i in range(10):
        Result = MagaThor.PowerOn(identifier,True,ClientId)["Result"]
        if Result:
            log.logger.info('%s','开电源成功')
        else:
            log.logger.error('error:%s','开电源失败')
        
        partten_id = randint(1,10)
        MagaThor.SwitchID(identifier,partten_id,ClientId)
        time.sleep(0.5)
        
        
        Result = MagaThor.PowerOn(identifier,False,ClientId)["Result"]
        if Result:
            log.logger.info('%s','关电源成功')
        else:
            log.logger.error('error:%s','关电源失败')


def test_offset(identifier,ClientId):
    # Result = MagaThor.PowerOn(identifier,True,ClientId)["Result"]
    # if Result:
    #     log.logger.info('%s','开电源成功')
    # else:
    #     log.logger.error('error:%s','开电源失败')
    # time.sleep(0.5)
    
    # for partten_id in range(10):
    #     MagaThor.SwitchID(identifier,partten_id,ClientId)
    #     time.sleep(0.3)

    # for i in range(0,255,1):
    #     MagaThor.DrawRGB(identifier,i,i,i,ClientId)
    #     time.sleep(0.2)
    for i in range(150,180,1):
        MagaThor.DrawRGB(identifier,i,i,i,ClientId)
        time.sleep(0.2)
    
    MagaThor.CloseRGB(identifier,ClientId)
    time.sleep(1)
    
    # MagaThor.SwitchID(identifier,1,ClientId)
    # time.sleep(1)
    
    # for partten_id in range(10):
    #     MagaThor.SwitchID(identifier,partten_id,ClientId)
    #     time.sleep(0.3)
    
    # Result = MagaThor.PowerOff(identifier,False,ClientId)["Result"]
    # if Result:
    #     log.logger.info('%s','关电源成功')
    # else:
    #     log.logger.error('error:%s','关电源失败')
    # time.sleep(0.5)
    







if __name__ == '__main__':
    #通讯参数
    identifier = 1
    #PG编号
    ClientId = 1
    #测试次数
    times = 5000
    #PG服务对象
    pg = pg_cmd.ServPg(serv='10.10.10.101')
    pg.open()
    #上位机第三方对象
    MagaThor = Thordata()
    MagaThor.connect()
    for i in range(1,times+1):
        print('第%d次'%i)
    #while True:
        try:
            #MagaThor.CrossCursor(identifier,CrossMark(True,  500,  500,  255,  0,  0),ClientId)
            #liucheng_3(identifier,ClientId)
            #liucheng_2(identifier,ClientId)
            #liucheng_4(identifier,ClientId)
            #liucheng_4_test(identifier,ClientId)
            #print(MagaThor.GetScreenBrightness(identifier,ClientId)['Content']['Lv'])
            #print(MagaThor.ReadFMA(identifier,ClientId)['Content'])
            #liucheng_3(identifier,ClientId)

            # if i % 6 == 0:
            #     test_huayi_1(identifier,ClientId)
            # elif i % 6 == 1:
            #     test_huayi_2(identifier,ClientId)
            # elif i % 6 == 2:
            #     test_huayi_3(identifier,ClientId)
            # elif i % 6 == 3:
            #     test_huayi_4(identifier,ClientId)
            # elif i % 6 == 4:
            #     test_huayi_5(identifier,ClientId)
            # else:
            #     test_huayi_6(identifier,ClientId)

            test_offset(identifier,ClientId)
        except Exception as e:
            print(e)
            log.logger.error('error:%s',e)
            break
    MagaThor.close()
    pg.close()