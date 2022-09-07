import time
import pytest
import RS232
import pic_open

#pytest -vs test_ON-OFF1.py --count=10 --repeat-scope=session -x
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
class Test_01(object):
    def test_POWER_ON(self):
        time_begin = time.time()
        result = 0  #0为失败，1为成功
        
        data = (0xAA,0x01,0xC3,0x33,0x00,0x00,0x55) #开电
        g_pg.Send_data(data)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')
        time.sleep(2)
        if strRet[0] == 'Display_on':
            result_dis = 1
        else:
            result_dis = 0
        cap = pic_open.Video_get()
        result_pannl,num =  cap.checkdianliang()
        if result_pannl == True:
            result_pannl = 1
        else:
            result_pannl = 0
        
        result = result_dis*result_pannl

        self.POWER_OFF()

        assert result == 1

        
    def POWER_OFF(self):#Display_off-1
        data = (0xAA,0x01,0xC3,0x66,0x00,0x00,0x55) #关电
        g_pg.Send_data(data)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')
        time.sleep(2)
        #print(strRet[0])
        #close()

def delay_time(time_s):
    time.sleep(time_s)


    
if __name__ == "__main__":
    pytest.main(["-v", "test_dianlianglv.py",'--html=./report.html','--count=100'])