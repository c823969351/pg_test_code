import time
import pytest
import RS232

#pytest -vs .\test_M695_1.py --count=5  --repeat-scope=session -x
com = "COM9"    

g_pg = RS232.Communication(com, 115200, 15)

DELAY = 1

@pytest.fixture(scope='class')
def serpg():
    g_pg.Open_Engine()
    print('Connection successful')

    yield

    time.sleep(1)
    g_pg.Close_Engine()
    print('Connection closed')

@pytest.mark.usefixtures('serpg')
class Test_01:
    def test_POWER_ON(self):
        data = (0xAA,0x01,0xC3,0x33,0x00,0x00,0x55) #开电
        g_pg.Send_data(data)
        time.sleep(4)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')
        assert strRet[0] == "Display_on"

    def test_READ_ID(self):
        data = (0xAA,0x01,0xC3,0xD1,0x00,0x00,0x55) 
        g_pg.Send_data(data)
        time.sleep(2)
        strRet = g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet = strRet.split('\r')
        assert strRet[0] == "00 00 01 C5 01"

    def test_READ_SN(self):
        data = (0xAA,0x01,0xC3,0xD2,0x00,0x00,0x55) 
        g_pg.Send_data(data)
        time.sleep(2)
        strRet = g_pg.Recive_data(1)
        strRet = strRet.split('\r')
        assert strRet[1] == '\n0XF1H_0 = 0x39' or strRet[1] == '\n0x10,0x39'

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
        strRet[0] = strRet[0][0:3]
        assert strRet[0] == 'LCD'
        

    def test_Sleep_IN(self):
        data = (0xAA,0x01,0xC3,0x44,0x00,0x00,0x55) #sleep in-1
        g_pg.Send_data(data)
        strRet = g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet += g_pg.Read_Line()
        strRet = strRet.split('\r')
        time.sleep(3)
        assert strRet[0] == 'Sleep_in'

    def test_Sleep_OUT(self):
        data = (0xAA,0x01,0xC3,0x88,0x00,0x00,0x55) #sleep out-1
        g_pg.Send_data(data)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')
        time.sleep(3)
        assert strRet[0] == 'Sleep_out'


    @pytest.mark.parametrize('num', [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08])
    def test_SHOW_PATTERN(self,num):#切图-1
        data = (0xAA,0x01,0xC3,num,0x00,0x00,0x55) 
        g_pg.Send_data(data)
        time.sleep(2)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')
        frame = 'frame='+str(num)
        assert strRet[0] == frame

        
    def test_POWER_OFF(self):#Display_off-1
        data = (0xAA,0x01,0xC3,0x66,0x00,0x00,0x55) #关电
        g_pg.Send_data(data)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')
        time.sleep(2)
        assert strRet[0] == 'Display_off'
        #close()

def delay_time(time_s):
    time.sleep(time_s)

    
if __name__ == "__main__":
    '''pg.open()
    print(pg.query('*IDN?'))
    pg.powerOff('ALL')
    pg.close'''
    pytest.main(["-s", r"D:\testCode\pytest-PG\m695\test_M695_1.py"])