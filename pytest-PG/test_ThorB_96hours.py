import time
import pytest
import pg_cmd

ip = "10.10.10.10"
pg = pg_cmd.ServPG(ip)

@pytest.fixture(scope='class')
def serpg():
    pg.open()
    print('Connection successful')

    yield

    time.sleep(1)
    pg.rst()
    pg.close()
    print('Connection closed')

@pytest.fixture(scope='class')
def disponoff():
    pg.dispOn()
    time.sleep(1)
    print('Display ON!!!')

    yield

    pg.dispOff()
    print('Display OFF!!!')


@pytest.mark.usefixtures('serpg')
class Test_power:################电源测试
    @pytest.mark.parametrize('power, onoff', 
                            [('VDD1', 'ON'), 
                            ('VDD2', 'ON'),
                            ('VIF', 'ON'), 
                            ('VDIM', 'ON')])
    def test_power(self,power, onoff):
        pg.powerOn(power)
        time.sleep(0.2)
        assert pg.powerQoutput(power) == onoff
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDD1', 2),
                            ('VDD1', 5), 
                            ('VDD1', 4),
                            ('VDD1', 9),
                            ('VDD1', 12), 
                            ('VDD1', 20)
                            ])
    def test_VDD1(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDD2', 2),
                            ('VDD2', 5), 
                            ('VDD2', 4),
                            ('VDD2', 9),
                            ('VDD2', 12), 
                            ('VDD2', 20)
                            ])
    def test_VDD2(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VIF', 5),
                            ('VIF', 7), 
                            ('VIF', 9),
                            ('VIF', 12),
                            ('VIF', 15)
                            ])
    def test_VIF(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VIF', 5),
                            ('VIF', 7), 
                            ('VIF', 9),
                            ('VIF', 12),
                            ('VIF', 15)
                            ])
    def test_VIF(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    
    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDIM', 1),
                            ('VDIM', 2), 
                            ('VDIM', 3),
                            ('VDIM', 4),
                            ('VDIM', 5)
                            ])
    def test_VDIM(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)
        

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDD1', -1),
                            ('VDD1', 0),
                            ('VDD1', 1),
                            ('VDD1', 26), 
                            ('VDD1', 100)
                            ])
    def test_VDD1_BV(self,power, volt):
        pg.powerOn(power)
        time.sleep(1)
        a = pg.powerQvolt(power)
        pg.powerOff(power)
        time.sleep(1)
        ######################
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        b = pg.powerQvolt(power)
        assert round(a,2) == round(b,2) 
        pg.powerOff(power)
        time.sleep(1)


    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDD2', -1),
                            ('VDD2', 0),
                            ('VDD2', 1),
                            ('VDD2', 26), 
                            ('VDD2', 100)
                            ])
    def test_VDD2_BV(self,power, volt):
        pg.powerOn(power)
        time.sleep(1)
        a = pg.powerQvolt(power)
        pg.powerOff(power)
        time.sleep(1)
        ######################
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        b = pg.powerQvolt(power)
        assert round(a,2) == round(b,2) 
        pg.powerOff(power)
        time.sleep(1)

    
    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VIF', -1),
                            ('VIF', 0),
                            ('VIF', 4),
                            ('VIF', 16), 
                            ('VIF', 100)
                            ])
    def test_VIF_BV(self,power, volt):
        pg.powerOn(power)
        time.sleep(1)
        a = pg.powerQvolt(power)
        pg.powerOff(power)
        time.sleep(1)
        ######################
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        b = pg.powerQvolt(power)
        assert round(a,2) == round(b,2) 
        pg.powerOff(power)
        time.sleep(1)

    
    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDIM', -1),
                            ('VDIM', 0),
                            ('VDIM', 0.5),
                            ('VDIM', 6), 
                            ('VDIM', 100)
                            ])
    def test_VDIM_BV(self,power, volt):
        pg.powerOn(power)
        time.sleep(1)
        a = pg.powerQvolt(power)
        pg.powerOff(power)
        time.sleep(1)
        ######################
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        b = pg.powerQvolt(power)
        assert round(a,2) == round(b,2) 
        pg.powerOff(power)
        time.sleep(1)


    

@pytest.mark.usefixtures('serpg')
class Test_display:###################显示测试
    def test_dispPower(self,disponoff):
        assert pg.dispQonoff() == 'ON'

@pytest.mark.usefixtures('serpg','disponoff')
class Test_crop(): ##############切图测试
    def next_pattern(self):
        pg.dispNext()

    def prev_pattern(self):
        pg.dispPrev()

    def test_next(self):
        self.next_pattern()
        assert pg.dispQindex() == 1    

    def test_prev(self):
        self.prev_pattern()
        assert pg.dispQindex() == 0

    @pytest.mark.parametrize('id',[1,3,5,7,9,2,4,6,8])
    def test_index(self,id):
        pg.dispIndex(id)
        time.sleep(0.5)
        assert pg.dispQindex() == id

    def test_0(self):
        pg.dispOff()
        time.sleep(0.5)
        pg.dispOn()
        time.sleep(0.5)
        assert pg.dispQindex() == 0

if __name__ == "__main__":
    '''pg.open()
    print(pg.query('*IDN?'))
    pg.powerOff('ALL')
    pg.close'''
    pytest.main(["-vs", "test_ThorB_96hours.py"])