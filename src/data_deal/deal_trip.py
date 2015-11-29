#coding=utf-8
from src.data_deal.readAll import read_csvfile
import json
import time
#读取csv文件,将文本中路径信息切分并形成MLP所需的数据格式
#并写入文件outpath,以及返回list数组：格式如下：
#  [
#      [
#             trip_id
#             call_type
#             taxi_id
#             [
#                 month
#                 day
#                 week
#                 hourandminute
#             ]
#             [
#                 10个轨迹点
#             ]
#             label
#         ]
#         ...
#     ]


def deal_trip(filepath, outpath="../../data/train_trip.csv"):
    rowlist =["TRIP_ID","CALL_TYPE","TAXI_ID","TIMESTAMP","POLYLINE"]
    datas = read_csvfile(filepath, rowlist)

    label_file = open("../../data/label_des.csv","r")
    out = open(outpath, "w")

    i = 0
    trip_id, label = get_label(label_file.readline())
    trip_id = int(trip_id)
    for idx, row in datas.iterrows():

        line = json.loads(row['POLYLINE'])
        try:
            lenght = len(line)
            if lenght < 10:
                continue
            else:
                if lenght < 34:
                    data = trip_unit(row)
                    data.append(line[0:5]+line[-5:])
                    while row['TRIP_ID'] != trip_id:
                        trip_id, label = get_label(label_file.readline())
                        trip_id = int(trip_id)
                    data.append(label)
                    out.write(json.dumps(data)+"\n")

                if 34 < lenght:
                    data = trip_unit(row)
                    data.append(line[0:5]+line[int(lenght*0.3)-5:int(lenght*0.3)])
                    while row['TRIP_ID'] != trip_id:
                        trip_id, label = get_label(label_file.readline())
                        trip_id = int(trip_id)
                    data.append(label)
                    out.write(json.dumps(data)+"\n")

                if 70 < lenght:
                    data = trip_unit(row)
                    data.append(line[0:5]+line[int(lenght*0.6)-5:int(lenght*0.6)])
                    while row['TRIP_ID'] != trip_id:
                        trip_id, label = get_label(label_file.readline())
                        trip_id = int(trip_id)
                    data.append(label)
                    out.write(json.dumps(data)+"\n")

                if 100 < lenght:
                    data = trip_unit(row)
                    data.append(line[0:5]+line[int(lenght*0.8)-5:int(lenght*0.8)])
                    while row['TRIP_ID'] != trip_id:
                        trip_id, label = get_label(label_file.readline())
                        trip_id = int(trip_id)
                    data.append(label)
                    out.write(json.dumps(data)+"\n")

                if i % 1000 == 999:
                    out.flush()
                    i = 0
                i += 1
        except :
            print 'error line:', line,  trip_id


def trip_unit(row):
    data = []
    data.append(row['TRIP_ID'])
    data.append(row['CALL_TYPE'])
    data.append(row['TAXI_ID'])
    line = row['TIMESTAMP']
    try:
        if line:
            mdhm = time.strftime("%m:%d:%H:%M:%U:%w",time.localtime(int(line))).split(":")
            month,day,hour,minute,weeks, week = mdhm[0],mdhm[1],mdhm[2],mdhm[3],mdhm[4],mdhm[5]
            hm = int(hour)*6 + int(minute)/10
            data.append([month,day,week,str(hm)])
    except:
        print 'error line:',line
    return data


def get_label(line):
    data = line.split(" ")
    return data[0], data[1]

if __name__=='__main__':
    deal_trip("../../data/train.csv")