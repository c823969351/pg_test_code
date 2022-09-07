from socket import *
import pg_cmd
import time
import write_excel

class Pattentime(object):
    def __init__(self):
        self.pg = pg_cmd.ServPg(serv='10.10.10.10')


    def Pre_load(self):
        delay = 0.07
        tm = 0
        qid = 0
        for i in range(1,10):
            tm_begin_2 = time.time()
            time.sleep(delay)
            self.pg.displayId(i)
            #self.pg.displayNext()
            tm = (time.time() - tm_begin_2)
            write_excel.excel_writetime(tm)
            print('切图时间：%s'%tm)

        tm_begin_2 = time.time()
        time.sleep(delay)
        self.pg.displayId(0)
        tm = (time.time() - tm_begin_2)
        write_excel.excel_writetime(tm)
        print('切图时间：%s'%tm)


    def Non_preload(self):
        tm = 0
        qid = 0
        for i in range(1,10):
            tm_begin_2 = time.time()
            self.pg.displayId(i)
            time.sleep(2)
            qid = self.pg.displayQId()

            while int(qid) != i:
                qid = self.pg.displayQId()

            tm = (time.time() - tm_begin_2)
            write_excel.excel_writetime(tm)

            print('切图时间：%s'%tm)
        self.pg.displayId(0)
        
    def logicpattern(self):
        self.pg.logicpattern_on()
        delay = 0.07
        tm = 0
        qid = 0
        for i in range(3,14):
            tm_begin_2 = time.time()
            time.sleep(delay)
            self.pg.logicpattern(i)
            tm = (time.time() - tm_begin_2)
            write_excel.excel_writetime(tm)
            print('切图时间：%s'%tm)

        tm_begin_2 = time.time()
        time.sleep(delay)
        self.pg.displayId(0)
        tm = (time.time() - tm_begin_2)
        write_excel.excel_writetime(tm)
        print('切图时间：%s'%tm)
        

if __name__ == "__main__":
    tm_begin_1 = time.time()
    res = Pattentime()
    res.pg.open()
    try:
        #res.Non_preload()
        res.Pre_load()
        #res.logicpattern()
    except Exception as e:
        print("---异常---：", e)
        print("测试失败")
    print("测试时间")
    print(time.time() - tm_begin_1)
    res.pg.close()