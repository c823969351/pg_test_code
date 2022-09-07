import re
import RS232
import write_csv
import time

com = "COM26"   #COM26 :MIPI 1  
                #COM21 :MIPI 2
g_pg = RS232.Communication(com, 115200, 15)

class curr_test(object):
    def __init__(self):
        pass
    def test_POWER_ON(self):
        data = (0xAA,0x01,0xC3,0x33,0x00,0x00,0x55) #开电
        g_pg.Send_data(data)
        time.sleep(4)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')

    def test_Show_VOLT(self):
        data = (0xAA,0x01,0xC3,0x55,0x00,0x00,0x55) #volt
        g_pg.Send_data(data)
        time.sleep(1)

        strRet = g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet = strRet.split('\r')
        led = strRet[1].split('  ')
        return led

if __name__ == '__main__':
    flag = curr_test()
    flag.test_POWER_ON()
    for i in range(100):
        ret = flag.test_Show_VOLT()
        write_csv.Csv_curr(ret[0].split('\n')[1],ret[1])
