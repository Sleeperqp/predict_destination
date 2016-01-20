import geohash as gh
import json
from src.data_deal.readAll import read_csvfile


def latlon2grid(filepath, outpath="../../data/grid_trip.csv"):
    rowlist = ["TRIP_ID", "POLYLINE"]
    datas = read_csvfile(filepath, rowlist)
    output = open(outpath, "w")
    codes = {}
    for idx, row in datas.iterrows():
        line = json.loads(row["POLYLINE"])
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

        output.write(str(row["TRIP_ID"]) + " | ")
        output.write(json.dumps(trip))
        output.write("\n")

    print "code has ", str(len(codes))


if __name__ == '__main__':
    latlon2grid("../../data/train.csv")
