import time
import pytest
import RS232

#pytest -vs test_ON-OFF1.py --count=10 --repeat-scope=session -x
com = "COM9"   
g_pg = RS232.Communication(com, 115200, 15)
g_pg.Close_Engine()

logfile = None
logfilename = ""

DELAY = 1

csv_file = None

def print_log(*args):
    strTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print( strTime + ": ", end="")
    print(args)
    global logfile
    global logfilename
    if logfile == None:
        logfilename = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) +".log"
        logfile = open(logfilename, "wt")

    logfile.write( strTime + ": ")
    logfile.write(str(args) + '\n')
    logfile.flush()

    global csv_file
    '''if csv_file == None:
        csv_file = open(logfilename + ".csv", "wt")'''

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
        
        data = (0xAA,0x01,0xC3,0x33,0x00,0x00,0x55) #开电
        g_pg.Send_data(data)
        strRet = g_pg.Read_Line()
        strRet = strRet.split('\r')
        time.sleep(2)
        assert strRet[0] == "Display_on"

        
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
    pytest.main(["-v", "test_ON-OFF1.py"])