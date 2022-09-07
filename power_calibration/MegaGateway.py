# -*- coding:utf-8 -*-

from socket import *


##############################################################################
### 删除list指定值的所有元素
def list_remove_all(lst, ele):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == ele:
            lst.remove(ele)
    return lst


### 去掉重复元素
def list_remove_same(lst):
    nlst = list(set(lst))
    nlst.sort(key=lst.index)
    return nlst


##############################################################################
def get_localhost_ip():
    ipList = list()
    addrInfoList = getaddrinfo(gethostname(), None)
    for addrinfo in addrInfoList:
        if addrinfo[0] == AF_INET:
            ipList.append(addrinfo[4][0])

    return list_remove_same(ipList)


##############################################################################
def mrgFindGateWay():
    devList = list()
    localIPList = get_localhost_ip()
    for strIP in localIPList:
        lst = list(filter(None, strIP.split('.')))
        lst[3] = "255"
        udpIP = ".".join(lst)
        client = socket(AF_INET, SOCK_DGRAM)
        client.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        client.settimeout(0.5)
        client.sendto(b"*?", (udpIP, 6000))
        while True:
            try:
                data, addr = client.recvfrom(1024)
                if data == b'MegaRobot Technologies,ThorPG':
                    devList.append('TCPIP0::' + addr[0] + '::inst0::INSTR')
            except:
                break
        client.close()
    return list_remove_same(devList)


def mrgOpenGateWay(char_p_desc, int_timeout_ms):
    lst = list(filter(None, char_p_desc.split('::')))
    client = socket(AF_INET, SOCK_STREAM)
    client.setsockopt(SOL_SOCKET, SO_SNDBUF, 1024 * 1024)
    client.setsockopt(SOL_SOCKET, SO_RCVBUF, 1024 * 1024)
    client.settimeout(int_timeout_ms / 1000.0)
    ret = client.connect_ex((lst[1], 5555))
    if ret == 0:
        return client
    else:
        client.close()
        return None


def mrgCloseGateWay(visa):
    return visa.close()


def mrgGateWaySendCmd(visa, cmd):
    visa.send(cmd.encode())


def mrgGateWayRead(visa, recvlen):
    return visa.recv(recvlen).decode('utf-8')


def mrgGateWayQuery(visa, cmd, recvlen):
    visa.send(cmd.encode())
    return visa.recv(recvlen).decode('utf-8')


def mrgGateWayIDNQuery(visa):
    return mrgGateWayQuery(visa, "*IDN?\n", 1024)


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
