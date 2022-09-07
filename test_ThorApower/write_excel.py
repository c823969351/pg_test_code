# -*- coding: UTF-8 -*-

import datetime
import csv
import os


def excel_writevolt(ret_ch, ret_v,get_v,v,filename):  #打印电压表

    a = filename.split('\\')
    dir = ''
    # print(a)
    for i in range(len(a)):
        if i == len(a)-1:
            dir = dir[:-1]
        else:
            b = a[i]+'\\'
            dir = dir +b
    
    if not os.path.exists(dir):
        os.mkdir(dir)

    with open(filename, 'a+') as test:
        time1 = datetime.datetime.now()

        if get_v == v:
            test.write(ret_ch +',Volt(V),Getvolt(V)')
            test.write("\n")
            test.write(','+ str(get_v) + ',' + str(ret_v))
            test.write("\n")
        else:
            #excel写入电压值
            test.write(','+ str(get_v) + ',' + str(ret_v))
            test.write("\n")

def excel_writevolt_TEST(): 

    with open('电源测试.csv', 'a+') as f:
        time1 = datetime.datetime.now()
        csv_write = csv.writer(f)
        data = [',Volt(V),Getvolt(V),Time']
        csv_write.writerow(data)



if __name__ == "__main__":
    filename = 'D:\\testCode\\test_ThorApower\\电源测试数据\\电源测试20220907-14-46-25.csv'
    excel_writevolt('vdd',2,5,1,filename)