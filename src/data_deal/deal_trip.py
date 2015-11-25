#coding=utf-8
from src.data_deal.readAll import read_csvfile
import json

#读取csv文件,将文本中的目的地提取出来
#并写入文件outpath,以及返回list数组 形式如[
#                                       [[trip_id1],[x1,y1]],
#                                       [[trip_id2],[x2,y2]...
#                                       ]
def deal_trip(filepath, outpath="../../data/des.csv"):
    rowlist =['TRIP_ID','POLYLINE']
    datas = read_csvfile(filepath, rowlist)
    out = open(outpath, "w")

    trip = []
    i = 0
    for line in datas['POLYLINE']:
        data = []
        data.append([datas['TRIP_ID'][i]])
        tmplist = json.loads(line)
        try:
            if tmplist:
                x, y = tmplist[-1][0], tmplist[-1][1]
                out.write(str(datas['TRIP_ID'][i])+" "+str(x)+" "+str(y)+"\n")
                data.append(tmplist[-1])
                trip.append(data)
        except :
            print tmplist
        i += 1
    print len(trip)
    return trip

if __name__=='__main__':
    deal_trip("../../data/train.csv")