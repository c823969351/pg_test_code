import re
import time
from socket import *


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


def get_localhost_ip():
    ipList = list()
    addrInfoList = getaddrinfo(gethostname(), None)
    for addrinfo in addrInfoList:
        if addrinfo[0] == AF_INET:
            ipList.append(addrinfo[4][0])

    return list_remove_same(ipList)


def mrgFindGateWay():
    devList = list()
    localIPList = get_localhost_ip()
    for strIP in localIPList:
        udpIP = '255.255.255.255'
        client = socket(AF_INET, SOCK_DGRAM)
        client.bind((strIP, 0))
        client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        client.settimeout(0.5)
        client.sendto(b"*?", (udpIP, 6000))
        while True:
            try:
                data, addr = client.recvfrom(1024)
                if data == b'MegaRobot Technologies,ThorPG':
                    devList.append(addr[0])
            except:
                break
        client.close()
    return list_remove_same(devList)


def pg_ip():
    tm_begin = time.time()
    for i in range(10):
        try:
            ip = mrgFindGateWay()
            if ip != []:
                ip = " ".join(ip)
                return ip
            else:
                time.sleep(1)
                continue
        except Exception as e:
            raise ("err:", e)
    print(time.time() - tm_begin)
    return('未找到PG')
    


def test_get_ip():
    udpIP = '255.255.255.255'
    client = socket(AF_INET, SOCK_DGRAM)
    client.bind(('10.10.10.35', 0))
    client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    client.settimeout(0.5)
    client.sendto(b"*?", (udpIP, 6000))
    while True:
        try:
            data, addr = client.recvfrom(1024)
            if data == b'MegaRobot Technologies,ThorPG':
                devList.append(addr[0])
        except:
            break
    client.close()


######硬重启时间测试###############
if __name__ == "__main__":
    # tm_begin = time.time()
    # ip = list()
    # time.sleep(1)
    # try:
    #     while 1:
    #         if ip == "10.10.10.10":
    #             print("重启完成")
    #             break
    #         else:
    #             ip = mrgFindGateWay()
    #             ip = " ".join(ip)
    #             print("启动中")
    # except Exception as e:
    #     print("err:", e)
    # print(time.time() - tm_begin)
    ip = pg_ip()
    print(ip)
