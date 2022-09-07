import time
import pytest
import pg_cmd
import write_excel
import RS232
import RigolTest



ip = "10.10.10.10"
pg = pg_cmd.ServPG(ip)



class Test_power(object):################电源测试

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
        return strRet



    def test_POWER_OFF(self):#Display_off-1
        data = (0xAA,0x01,0xC3,0x66,0x00,0x00,0x55) #关电
        g_pg.Send_data(data)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')
        time.sleep(2)

def IOVCC():
    test.test_POWER_ON()
    time.sleep(1)
    ret =  test.test_Show_VOLT()
    curr = rigol.Qcurr()
    data = ret[0] + curr
    return data

def LED():
    test.test_POWER_ON()
    time.sleep(1)
    ret =  test.test_Show_VOLT()
    curr = rigol.Qcurr()
    data = ret[1] + curr
    return data

def VSP():
    test.test_POWER_ON()
    time.sleep(1)
    ret =  test.test_Show_VOLT()
    curr = rigol.Qcurr()
    data = ret[2] + curr
    return data

def VSN():
    test.test_POWER_ON()
    time.sleep(1)
    ret =  test.test_Show_VOLT()
    curr = rigol.Qcurr()
    data = ret[3] + curr
    return data
    



if __name__ == "__main__":

    test = Test_power()
    mipichannl = input('1/2')
    if mipichannl == '1':
        com = "COM9" 
    else:
        com = "COM21"
    g_pg = RS232.Communication(com, 115200, 15)
    rigol = RigolTest.RigolTest()

###################################################################################
    data = IOVCC()
    write_excel.TEST(str(data))

    '''data = LED()
    data = data.split('\n')[1]
    write_excel.TEST(str(data))

    data = VSP()
    data = data.split('\n')[1]
    write_excel.TEST(str(data))

    data = VSN()
    data = data.split('\n')[1]
    write_excel.TEST(str(data))'''