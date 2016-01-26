import geohash as gh
import json
import time
from src.data_deal.readAll import read_csvfile


def latlon2grid(filepath, outpath="../../data/grid_trip.csv"):
    rowlist = ["TRIP_ID", "POLYLINE", "TIMESTAMP"]
    datas = read_csvfile(filepath, rowlist)
    output = open(outpath, "w")
    codes = {}
    for idx, row in datas.iterrows():
        line = json.loads(row["POLYLINE"])
        trip_time = row["TIMESTAMP"]
        # print idx, row["TRIP_ID"], line
        trip = []
        pre = ""
        for point in line:
            code = gh.encode(point[1], point[0], precision=5)
            # print code
            if codes.has_key(code) == False:
                codes[code] = 1
            if pre != code:
                pre = code
                trip.append(code)

        if len(trip) < 2:
            continue
        data = []
        if trip_time:
            mdhm = time.strftime("%m:%d:%H:%M:%U:%w", time.localtime(int(trip_time))).split(":")
            month, day, hour, minute, weeks, week = mdhm[0], mdhm[1], mdhm[2], mdhm[3], mdhm[4], mdhm[5]
            # print month,day,hour,minute,weeks,week
            hm = int(hour) * 6 + int(minute) / 10
            # print hm
            data = [month, day, week, str(hm)]

        output.write(str(row["TRIP_ID"]) + " | ")
        output.write(json.dumps(trip))
        output.write("|" + json.dumps(data))
        output.write("\n")

    print "code has ", str(len(codes))


if __name__ == '__main__':
    latlon2grid("../../data/train.csv")
