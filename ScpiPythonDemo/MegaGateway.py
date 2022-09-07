# -*- coding:utf-8 -*-

import os, sys, platform
import time
from types import *
import threading
import socket

##############################################################################
from ctypes import cdll,c_int,c_uint,c_float,c_double,c_long,c_char
from ctypes import create_string_buffer,byref,c_char_p

### 将C语言的char*字符串转化为标准的python字符串
def cbuf_to_string(cbuf):
    return bytes.decode(cbuf.value)

### python的字符串转化为C语言的char *格式
def string_to_charp(s):
    return c_char_p(s.encode())

### 删除list指定值的所有元素
def list_remove_all(lst, ele):
    for i in range(len(lst)-1,-1,-1):
        if lst[i] == ele:
            lst.remove(ele)
    return lst

##############################################################################
_dll = ""
def MageGatewayInit():
    global _dll
    pwd = os.path.abspath(os.path.dirname(__file__))
    _platform = platform.system()

    if _platform == "Windows" :
        os.chdir(pwd)
        print("LoadLibrary", pwd + '\\MegaGateway.dll')
        _dll = cdll.LoadLibrary(pwd + '\\MegaGateway.dll')
    else:
        info = os.popen('file /bin/ls').readlines()[0]
        cpuarch = info.split(",")[1]
        if 'x86' in cpuarch:
            _dll = cdll.LoadLibrary(pwd + "/libMegaGateway.so")
            print("LoadLibrary", pwd + "libMegaGateway.so")
        else:
            _dll = cdll.LoadLibrary(pwd + "/libMegaGateway.so")
            print("LoadLibrary", pwd + "libMegaGateway.so")

##############################################################################
def mrgFindGateWay():
    '''
    int mrgFindGateWay(int mode, char *output, int len);
    + 函数&说明 mrgFindGateWay
        查找网关
    + 参数 mode
        通讯模式
        BUS_SOCKET
    + 参数 output
        查找到的设备描述符,以逗号分隔
    + 参数 len
        提供的空间容量
    + 返回值
        查找到的设备数量,零或负数表示失败
    '''
    if( isinstance(_dll, str) ): 
        ## 未加载库
        MageGatewayInit()

    buf = create_string_buffer(1024)
    _dll.mrgFindGateWay(0, buf, 1024)
    if cbuf_to_string(buf) == '':
        return list()
    else:
        return list(filter(None, cbuf_to_string(buf).split(',') ))


def mrgOpenGateWay(char_p_desc,int_timeout_ms):
    '''
    int mrgOpenGateWay(int mode, char * desc, int timeout_ms);
    + 函数&说明 mrgOpenGateWay
        打开网关
    + 参数 desc
        设备描述符
    + 参数 timeout_ms
        设备通讯时的超时时间
    + 返回值
        成功返回网关句柄,零或负数表示失败
    '''
    return _dll.mrgOpenGateWay(string_to_charp(char_p_desc),int_timeout_ms)


def mrgCloseGateWay(ViSession_vi):
    '''
    int mrgCloseGateWay(ViSession  vi);
    + 函数&说明 mrgCloseGateWay
        关闭网关
    + 参数 vi
        网关句柄
    + 返回值
        0表示执行成功,否则失败
    '''
    return _dll.mrgCloseGateWay(ViSession_vi)


def mrgGateWaySendCmd(ViSession_vi,charp_cmd):
    '''
    int mrgGateWaySendCmd(ViSession  vi, char* cmd, int len);
    + 函数&说明 mrgGateWaySendCmd
        发送命令给网关
    + 参数 vi
        网关句柄
    + 参数 cmd
        SCPI指令信息
    + 参数 len
        指令长度
    + 返回值
        >0表示成功发送的字节数,否则失败
    '''
    return _dll.mrgGateWaySendCmd(ViSession_vi,string_to_charp(charp_cmd),len(charp_cmd))


def mrgGateWayRead(ViSession_vi,int_wantlen):
    '''
    int mrgGateWayRead(ViSession  vi, char * output, int wantlen);
    + 函数&说明 mrgGateWayRead
        网关从接收数据
    + 参数 vi
        网关句柄
    + 参数 output
        接收数据的存放地址
    + 参数 wantlen
        接收数据长度
    + 返回值
        >0表示成功接收的字节数,否则失败
    '''
    buf = create_string_buffer(int_wantlen)
    ret = _dll.mrgGateWayRead(ViSession_vi,buf,int_wantlen)
    if ret < 0:
        return ""
    else:
        return cbuf_to_string(buf)


def mrgGateWayQuery(ViSession_vi,charp_cmd,int_wantlen):
    '''
    int mrgGateWayQuery(ViSession  vi, char* cmd, char *output, int wantlen);
    + 函数&说明 mrgGateWayQuery
        发送查询命令并获取查询结果
    + 参数 vi
        网关句柄
    + 参数 cmd
        要发送的设置命令
    + 参数 output
        接收数据的存放地址
    + 参数 wantlen
        接收数据长度
    + 返回值
        >0表示成功接收的字节数,否则失败
    '''
    buf = create_string_buffer(int_wantlen)
    ret = _dll.mrgGateWayQuery(ViSession_vi,string_to_charp(charp_cmd),buf,int_wantlen)
    if ret < 0:
        print("mrgGateWayQuery error ", ret)
        return ""
    else:
        return cbuf_to_string(buf)


def mrgGateWayIDNQuery(ViSession_vi):
    '''
    int mrgGateWayIDNQuery(ViSession  vi, char *idn);
    + 函数&说明 mrgGateWayIDNQuery
        获取网关识别信息
    + 参数 vi
        网关句柄
    + 参数 idn
        输出信息
    + 返回值
        0表示成功,负数表示失败
    '''
    buf = create_string_buffer(1024)
    ret = _dll.mrgGateWayIDNQuery(ViSession_vi, buf)
    if ret < 0:
        return ""
    else:
        return cbuf_to_string(buf)

##############################################################################

def mrdSend(vi, cmd):
    cmd = str.rstrip(cmd)
    if cmd[-1] != "\n":
        cmd += "\n"
    return mrgGateWaySendCmd(vi, cmd)

def mrdRecv(vi, len):
    return mrgGateWayRead(vi, len)

def mrdQuery(vi, cmd):
    cmd = str.rstrip(cmd)
    if cmd[-1] != "\n":
        cmd = cmd + "\n"
    return mrgGateWayQuery(vi, cmd, 1024)




if __name__ == "__main__":
    print("hello world")