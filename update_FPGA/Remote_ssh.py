#-*- encoding:utf8 -*-
import re
from symbol import return_stmt
import paramiko
import sys
import time

# paramiko.util.log_to_file('ssh{}.log'.format(time.strftime("%Y-%m-%d", time.localtime())))


class Remote():
    def __init__(self, host, password, port=22, user='root'):
        self.port = port
        self.user = user
        self.password = password
        self.host = host
        self.transport()
        self.conn()

    def transport(self):
        self.transport = paramiko.Transport(self.host, self.port)
        self.transport.connect(username=self.user, password=self.password)

    def conn(self):
        self.myclient = paramiko.SSHClient()
        self.myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.myclient.connect(hostname=self.host,
                              port=self.port,
                              username=self.user,
                              password=self.password)

    def command(self, command):
        stdin, stdout, stderr = self.myclient.exec_command(command)
        print('{}===>>>'.format(self.host))
        result = stdout.readlines()
        print(result)
        return result

    def download(self, remotepath, localpath):
        self.remotepath = remotepath
        self.localpath = localpath
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.sftp.get(self.remotepath, self.localpath)

    def put(self, localpath, remotepath):
        self.localpath = localpath
        self.remotepath = remotepath
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.sftp.put(self.localpath, self.remotepath)

    def close(self):
        if self.transport:
            self.transport.close()
        if self.myclient:
            self.myclient.close()


if __name__ == "__main__":
    remote = Remote('10.10.10.101', 'mega.tech')#'192.168.64.130', 'jw.chen'
    #remote.download('D:/PGtestengine/aaa.log', '/tmp/ssh.log')
    #remote.put('D:/PGtestengine/ssh.log',
    #           '/tmp/ssh.log')
    remote.command('cd /app ; ls')
