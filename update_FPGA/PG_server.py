import datetime
import encodings
import os
import socket
import sys
import paramiko
import time
from Find_PG import pg_ip



class ServPg(object):

    def __init__(self, serv=pg_ip(), port=5555):
        self._user = "root"
        self._pw = "mega.tech"
        self._tmp = "/tmp/"
        self._sock = None
        self._port = port
        if not serv:
            raise Exception('未检查到PG ip')
        else:
            self._host = serv
    
    def open(self):
        self._sock = socket.socket()
        self._sock.connect((self._host, self._port))
        pass

    def close(self):
        if (self._sock):
            self._sock.close()
        pass

    def send(self, cmd):
        cmd = cmd + "\n"
        # print( cmd )
        stream = encodings.utf_8.encode(cmd)
        self._sock.sendall(stream[0])

    def remove_space(self, data):
        return data.split()[0]
    
    def query(self, cmd):
        self.send(cmd)
        data = self._sock.recv(2048)
        buf = data.decode()
        if buf != '':
            buf = self.remove_space(buf)
        return buf
    
    def k160_version(self,num):
        result = {}
        for i in range(num):
            result[i] = self.query('PROJect:k160:READ? {},#H0'.format(i))
        return result
    
    def ZU7_version(self):
        return self.query('PROJect:MEMO:READ? #H80000000,U32')

    def _transferFile(self, fullName, dstPath, select_bin, truncate=True):
        transport = paramiko.Transport((self._host, 22))
        transport.connect(username=self._user, password=self._pw)

        # 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
        sftp = paramiko.SFTPClient.from_transport(transport)

        # 将本地 api.py 上传至服务器 /www/test.py。文件上传并重命名为test.py
        # get fileName
        lastSep = fullName.rfind('/')
        if lastSep < 0:
            lastSep = fullName.rfind('\\')
        else:
            pass

        if lastSep < 0:
            assert (False)

        rawFile = fullName[lastSep + 1:]

        if truncate:
            extDot = rawFile.rfind(".")
            if select_bin =='k160':
                pureFileName = "k160" + rawFile[extDot:]
            elif select_bin == 'ZU7':
                pureFileName = "BOOT" + rawFile[extDot:]
            else:
                raise('error')
        else:
            pureFileName = rawFile
        try:
            t1 = datetime.datetime.now()
            sftp.put(fullName, dstPath + pureFileName)
            t2 = datetime.datetime.now()
            print("transfer %s %s,%s,%d" % (self._host, fullName, pureFileName, (t2 - t1).seconds))
        except Exception as e:
            print('error:%s' % e)

        transport.close()

        return (dstPath, pureFileName, rawFile)


if __name__ == "__main__":
    pg = ServPg()
    pg.open()
    a = str(pg.k160_version(4))[1:-1]

    print(a)

