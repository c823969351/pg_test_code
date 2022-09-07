import time
import pytest
import pg_cmd
import write_excel

ip = "10.10.10.10"
pg = pg_cmd.ServPG(ip)


@pytest.fixture(scope='class')
def serpg():
    pg.open()
    print('Connection successful')

    yield

    time.sleep(2)
    #pg.rst()
    pg.close()
    print('Connection closed')

@pytest.fixture(scope='class')
def disponoff():
    pg.dispOn()
    time.sleep(2)
    print('Display ON!!!')

    yield

    pg.dispOff()
    print('Display OFF!!!')


@pytest.mark.usefixtures('serpg')
class Test_power:################电源测试

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('ELVDD', 1.5),
                            ('ELVDD', 4),
                            ('ELVDD', 15)
                            ])
    def test_ELVDD(self,power, volt):

        self.Power_on(power,volt)

        time.sleep(2)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1.5)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VBL', 1.5),
                            ('VBL', 1.8),  
                            ('VBL', 15)
                            ])
    def test_VBL(self,power, volt):
        self.Power_on(power,volt)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1.5)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('TPVDDIO', 1.5),
                            ('TPVDDIO', 1.8),
                            ('TPVDDIO', 15)
                            ])
    def test_TPVDDIO(self,power, volt):
        self.Power_on(power,volt)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1.5)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))


    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDDIO', 1.5),
                            ('VDDIO', 1.8),
                            ('VDDIO', 15)
                            ])
    def test_VDDIO(self,power, volt):
        self.Power_on(power,volt)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1.5)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))


    @pytest.mark.parametrize('power, volt', 
                            [
                            ('TPVDD', 1.5),
                            ('TPVDD', 1.8),
                            ('TPVDD', 15)
                            ])
    def test_TPVDD(self,power, volt):
        self.Power_on(power,volt)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1.5)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))


    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDD', 1.5),
                            ('VDD', 3.3), 
                            ('VDD', 15)
                            ])
    def test_VDD(self,power, volt):
        self.Power_on(power,volt)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1.5)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))
    

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VGH', 1),
                            ('VGH', 16), 
                            ('VGH', 24)
                            ])
    def test_VGH(self,power, volt):
        self.Power_on(power,volt)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))
    
    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VGL', -1),
                            ('VGL', -16), 
                            ('VGL', -24)
                            ])
    def test_VGL(self,power, volt):
        self.Power_on(power,volt)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('ELVSS', -3),
                            ('ELVSS', -6), 
                            ('ELVSS', -15)
                            ])
    def test_ELVSS(self,power, volt):
        self.Power_on(power,volt)
        pw = pg.powerQvolt(power)
        write_excel.excel_writevolt(power,pw,volt)
        self.Power_off(power,1)
        assert (pw < (volt+0.01)) and (pw > (volt-0.01))
    
    def Power_on(self,power,volt):
        pg.powerRelayON(power)
        time.sleep(0.2)
        pg.powerVolt(power,volt)
        time.sleep(0.2)
        pg.powerDCENON(power)
        time.sleep(0.2)
    
    def Power_off(self,power,volt_min):
        pg.powerRelayOff(power)
        time.sleep(0.2)
        pg.powerDCENOff(power)
        time.sleep(0.2)
        pg.powerVolt(power,volt_min)
        time.sleep(0.2)
    



if __name__ == "__main__":
    '''pg.open()
    print(pg.query('*IDN?'))
    pg.powerOff('ALL')
    pg.close'''
    pytest.main(["-vs", "test_ThorA-P102.py"])

    