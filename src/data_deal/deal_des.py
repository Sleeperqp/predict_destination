#coding=utf-8
from src.data_deal.readAll import read_csvfile
import json

#读取csv文件,将文本中的目的地提取出来
#并写入文件outpath,以及返回list数组 形式如[
#                                       [[trip_id1],[x1,y1]],
#                                       [[trip_id2],[x2,y2]...
#                                       ]
def deal_des(filepath, outpath="../../data/des.csv"):
    rowlist =['TRIP_ID','POLYLINE']
    datas = read_csvfile(filepath, rowlist)
    out = open(outpath, "w")

    trip = []
    i = 0
    blank = 0
    errornum = 0
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
            else:
                blank += 1
        except :
            print tmplist
            errornum += 1

        i += 1
    print "blank:",blank,"valid:",len(trip),"error:",errornum
    return trip

if __name__=='__main__':
    deal_des("../../data/train.csv")