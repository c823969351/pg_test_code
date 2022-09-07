# -*- coding: UTF-8 -*-

from os import write
import xlwt
import os
import datetime


def excel_writetime(time):
    test = open('切图时间.csv', 'a+', encoding='gbk')
    time = str(time)
    test.write(time)
    test.write("\n")

    test.close

def excel_writevolt(excel_v, v):  #打印表
    test = open('电源测试.xls', 'a+', encoding='gbk')
    time1 = datetime.datetime.now()
    test.write(v + '\t')
    test.write(str(excel_v))
    test.close()


def excel_writecurr(ret_i, excel_a):  #打印电流表
    test = open('电源测试.xls', 'a+', encoding='gbk')
    time2 = datetime.datetime.now()
    if ret_i == 1:
        test.write('channel' + '\t' + 'ELVSS' + '\t' + 'ELVDD' + '\t' + 'VBL' +
                   '\t' + 'TPVDDIO' + '\t' + 'VDDIO' + '\t' + 'TPVDD' + '\t' +
                   'VDD' + '\t' + 'VGH' + '\t' + 'VGL'+ '\t' + str(time2))
        test.write("\n")

    #excel写入电流值
    test.write('电流' + str(ret_i) + '\t')
    for i in range(0, len(excel_a)):
        if i + 1 == len(excel_a):
            test.write(str(excel_a[i]))
        else:
            test.write(str(excel_a[i]))
            test.write('\t')
    if i == ret_i - 2:  #最后一行后换行
        test.write('\n')

    test.close()


if __name__ == "__main__":
    data = b'MegaRobot Technologies,ThorPG'
    
    if data == b'MegaRobot Technologies,ThorPG':
        print(1)

    else:
        print(2)
