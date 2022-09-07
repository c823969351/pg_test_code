# -*- coding: UTF-8 -*-

import datetime
import csv


class PG_CSV(object):
    def __init__(self):
        
        pass

def Csv_curr(ret_ch, curr):  #打印电压表

    with open('背光电流测试.csv', 'a+') as test:
        time1 = datetime.datetime.now()
        test.write(ret_ch+','+ str(curr) +','+str(time1))
        test.write("\n")

def excel_writevolt_TEST(): 

    with open('电源测试.csv', 'a+') as f:
        time1 = datetime.datetime.now()
        csv_write = csv.writer(f)
        data = [',Volt(V),Getvolt(V),Time']
        csv_write.writerow(data)



if __name__ == "__main__":
    print('hello')
    excel_writevolt_TEST()