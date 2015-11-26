#coding=utf-8
from src.data_deal.readAll import read_csvfile
import json

#读取csv文件,将文本中的目的地提取出来
#并写入文件outpath,以及返回list数组 形式如[
#                                       [[trip_id1],[x1,y1]],
#                                       [[trip_id2],[x2,y2]...
#                                       ]
def deal_trip(filepath, outpath="../../data/train_trip.csv"):
    rowlist =['TRIP_ID','POLYLINE']
    datas = read_csvfile(filepath, rowlist)
    out = open(outpath, "w")

    #trip = []
    i = 0
    for line in datas['POLYLINE']:
        line = json.loads(line)
        try:
            lenght = len(line)
            if lenght < 10:
                continue
            else:
                if lenght < 34:
                    data = []
                    data.append([datas['TRIP_ID'][i]])
                    data.append(line[0:5]+line[-5:])
                    #print data
                    #trip.append(data)
                    out.write(json.dumps(data)+"\n")
                if 34 < lenght:
                    data = []
                    data.append([datas['TRIP_ID'][i]])
                    data.append(line[0:5]+line[int(lenght*0.3)-5:int(lenght*0.3)])
                    #print data
                    #trip.append(data)
                    out.write(json.dumps(data)+"\n")
                if 70 < lenght:
                    data = []
                    data.append([datas['TRIP_ID'][i]])
                    data.append(line[0:5]+line[int(lenght*0.6)-5:int(lenght*0.6)])
                    #print data
                    #trip.append(data)
                    out.write(json.dumps(data)+"\n")
                if 100 < lenght:
                    data = []
                    data.append([datas['TRIP_ID'][i]])
                    data.append(line[0:5]+line[int(lenght*0.8)-5:int(lenght*0.8)])
                    #print data
                    #trip.append(data)
                    out.write(json.dumps(data)+"\n")

        except :
            print line
        i += 1
    #print len(trip)
    #return trip

if __name__=='__main__':
    deal_trip("../../data/train.csv")