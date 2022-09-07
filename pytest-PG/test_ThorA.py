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
                            [('VBL', 'ON'), 
                            ('ELVDD', 'ON'),
                            ('VDD', 'ON'), 
                            ('VDDIO', 'ON'),
                            ('TPVDD', 'ON'), 
                            ('VGH', 'ON'),
                            ('ELVSS', 'ON'),
                            ('VGL', 'ON'),])
    def test_power(self,power, onoff):
        pg.powerOn(power)
        time.sleep(0.2)
        assert pg.powerQoutput(power) == onoff
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VBL', 1),
                            ('VBL', 3), 
                            ('VBL', 5),
                            ('VBL', 7),
                            ('VBL', 9), 
                            ('VBL', 15)
                            ])
    def test_VBL(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('ELVDD', 1),
                            ('ELVDD', 3), 
                            ('ELVDD', 5),
                            ('ELVDD', 7),
                            ('ELVDD', 9), 
                            ('ELVDD', 15)
                            ])
    def test_ELVDD(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDD', 1),
                            ('VDD', 3), 
                            ('VDD', 5),
                            ('VDD', 7),
                            ('VDD', 9), 
                            ('VDD', 15)
                            ])
    def test_VDD(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VDDIO', 1),
                            ('VDDIO', 3), 
                            ('VDDIO', 5),
                            ('VDDIO', 7),
                            ('VDDIO', 9), 
                            ('VDDIO', 15)
                            ])
    def test_VDDIO(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    
    @pytest.mark.parametrize('power, volt', 
                            [
                            ('TPVDD', 1),
                            ('TPVDD', 3), 
                            ('TPVDD', 5),
                            ('TPVDD', 7),
                            ('TPVDD', 9), 
                            ('TPVDD', 15)
                            ])
    def test_TPVDD(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('TPVDDIO', 1),
                            ('TPVDDIO', 3), 
                            ('TPVDDIO', 5),
                            ('TPVDDIO', 7),
                            ('TPVDDIO', 9), 
                            ('TPVDDIO', 15)
                            ])
    def test_TPVDDIO(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)
    

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VGH', 1),
                            ('VGH', 6), 
                            ('VGH', 10),
                            ('VGH', 14),
                            ('VGH', 18), 
                            ('VGH', 24)
                            ])
    def test_VGH(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)
    

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('ELVSS', -1),
                            ('ELVSS', -3), 
                            ('ELVSS', -5),
                            ('ELVSS', -7),
                            ('ELVSS', -10), 
                            ('ELVSS', -15)
                            ])
    def test_ELVSS(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)
    

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VGL', -1),
                            ('VGL', -6), 
                            ('VGL', -10),
                            ('VGL', -14),
                            ('VGL', -18), 
                            ('VGL', -24)
                            ])
    def test_ELVSS(self,power, volt):
        pg.powerVolt(power,volt)
        pg.powerOn(power)
        time.sleep(1)
        assert (pg.powerQvolt(power) < (volt+0.1)) and (pg.powerQvolt(power) > (volt-0.1))
        pg.powerOff(power)
        time.sleep(1)
        

    @pytest.mark.parametrize('power, volt', 
                            [
                            ('VBL', -1),
                            ('VBL', 0),
                            ('VBL', 16),
                            ('VBL', 100)
                            ])
    def test_VBL_BV(self,power, volt):
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
                            ('ELVDD', -1),
                            ('ELVDD', 0),
                            ('ELVDD', 16), 
                            ('ELVDD', 100)
                            ])
    def test_ELVDD_BV(self,power, volt):
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
                            ('VDD', -1),
                            ('VDD', 0),
                            ('VDD', 16), 
                            ('VDD', 100)
                            ])
    def test_VDD_BV(self,power, volt):
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
                            ('VDDIO', -1),
                            ('VDDIO', 0),
                            ('VDDIO', 16), 
                            ('VDDIO', 100)
                            ])
    def test_VDDIO_BV(self,power, volt):
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
                            ('TPVDD', -1),
                            ('TPVDD', 0),
                            ('TPVDD', 16), 
                            ('TPVDD', 100)
                            ])
    def test_TPVDD_BV(self,power, volt):
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
                            ('TPVDDIO', -1),
                            ('TPVDDIO', 0),
                            ('TPVDDIO', 16), 
                            ('TPVDDIO', 100)
                            ])
    def test_TPVDDIO_BV(self,power, volt):
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
                            ('VGH', -1),
                            ('VGH', 0),
                            ('VGH', 25), 
                            ('VGH', 100)
                            ])
    def test_VGH_BV(self,power, volt):
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
                            ('ELVSS', 1),
                            ('ELVSS', 0),
                            ('ELVSS', -16), 
                            ('ELVSS', -100)
                            ])
    def test_ELVSS_BV(self,power, volt):
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
                            ('VGL', 1),
                            ('VGL', 0),
                            ('VGL', -25), 
                            ('VGL', -100)
                            ])
    def test_VGL_BV(self,power, volt):
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
    #pytest.main(["-s", "test_ThorB.py"])

    i = -2
    print (-i)
    