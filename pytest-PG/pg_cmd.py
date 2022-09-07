import socket
from tempfile import tempdir
import time
import json
import encodings
import paramiko
import os, sys
import datetime
import time
import PGtest_log
import configparser


nowtime = time.localtime()
strftime = time.strftime("%Y%m%d", nowtime)
logfile = ('pytest-' + strftime + '.log')
log = PGtest_log.Logger(logfile, level='info')


class ServPG(object):
    def __init__(self, serv="10.10.10.10", port=5555):
        self._user = "root"
        self._pw = "mega.tech"
        self._tmp = "/tmp/"
        self._host = serv
        self._port = port
        self._sock = None

    def open(self):
        self._sock = socket.socket()
        self._sock.connect((self._host, self._port))
        log.logger.info('sock.connect:%s,%s', self._host, self._port)
        pass

    def close(self):
        if (self._sock):
            self._sock.close()
        pass

    def send(self, cmd):
        cmd = cmd + "\n"
        # print( cmd )
        stream = encodings.utf_8.encode(cmd)
        log.logger.info('send:%s', cmd)
        self._sock.sendall(stream[0])

    def sendArbBytes(self, cmd, arbStream, tail=None):
        arbLen = len(arbStream)

        cmd = cmd + ",#4%04d" % (arbLen)

        headStream = encodings.utf_8.encode(cmd)
        headLen = len(headStream[0])

        # tail
        if tail is None:
            tailLen = 0
        else:
            tailStream, _ = encodings.utf_8.encode("," + tail)
            tailLen = len(tailStream)

        rawStream = bytearray(headLen + arbLen + tailLen + 1)

        # head
        for i in range(headLen):
            rawStream[i] = headStream[0][i]

        # payload
        for i in range(arbLen):
            rawStream[headLen + i] = arbStream[i]

        # tail
        for i in range(tailLen):
            rawStream[headLen + arbLen + i] = tailStream[i]

        rawStream[-1] = 0x0A
        print(rawStream)
        log.logger.info('sendArbBytes:%s', rawStream)
        self._sock.sendall(rawStream)

    def sendArb(self, cmd, arb):

        arbStream, _ = encodings.utf_8.encode(arb)
        arbLen = len(arbStream)
        log.logger.info('sendArb:cmd:%s,arb:%s', cmd, arbStream)

        self.sendArbBytes(cmd, arbStream)

    def query(self, cmd):
        self.send(cmd)
        data = self._sock.recv(2048)
        buf = data.decode()
        log.logger.info('query:%s', buf)
        return buf

    def readBytes(self):
        data = self._sock.recv(2048)
        log.logger.info('readBytes:%s', data)
        return data

    def readArbBytes(self):
        data = self._sock.recv(2048)
        log.logger.info('readArbBytes_data:%s', data)
        if (len(data) < 2):
            return None

        # print( data )
        # check the first
        if data[0] != ord('#'):
            return None
        headLen = (data[1]) - 0x30

        # the header
        if (len(data) < (2 + headLen)):
            return None

        lenStr = ""
        for i in range(headLen):
            lenStr = lenStr + chr(data[2 + i])

        payloadLen = int(lenStr)
        if (len(data) < (2 + headLen + payloadLen)):
            return None

        payloads = bytearray(payloadLen)
        for i in range(payloadLen):
            payloads[i] = data[2 + headLen + i]
        log.logger.info('readArbBytes:%s', payloads)

        return payloads

    def fmtClr(self, clr):
        return "#H%04X%04X%04X" % (clr[0], clr[1], clr[2])  ##颜色转换为16进制类型

########################显示协议指令####################################################

    def dispOn(self):
        self.send("DISPLAY:POWER ON")

    def dispOff(self):
        self.send("DISPLAY:POWER OFF")

    def dispQonoff(self):
        onoff = self.query("DISPLAY:POWER? ")
        onoff = onoff.split()[0]
        return onoff

    def dispNext(self):
        self.send("DISPLAY:NEXT")

    def dispPrev(self):
        self.send("DISPLAY:PREV")

    def dispIndex(self, id):
        self.send("DISPLAY:INDEX %d" % (id))

    def dispQindex(self):
        id = self.query("DISPLAY:INDEX?")
        id = int(id.split()[0])
        return id

    def dispQname(self):
        name = self.query("DISPLAY:CURRENT?")
        name = str(name.split()[0])
        return name

    def rst(self):
        self.dispOff()
        self.powerClear()

#################################电源协议指令##################################################

    def powerClear(self):
        self.send("POWER:LIMIT:CLEAR")

    #查询电源保护状态
    def powerState(self, ch):
        dats = self.query("POWER:LIMIT:STATE? %s" % (ch))
        return dats

    # power on
    def powerOn(self, ch):
        self.send("POWER:OUTP %s,ON" % (ch))

    # power off
    def powerOff(self, ch):
        self.send("POWER:OUTP %s,OFF" % (ch))

    def powerQoutput(self, ch):
        onoff = self.query("POWE:OUTP? %s" % (ch))
        onoff = onoff.split()[0]
        return onoff

    def powerVolt(self, ch, v):
        self.send("POWER:VOLT %s,%g" % (ch, v))

    # read Volt
    def powerQvolt(self, ch):
        dats = self.query("POWE:VOLT? %s" % (ch))
        dats = float(dats.split()[0])
        return dats

    # read  CURRENT
    def powerQcurrent(self, ch, v="B"):
        dats = self.query("POWE:CURR? %s,%s" % (ch, v))
        return dats

    # ovp
    def powerOvp(self, ch, v):
        self.send("POWER:OVP %s,%g" % (ch, v))

    def powerOcp(self, ch, v):
        self.send("POWER:OCP %s,%g" % (ch, v))

    # uvp
    def powerUvp(self, ch, v):
        self.send("POWER:UVP %s,%g" % (ch, v))

    def powerUcp(self, ch, v):
        self.send("POWER:UCP %s,%g" % (ch, v))
    
    def temp(self):
        temp1,temp2 = self.query('DEVICE:TEMP?')#获取温度1为出风口，2为中间位置
        return temp1,temp2

    #读取电源保护值
    def powerQallp(self, ch):
        self.query("POWER:LIMI:OVP? %s" % (ch))
        self.query("POWER:LIMI:OCP? %s" % (ch))
        self.query("POWER:LIMI:UVP? %s" % (ch))
        self.query("POWER:LIMI:UCP? %s" % (ch))
#########################################系统指令#######################################################
    #重启
    def reboot(self):
        self.send("SYST:EXEC? reboot")

    def powerRelayON(self,ch):
        self.send("POWER:RELAY %s,ON" % (ch))
    
    def powerRelayOff(self,ch):
        self.send("POWER:RELAY %s,OFF" % (ch))

    def powerDCENON(self,ch):
        self.send("POWER:DCEN %s,ON" % (ch))

    def powerDCENOff(self,ch):
        self.send("POWER:DCEN %s,OFF" % (ch))