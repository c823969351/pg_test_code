import socket
import time
import json 
import encodings
import paramiko
import os,sys
import datetime
import time

import PGtest_log
import configparser

nowtime = time.localtime()
strftime = time.strftime("%Y%m%d",nowtime)
logfile = ('pytest-'+strftime+'.log')
log = PGtest_log.Logger(logfile,level='info')
class ServPg( object ):

    def __init__( self, serv="10.10.10.10", port=5555 ):
        self._user = "root"
        self._pw = "mega.tech"
        self._tmp = "/tmp/"
        self._host = serv 
        self._port = port 

        self._sock = None 

    def open(self):
        self._sock = socket.socket()
        self._sock.connect( (self._host, self._port) )
        log.logger.info('sock.connect:%s,%s',self._host,self._port)
        pass 
        
    def close(self):
        if ( self._sock ):
            self._sock.close()
        pass

    def send( self, cmd ):
        cmd = cmd + "\n"
        # print( cmd )
        stream = encodings.utf_8.encode( cmd )
        log.logger.info('send:%s',cmd)
        self._sock.sendall( stream[0] )   

    def sendArbBytes( self, cmd, arbStream, tail=None  ):
        arbLen = len( arbStream )
        
        #cmd = cmd + ",#4%04d"%( arbLen )
        
        headStream = encodings.utf_8.encode( cmd )
        headLen = len( headStream[0] )
        
        # tail 
        if tail is None:
            tailLen = 0
        else:
            tailStream, _ = encodings.utf_8.encode( ","+tail )
            tailLen = len(tailStream)
        
        if arbLen:
            rawStream = bytearray( headLen + arbLen + tailLen + 8 )
            print( rawStream )
        else:
            rawStream = bytearray( headLen + tailLen +1 )
        # head
        for i in range( headLen ):
            rawStream[i] = headStream[0][i]
        print( rawStream )

        # tail 
        for i in range( tailLen ):
            rawStream[ headLen + i ] = tailStream[i]
        print( rawStream )
            
        # payload    
        if arbLen:
            blockdata = encodings.utf_8.encode(",#4%04d"%( arbLen ))
            for i in range( 7 + arbLen ):
                if i < 7 :
                    rawStream[ headLen + tailLen + i ] = blockdata[0][i]
                    print( rawStream )
                else:
                    rawStream[ headLen + tailLen + i ] = arbStream[i - 7]
            print( rawStream )
        else:
            pass
        
            
        rawStream[-1] = 0x0A
        print( rawStream )
        log.logger.info('sendArbBytes:%s',rawStream)
        self._sock.sendall( rawStream )   
        
    def sendArb( self, cmd, arb ):
    
        arbStream, _ = encodings.utf_8.encode( arb )
        arbLen = len( arbStream )
        log.logger.info('sendArb:cmd:%s,arb:%s',cmd,arbStream)
        
        self.sendArbBytes( cmd, arbStream )
     
    def query( self, cmd ):
        self.send( cmd )
        data = self._sock.recv( 2048 )
        buf = data.decode()  
        log.logger.info('query:%s',buf)
        return buf

    def readBytes( self ):
        data = self._sock.recv( 2048 )
        log.logger.info('readBytes:%s',data)
        return data 
        
    def readArbBytes( self ):
        data = self._sock.recv( 2048 )
        log.logger.info('readArbBytes_data:%s',data)
        if ( len(data) < 2 ):
            return None 
            
        # print( data )
        # check the first 
        if data[0]!=ord('#'):
            return None 
        headLen = (data[1]) - 0x30
        
        # the header 
        if ( len(data) < (2+headLen) ):
            return None 
        
        lenStr=""
        for i in range( headLen ):
            lenStr = lenStr + chr( data[2+i] )
        
        payloadLen = int(lenStr)
        if ( len(data) < (2+headLen+payloadLen) ):
            return None 
            
        payloads = bytearray( payloadLen )
        for i in range( payloadLen ):
            payloads[i] = data[ 2 + headLen + i ]
        log.logger.info('readArbBytes:%s',payloads)
        
        return payloads
    
    def fmtClr( self, clr ):
        return "#H%04X%04X%04X"%(clr[0],clr[1],clr[2])

    def rst( self ):
        self.dispOn(False)
        
        self.exitTest()
        
        self.clearText()
        
        self.cursorDisplay(False)
        
    def idn( self ):
        return self.query("*IDN?")

    def dispOn( self, onOff ):
        self.send( "DISPLAY:POWER %s" % ( "ON" if onOff  else "OFF" ) )
    
    def dispQOnoff( self ):
        self.query( "DISPLAY:POWER? " )
    
    def displayNext( self ):
        self.send( "DISPLAY:NEXT" )

    def displayPrev( self ):
        self.send( "DISPLAY:PREV"  )
    
    def displayId( self, id ):
        self.send( "DISPLAY:INDEX %d" % ( id ) )
    
    def displayQId( self ):
        id = self.query( "DISPLAY:INDEX?" )
        id = int(id.split()[0])
        return id

    def logicpattern_on(self):
        self.send( "DISPLAY:LPG:MODE ON")
    
    def logicpattern_off(self):
        self.send( "DISPLAY:LPG:MODE OFF")

    def logicpattern(self,id = 3):
        self.send("DISPLAY:LPG:INDEX %d" % ( id )) #3 -13

    def displayQname(self):
        name = self.query("DISPLAY:CURRENT?")
        name = str(name.split()[0])
        return name
    
    '''def displayFile( self, fullName, truncate=True ):
        files = self._transferFile( fullName, self._tmp, truncate )
        
        # show 
        self.send( "DISPLAY:TEST:MODE EXIT" )
        self.send( 'DISPLAY:DESIGNTE "%s"' % ( files[0] ) )

        return files'''
    def displayFile(self,path,fliename):
        files = self.filetoPG(path,fliename)
        self.send('DISPLAY:DESIGNTE "%s"' % ( files ) )
        
        
    def displayGray( self, gray ):
        self.send( "DISPLAY:TEST:MODE ENTER" )
        self.send( "DISPLAY:TEST:GRAYSCALE %d" % ( gray ) )
        
    def displayColor( self, clr ):
        self.send( "DISPLAY:TEST:MODE ENTER" )
        self.send( "DISPLAY:TEST:COLOR %s" % self.fmtClr(clr) )
        
    def exitTest( self ):
        self.send( "DISPLAY:TEST:MODE EXIT" )
        
    def _transferFile( self, fullName, dstPath, truncate=True ):
        transport = paramiko.Transport((self._host, 22))    
        transport.connect(username=self._user, password=self._pw )    
 
        # 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
        sftp = paramiko.SFTPClient.from_transport(transport)
 
        # 将本地 api.py 上传至服务器 /www/test.py。文件上传并重命名为test.py
        # get fileName
        lastSep = fullName.rfind('/')
        if  lastSep < 0:
            lastSep = fullName.rfind('\\')
        else:
            pass 
            
        if lastSep < 0:
            assert(False)
        
        rawFile=fullName[lastSep+1:]
        
        if truncate:
            extDot = rawFile.rfind(".")
            pureFileName = "userfile" + rawFile[extDot:]
        else:
            pureFileName = rawFile 
        
        t1 = datetime.datetime.now()
        sftp.put(fullName, dstPath+pureFileName )
        t2 = datetime.datetime.now()
        print( "transfer %s %s,%s,%d" % ( self._host, fullName, pureFileName, (t2-t1).seconds) )
        
        transport.close()
        
        return ( dstPath+pureFileName,pureFileName,rawFile)
    
    def cursorDisplay( self, onOff, clr=(255,0,0) ):
        if (onOff):
            self.send( "DISPLAY:CURSOR:COLOR %s" % self.fmtClr(clr) )
        
        self.send( "DISPLAY:CURSOR:MODE %s" % ( "ENTER" if onOff else "EXIT" ) )
        pass 
        
    def cursorPos( self, x, y ):
        self.send( "DISPLAY:CURSOR:POS %d,%d"%(x,y) )
        pass 
        
    def drawText( self, x,y,text,size=64,clr=(0x0,0x3ff,0x0) ):
        self.sendArb( "DISPLAY:DRAW:TEXT %d,%d,%d,%s"%( x,y,size,self.fmtClr(clr) ), text )
        # self.send( "DISPLAY:DRAW:TEXT %d,%d,%d,%s,\"%s\"" %( x,y,size, self.fmtClr(clr), text ) )

    def clearText( self ):
        self.send( "DISPLAY:DRAW:CLEAR" )
        pass 
        
    # config load 
    def loadXxx( self, xxx, file ):
        self.send( "CONFIG:%s:LOAD? \"%s\"" %(xxx, file) )
        
    def loadPower( self, file ):
        self.loadXxx( "POWER", file )
        
    def loadTiming( self, file ):
        self.loadXxx( "TIMING", file )
        
    def loadPlaylist( self, file ):
        self.loadXxx( "PLAYLIST", file )
    
    # VBO_4K10bit_12v_fps.tim
    def setFps( self, templateFile, fps ):
        timObj = PgTiming( templateFile )
        timObj.setFps( fps )
        
        files = self._transferFile( templateFile, "/app/res/product/timing/" )
        print(files)
        self.loadTiming( files[1] )
    
    # ad/da 
    def qAdcV( self, ch ):
        dats = self.query( "POWER:ADC? %s" % (ch) )
        ls = dats.split(",")
        return int(ls[0])
        
    def qAdcA( self, ch ):
        dats = self.query( "POWER:ADC? %s" % (ch) )
        ls = dats.split(",")
        return int(ls[1])
        
    def dac( self, ch, v ):
        self.send( "POWER:DAC %s,%d"%(ch,v) )
    
    def qDac( self, ch ):
        dats = self.query( "POWER:DAC? %s" % (ch) )
        return int(dats)
    #清楚电源保护状态    
    def powerClear( self ):
        self.send( "POWER:LIMIT:CLEAR" )
    #查询电源保护状态
    def powerState( self, ch ):
        dats = self.query( "POWER:LIMIT:STATE? %s"%(ch) )
        return dats 
    # power on 
    def powerOn( self, ch ):
        self.send( "DEVICE:POWER:OUTP %s,ON"%(ch) )
    # power off
    def powerOff( self, ch ):
        self.send( "DEVICE:POWER:OUTP %s,OFF"%(ch) )

    def powerVolt( self, ch, v ):
        self.send( "POWER:VOLT %s,%g"%(ch, v) )
   # read Volt
    def powerQVolt( self, ch ):
        dats = self.query( "POWE:VOLT? %s"%(ch) )
        return dats
    
    # read  CURRENT  
    def powerQCurrent( self, ch , v = "B"):
        dats = self.query( "POWE:CURR? %s,%s"%(ch, v) )
        return dats 
    # 电压开关    
    def powerOutputON( self, ch):
        self.send( "POWE:OUTP %s,ON"%(ch) )
    
    def powerOutputOFF( self, ch):
        self.send( "POWE:OUTP %s,OFF"%(ch) )

    def powerQOutput( self, ch):
        self.query( "POWE:OUTP? %s"%(ch) )

    # ovp 
    def powerOvp( self, ch, v ):
        self.send( "DEVICE:POWER:OVP %s,%g"%(ch, v ) )
        
    def powerOcp( self, ch, v ):
        self.send( "DEVICE:POWER:OCP %s,%g"%(ch, v ) )

     # uvp 
    def powerUvp( self, ch, v ):
        self.send( "DEVICE:POWER:UVP %s,%g"%(ch, v ) )
        
    def powerUcp( self, ch, v ):
        self.send( "DEVICE:POWER:UCP %s,%g"%(ch, v ) )
    
    def LPG_QRGB( self ):
        dats = self.query( "DISPLAY:LPG:RGB?")
        return dats
    
    def LPG_RGB(self,value = '#H7F007F007F'):
        self.send( "DISPLAY:LPG:RGB %s,OFF"%value )

    
    def temp(self):
        temp1,temp2 = self.query('DEVICE:TEMP?').split(',')#获取温度1为出风口，2为中间位置
        return temp1,temp2.split('\n')[0]
    
    def LPG_Q(self):
        return self.query("DISPLAY:LPG:MODE?")
    
    def TEST_LOADING(self):
        res = self.query("CONFIG:TEST:LOADING?").split('\n')[0]
        return res

    #读取电源保护值
    def powerQOUP(self,ch):
        self.query("POWER:LIMI:OVP? %s"%(ch))
        self.query("POWER:LIMI:OCP? %s"%(ch))
        self.query("POWER:LIMI:UVP? %s"%(ch))
        self.query("POWER:LIMI:UCP? %s"%(ch))
    #重启
    def reboot(self):
        self.send( "SYST:EXEC? reboot" )
        
    # gpio 
    def gpioLevel( self, level ):
        #                ch2, ch1
        vals = { "2.5": (0,0),
                 "3.3": (1,0),   
                 "5":  (1,1),   
            }
        assert( level in vals.keys() )
        if level in vals.keys():
            chId = 2
            for v in vals.get(level):
                self.send("DEVICE:GPIO:VALUE %d,%s" % ( chId, "HIGH" if v == 1 else "LOW" ) )
                chId = chId - 1
        pass 
        
    def gpioSet( self, pt, v ):
        assert( pt >= 1 and pt <= 11 )
        self.send("DEVICE:GPIO:VALUE %d,%s" % ( pt+2, "HIGH" if v == 1 else "LOW" ) )
        pass 
        
    # pwm
    def pwmSet( self, freq, width ):
        self.send("DEVICE:EDP:PWM:VALUE %d,%d" % ( freq, width ) )
        pass 
    
    """
    slaveAttr: (slave, slaveW )
    addrAttr: ( addr, addLen, bigEndian )
    """
    def iicWrite( self, bus01, slaveAttr, addrAttr, dataBytes ):
        # deload 
        slave, slaveW = slaveAttr
        addr, adrLen, bigEndian = addrAttr 
        
        head = "DEVICE:IIC:WRITE %d,%d,S%d" % (bus01,slave,slaveW )

        # add addr 
        payloads = bytearray( adrLen + len(dataBytes) )
        for i in range( adrLen ):
            if ( bigEndian ):
                payloads[ adrLen - 1 - i ] = addr&0xff
            else:
                payloads[i] = addr&0xff
            addr >>= 8
        # copy the databytes 
        for i in range( len(dataBytes ) ):
            payloads[ i + adrLen ] = dataBytes[i]
        self.sendArbBytes( head, payloads )
        
    def iicRead( self, bus01, slaveAttr, addrAttr , readLen ):
        
        slave, slaveW = slaveAttr
        if addrAttr:
            addr, adrLen, bigEndian = addrAttr
    
        head = "DEVICE:IIC:READ? %d,%d,S%d" % (bus01,slave,slaveW )
        tail = "%d" % (readLen)
        
        if addrAttr:
            adrBytes = bytearray( adrLen )
            for i in range( adrLen ):
                if ( bigEndian ):
                    adrBytes[ adrLen - 1 - i ] = addr&0xff
                else:
                    adrBytes[i] = addr&0xff
                addr >>= 8 
        else:
            adrBytes = bytearray()
        
        self.sendArbBytes( head, adrBytes, tail )
        pass 
        
    def iicSend( self, bus01, slaveAttr, dataBytes , preDat = False):
    
        # deload 
        slave, slaveW = slaveAttr
        if preDat:
            adrLen = len(preDat)
        else:
            adrLen = 0
        
        head = "DEVICE:IIC:WRITE %d,%d,S%d" % (bus01,slave,slaveW )
        
        # add pre 
        payloads = bytearray( adrLen + len(dataBytes) )
        for i in range( adrLen ):
            payloads[ i ] = preDat[i]
        
        # copy the databytes 
        for i in range( len(dataBytes ) ):
            payloads[ i + adrLen ] = dataBytes[i]
        
        self.sendArbBytes( head, payloads )
        
    def iicQuery( self, bus01, slaveAttr,readLen, preDat=0): 
        # deload 
        slave, slaveW = slaveAttr
        if preDat:
            adrLen = len(preDat)
        else:
            adrLen = 0
    
        head = "DEVICE:IIC:READ? %d,%d,S%d" % (bus01,slave,slaveW )
        tail = "%d" % (readLen)
        
        adrBytes = bytearray( adrLen )
        for i in range(adrLen):
            adrBytes[i] = preDat[i]
            
        # send 
        self.sendArbBytes( head, adrBytes, tail )
        
        # recv 
        return self.readArbBytes()

    def filetoPG(self,window_path,filename="test"):#传入升级文件到PG
        password = self._pw
        username = self._user
        Linux_ip = self._host
        Linux_path = self._tmp
        cmd1 = r'cd C:\Users\mega\AppData\Local\Programs\Python\Python39' ##本地PYTHON安装路径
        cmd2 = 'pscp -pw {password} -r {window_path} {username}@{Linux_ip}:{Linux_path}'.format( 
                password=password, window_path=window_path, username=username,Linux_ip=Linux_ip, Linux_path=Linux_path) 
        cmd3 = cmd1 + "&&" + cmd2
        os.system(cmd3)
        print('文件传入完成')
        return (Linux_path+filename)

    def pg_updata(self,mrd_name):
        print('开始升级')
        self.send('SYST:UPGR:START "%s%s"'%(self._tmp,mrd_name))
        #Str = pg.mrdQuery(visa,'SYST:UPGR:STATE?')
        PROG = self.query('SYST:UPGR:PROG?')
        while (PROG != "100\n" ):
            PROG = self.query('SYST:UPGR:PROG?')
            sys.stdout.write('已完成：%.1f%%'%float(int(PROG))+'\r')
            sys.stdout.flush()    
        print('升级完成')

if __name__ == "__main__":
    tm_begin = time.time()
    ip = "10.10.10.10"
    try:
        pg = ServPg(ip)
        pg.open()
        ch = 'VDD'
        tm_begin = time.time()
        pg.send('DISPLAY:LPG:MODE ON,OFF')
        pg.send('DISPLAY:LPG:INDEX 2,OFF')
        pg.LPG_RGB()
        print('时间{}ms'.format((time.time() - tm_begin)*1000))

        tm_begin = time.time()
        pg.LPG_QRGB()
        print('时间{}ms'.format((time.time() - tm_begin)*1000))
    except Exception as e:
        print("---异常---：", e)
        print("测试失败")
    print("测试时间")
    print(time.time() - tm_begin)
    pg.close
    
    