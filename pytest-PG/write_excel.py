# -*- coding: UTF-8 -*-

import datetime
import csv
import pandas

class PG_CSV(object):
    def __init__(self):
        
        pass

def excel_writevolt(ret_ch, ret_v,get_v):  #打印电压表

    with open('电源测试.csv', 'a+') as test:
        time1 = datetime.datetime.now()

        #excel写入电压值
        test.write(ret_ch+','+ str(get_v) + ',' + str(ret_v)+','+str(time1))
        test.write("\n")

def excel_writevolt_TEST(): 

    with open('电源测试.csv', 'a+') as f:
        time1 = datetime.datetime.now()
        csv_write = csv.writer(f)
        data = [',Volt(V),Getvolt(V),Time']
        csv_write.writerow(data)

def TEST(data): 

    with open('空载MIPI2.csv', 'a+') as f:
        f.write(data)
        f.write('\n')



if __name__ == "__main__":
    print('hello')
    excel_writevolt_TEST()