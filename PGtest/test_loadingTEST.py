from Find_PG import *
import pg_cmd
import time

ip = "10.10.10.10"
file_name = "mrdPatternGenerator_01.00.00.02.mrd"
file_path = r"D:\Thor_A_mrd"
window_path='{file_path}\\{file_name}' .format(file_path = file_path ,file_name = file_name)

def reboot_test():
    udpip = list()
    pg.reboot()  ##重启
    time.sleep(2)
    while 1:
        if udpip == ip:
            break
        else:
            udpip = mrgFindGateWay()
            udpip = " ".join(udpip)
            print("重启中")

def pg_updata():
    pg.filetoPG(window_path) #升级文件传入PG
    pg.pg_updata(file_name)  #升级PG
    reboot_test() ##重启

    pg.open()
    IDN = pg.idn()
    print(IDN)

    return IDN
 

if __name__ == "__main__":

    tm_begin = time.time()
    try:
        pg = pg_cmd.ServPg(ip)
        pg.open()
        IDN = pg.idn()
        print(IDN)

        aft_IDN = pg_updata()
        print("升级完成")
    except Exception as e:
        print("---异常---：", e)
        print("测试失败")
    print("测试时间")
    #print("第%s次升级"%i)
    print(time.time() - tm_begin)
    pg.close