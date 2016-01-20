# coding=utf-8
import numpy as np
import geohash as gh
import json
import random
from collections import defaultdict


def total_M(inputpath="../../data/grid_trip.csv"):
    input = open(inputpath)
    grid_2_id = {}
    id_2_grid = {}
    M = np.zeros((1568, 1568))

    des = defaultdict(int)
    des_num = 0

    test_data = []
    trip_data = []
    test_num = 0

    max_len = 0
    id = 0
    for line in input:
        line = line.split("|")
        datas = json.loads(line[1])
        if test_num < 1000 and random.randint(1, 100) > 80:
            test_data.append(datas)
            test_num += 1
            continue
        # print datas

        trip_data.append(datas)
        # 计算转移矩阵
        pre = -1
        for data in datas:
            if grid_2_id.has_key(data) == False:
                grid_2_id[data] = id
                id_2_grid[id] = data
                id += 1
            now = grid_2_id[data]
            if pre == -1:
                pass
            else:
                M[pre, now] += 1
            pre = now
        # 统计最长的轨迹
        des_num += 1
        if max_len < len(datas):
            max_len = len(datas)
        # 计算以块为终点的个数
        des[pre] += 1

    print max_len

    M = M / 1184208
    print np.max(M), np.min(M)

    ans = -1.0
    for i in des:
        des[i] = des[i] * 1.0 / des_num
        if ans < des[i]:
            ans = des[i]
    print ans, ans * des_num

    return M, grid_2_id, id_2_grid, test_data, trip_data


def compute_A(M):
    A = []
    Mpow = M
    A.append(M)
    # print np.max(A[0])

    for i in range(1, 120):
        # print i
        Mpow = Mpow * M
        # print i-1,np.max(A[i-1])
        A.append(A[i - 1] + Mpow)

    # print len(A)
    return A


def compute_MT(A, M, grid_2_id, id_2_grid):
    MT = np.zeros((1568, 1568))
    sortlist = defaultdict(list)

    for i in id_2_grid:
        for j in id_2_grid:
            if i != j:
                x = id_2_grid[i]
                y = id_2_grid[j]
                (lat1, lon1, lat_length, lon_length) = gh._decode_c2i(x)
                (lat2, lon2, lat_length, lon_length) = gh._decode_c2i(y)
                sortlist[(abs(lat1 - lat2) + abs(lon1 - lon2))].append([i, j])

    Mpow = M
    for i in sortlist:
        try:
            Mpow = Mpow * M
            print  i, np.max(Mpow)
            Lde = int(i * 0.2)
            Mtemp = Mpow * A[Lde]
            for x in sortlist[i]:
                MT[x[0], x[1]] = Mtemp[x[0], x[1]]
        except:
            print Lde
    print np.max(MT), np.unravel_index(MT.argmax(), MT.shape)

    return MT


def ZMDB():
    print 'ZMD'


def subsyn():
    print 'subsyn'


def test(test_data):
    print len(test_data)


if __name__ == "__main__":
    M, grid_2_id, id_2_grid, test_data, trip_data = total_M()
    A = compute_A(M)
    MT = compute_MT(A, M, grid_2_id, id_2_grid)
    # test(test_data)
    # datas = ['ez3f5', 'ez3fj', 'ez3cu', 'ez3cg', 'ez3cv', 'ez3fk', 'ez3f7', 'ez3fm', 'ez3fh']
    # for i in datas:
    #     (lat,lon,lat_length,lon_length) = gh._decode_c2i(i)
    #     print lat,lon,"\n"
    #
    # print gh.expand("ez3fh")
