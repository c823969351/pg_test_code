import pg_cmd
import time
import numpy as np
pg = pg_cmd.ServPg(serv='10.10.10.127',port=5555)
pg.open()
tm_begin = time.time()

def test1():
    for x,y in zip(range(0,3840,50),range(0,2160,20)):
        pg.cursorPos(x,y)
        time.sleep(0.03)


def test2():
    for i in range(80):
        x = np.random.randint(0,3840,size=1)
        y = np.random.randint(0,2160,size=1)
        pg.cursorPos(x,y)
        time.sleep(0.08)

if __name__ == "__main__":
    try:
        pg.logicpattern_on()
        pg.logicpattern(8)
        pg.cursorDisplay(True)
        test1()
        #test2()
    except Exception as e:
        print("---异常---：", e)
        print("测试失败")
    print("测试时间")
    print(time.time() - tm_begin)
    pg.close