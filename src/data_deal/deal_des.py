#coding=utf-8
from src.data_deal.readAll import read_csvfile
import json

#读取csv文件,将文本中的目的地提取出来
#并写入文件outpath,以及返回list数组 形式如[[x1,y1],[x2,y2]...]
def deal_des(filepath, outpath="../../data/des.csv"):
    rowlist =['TRIP_ID','POLYLINE']
    datas = read_csvfile(filepath, rowlist)
    out = open(outpath, "w")

    trip = []
    for line in datas['POLYLINE']:
        tmplist = json.loads(line)
        #print tmplist[-1]
        try:
            if tmplist:
                x, y = tmplist[-1][0], tmplist[-1][1]
                out.write(str(x)+","+str(y)+"\n")
                trip.append(tmplist[-1])
        except IndexError:
            print tmplist
    print len(trip)
    return trip

if __name__=='__main__':
    deal_des("../../data/test.csv")