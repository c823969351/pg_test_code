from datetime import datetime
from socket import *
import pg_cmd
import time
from Find_PG import *
import pandas as pd

# ip = mrgFindGateWay()
# ip = " ".join(ip)
ip = '10.10.10.101'
pg = pg_cmd.ServPg(ip)
pg.open()


def Qstate(res='ALL'):
    pg.powerState(res)
    pg.powerQOutput(res)
    pg.powerQVolt(res)
    pg.powerQOUP(res)
    pg.powerQCurrent(res)


if __name__ == "__main__":
    tm_begin = time.time()
    i = 0
    df = pd.DataFrame(columns=['中间温度','风扇温度','时间'])
    while True:
        i = i+1
        try:
            pg.dispOn()
            IDN = pg.idn()
            print(IDN)
            if IDN == '电源已经开启 or 自检失败，需要校准！\n':
                raise Exception('开电失败-1')
            #pg.powerOn("ALL")
            time.sleep(1)
            #pg.powerClear()
            #Qstate() #读所有状态
            # state_nm = pg.powerState("ALL").split(',')
            # index = len(state_nm)
            # state_nm[index-1]=state_nm[index-1].split('\n')[0]
            # for state_i in range(index):
            #     if state_nm[state_i] == '0':
            #         pass
            #     else:
            #         raise Exception('电源保护')
            #############切图测试###############
            for a in range(5):
                pg.displayId(a)
                time.sleep(1)
                qid = pg.displayQId()
                if int(qid) == a:
                    pass
                else:
                    raise Exception('切图失败')
            pg.dispOff()
            time.sleep(2)

        #############################################################################
        #     temp1,temp2 = pg.temp()#1风扇，2中间
        #     df.loc[i] = [temp1,temp2,datetime.now()]
        #     df.to_excel('温度数据.xlsx')
        #     print(df)
        # #####################关电复位###########################################################
        #     time.sleep(2)
        #     pg.rst()
        #     time.sleep(3)
        #     pg.powerState("ALL")
            print("第%s次测试"%i)
            #Read_EDID()
            #pg.powerOn("ALL",True) ##True = ON
            #time.sleep(5)
            #pg.powerOn("ALL","OFF") ##False = OFF
            #pg.reboot()  ##重启
            #time.sleep(1)
        except Exception as e:
            pg.rst()
            print("---异常---：", e)
            print("测试失败")
            break
    print("第%s次测试"%i)
    print("测试时间")
    print(time.time() - tm_begin)
    pg.close