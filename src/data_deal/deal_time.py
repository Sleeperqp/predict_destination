#coding=utf-8

from src.data_deal.readAll import read_csvfile
import time

def deal_time2we(filepath):
    rowlist = ['TRIP_ID','TIMESTAMP']
    datas = read_csvfile(filepath, rowlist)
    print datas
    trip = []
    first = 1
    for line in datas['TIMESTAMP']:
        try:
            if line:
                mdhm = time.strftime("%m:%d:%H:%M:%U:%w",time.localtime(int(line))).split(":")
                month,day,hour,minute,weeks, week = mdhm[0],mdhm[1],mdhm[2],mdhm[3],mdhm[4],mdhm[5]
                print month,day,hour,minute,weeks,week
        except:
            print 'error line:',line


if __name__=='__main__':
    deal_time2we("../../data/test.csv")