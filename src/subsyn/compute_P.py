# coding=utf-8
import numpy as np
import geohash as gh
import json
import random
import sys
import gnumpy as gnp
from collections import defaultdict


def total_M(inputpath="../../data/grid_trip.csv"):
    input = open(inputpath)
    grid_2_id = {}
    id_2_grid = {}
    M = np.zeros((1568, 1568))
    i_in_Trip = defaultdict(int)
    des = defaultdict(int)
    des_num = 0

    test_data = []
    test_des = []
    trip_data = []
    test_num = 0

    max_len = 0
    id = 0
    for line in input:
        line = line.split("|")
        datas = json.loads(line[1])
        if test_num < 1000 and random.randint(1, 100) > 70 and len(datas) > 4:
            for data in datas:
                if grid_2_id.has_key(data) == False:
                    grid_2_id[data] = id
                    id_2_grid[id] = data
                    id += 1
            test_data.append(datas)
            test_des.append(grid_2_id[datas[-1]])
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
            i_in_Trip[grid_2_id[data]] += 1
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

    # 计算p_(ij)
    for i in range(0, 1568):
        if i_in_Trip[i] == 0:
            continue
        for j in range(0, 1568):
            try:
                M[i, j] = M[i, j] / i_in_Trip[i]
            except:
                print M[i, j], i_in_Trip[i]
    print np.max(M), np.min(M)

    #计算P(d \in n^j)
    ans = -1.0
    for i in des:
        des[i] = des[i] * 1.0 / des_num
        if ans < des[i]:
            ans = des[i]
    #print ans, ans * des_num

    return M, grid_2_id, id_2_grid, test_data, trip_data, test_des, des


def compute_A(M):
    print 'computing A'
    A = []
    Mpow = gnp.garray(M)
    A.append(gnp.garray(np.eye(1568)))
    # print np.max(A[0])

    for i in range(1, 120):
        # print i
        Mpow = Mpow.dot(M)
        #print i-1,np.max(np.array(A[i-1]))
        A.append(A[i - 1] + Mpow)
        #print A[i]
    # print len(A)
    return A


def compute_MT(A, M, grid_2_id, id_2_grid):
    print 'computing MT'
    MT = np.zeros((1568, 1568))
    sortlist = defaultdict(list)

    for i in id_2_grid:
        for j in id_2_grid:
            if i == j:
                continue
            x = id_2_grid[i]
            y = id_2_grid[j]
            (lat1, lon1, lat_length, lon_length) = gh._decode_c2i(x)
            (lat2, lon2, lat_length, lon_length) = gh._decode_c2i(y)
            sortlist[(abs(lat1 - lat2) + abs(lon1 - lon2))].append([i, j])

    # Mpow = np.eye(1568)
    Mpow = gnp.garray(np.eye(1568))
    M = gnp.garray(M)
    #print Mpow
    for i in sortlist:
        # print  i
        Mpow = Mpow.dot(M)
        Lde = int(i * 0.2)
        Mtemp = Mpow.dot(A[Lde])
        # np.dot(Mpow, A[Lde])
        # print 'finish'
        # print Mtemp
        for x in sortlist[i]:
            MT[x[0], x[1]] = Mtemp[x[0], x[1]]

    # print np.max(MT), np.unravel_index(MT.argmax(), MT.shape)
    #print MT
    return MT


def testINtrip(testdata, tripdata):
    if len(testdata) > len(tripdata):
        return 0

    for idx in range(0, len(tripdata)):
        i = idx
        for j in range(0, len(testdata)):
            if i < len(tripdata) and tripdata[i] != testdata[j]:
                break
            i += 1
        if i - idx == len(testdata):
            return 1
    return 0


def ZMDB(test_data, trip_data, test_des, id_2_grid):
    print 'ZMDB'
    # print test_des
    total_error = []
    total_km = 0
    try:
        idx = 0
        for data in test_data:
            des_num = defaultdict(int)
            num = 0
            # 计算  每个查询轨迹:满足目的地为n^j 且 查询轨迹匹配trip_data的数目:des_num 总的匹配轨迹为num
            for trip in trip_data:
                tmp = testINtrip(data, trip)
                num += tmp
                des_num[trip[-1]] += tmp

            if num <= 0:
                idx += 1
                continue
            # print num
            max_P = -1
            max_ID = -1
            # 对每个目的地而言, P(n^j | T^end(np.eye(1568))p)
            P = defaultdict(float)
            for i in des_num:
                P[i] = des_num[i] * 1.0 / num
                if max_P < P[i]:
                    max_P = P[i]
                    max_ID = i

            P = sorted(P.iteritems(), key=lambda (k, v): (v, k), reverse=True)
            Q = []
            for k, v in P:
                Q.append(int(k))

            # 计算涵盖率
            yes_list = []
            # print test_des[idx], Q[:5]
            if test_des[idx] in Q[:1]:
                yes_list.append(1)
            else:
                yes_list.append(0)

            if test_des[idx] in Q[:3]:
                yes_list.append(1)
            else:
                yes_list.append(0)

            if test_des[idx] in Q[:5]:
                yes_list.append(1)
            else:
                yes_list.append(0)
            # print data, max_ID, max_P, test_des[idx]
            total_error.append(yes_list)
            # 计算误差曼哈顿距离
            # print test_des[idx]
            # print id_2_grid[int(test_des[idx])]
            (lat1, lon1, lat_length, lon_length) = gh._decode_c2i(id_2_grid[int(test_des[idx])])
            (lat2, lon2, lat_length, lon_length) = gh._decode_c2i(id_2_grid[Q[0]])
            total_km += abs(lat1 - lat2) + abs(lon1 - lon2)
            idx += 1
    except:
        # print test_des[idx], Q[0]
        s = sys.exc_info()
        print "Error '%s' happened on line %d" % (s[1], s[2].tb_lineno)
    P1 = P3 = P5 = 0.0
    for data in total_error:
        P1 += data[0]
        P3 += data[1]
        P5 += data[2]
    print P1, P3, P5
    print P1 / len(test_des), P3 / len(test_des), P5 / len(test_des)
    print total_km * 1.0 / len(test_des)


def subsyn(test_data, trip_data, test_des, M, MT, des):
    print 'subsyn'

    idx = 0
    total_error = []
    total_km = 0
    for datas in test_data:
        # 计算P(Tp)
        # Ptp = 100000000
        # pre = -1
        # for point in datas:
        #     if pre < 0:
        #         pre = point
        #         continue
        #     Ptp = Ptp * M[pre, point]
        #
        # 计算P(T^p|d \in n_j)
        Ptpnj = defaultdict(float)
        for j in des:
            if MT[datas[0], j] <= 0:
                continue
            try:
                Ptpnj[j] = MT[datas[-1], j] / MT[datas[0], j]
            except:
                print ''

        P = defaultdict(float)
        sum = 0.0
        for j in Ptpnj:
            P[j] = Ptpnj[j] * des[j]
            sum += P[j]

        P = sorted(P.iteritems(), key=lambda (k, v): (v, k), reverse=True)
        Q = []
        for k, v in P:
            Q.append(int(k))

        # print test_des[idx], Q[:5]
        # 计算涵盖率
        yes_list = []
        # print test_des[idx], Q[:5]
        if test_des[idx] in Q[:1]:
            yes_list.append(1)
        else:
            yes_list.append(0)

        if test_des[idx] in Q[:3]:
            yes_list.append(1)
        else:
            yes_list.append(0)

        if test_des[idx] in Q[:5]:
            yes_list.append(1)
        else:
            yes_list.append(0)
        # print data, max_ID, max_P, test_des[idx]
        total_error.append(yes_list)
        # 计算误差曼哈顿距离
        # print id_2_grid[int(test_des[idx])]
        (lat1, lon1, lat_length, lon_length) = gh._decode_c2i(id_2_grid[int(test_des[idx])])
        (lat2, lon2, lat_length, lon_length) = gh._decode_c2i(id_2_grid[Q[0]])
        total_km += abs(lat1 - lat2) + abs(lon1 - lon2)
        idx += 1

    P1 = P3 = P5 = 0.0
    for data in total_error:
        P1 += data[0]
        P3 += data[1]
        P5 += data[2]
    print P1, P3, P5
    print P1 / len(test_des), P3 / len(test_des), P5 / len(test_des)
    print total_km * 1.0 / len(test_des)


def geohash2id(datas, isTest=False):
    test = []
    for data in datas:
        p = random.randint(40, 70)
        data_tmp = []
        if isTest == True:
            data = data[:int(len(data) * float(p) / 100.0)]
        for i in data:
            data_tmp.append(grid_2_id[i])
        test.append(data_tmp)
    return test


def test(test_data, trip_data, grid_2_id, test_des, id_2_grid, M, MT, des):
    # print len(test_data)
    # print len(trip_data)

    test_data = geohash2id(test_data, True)
    trip_data = geohash2id(trip_data)

    # test ZMDB
    # ZMDB([[1,2]],[[1,2,3],[2,1]])
    ZMDB(test_data, trip_data, test_des, id_2_grid)
    subsyn(test_data, trip_data, test_des, M, MT, des)


if __name__ == "__main__":
    M, grid_2_id, id_2_grid, test_data, trip_data, test_des, des= total_M()
    A = compute_A(M)
    MT = compute_MT(A, M, grid_2_id, id_2_grid)
    # print test_des
    test(test_data, trip_data, grid_2_id, test_des, id_2_grid, M, MT, des)
    #print testINtrip([1,23,2], [1,23,4,2])
    # datas = ['ez3f5', 'ez3fj', 'ez3cu', 'ez3cg', 'ez3cv', 'ez3fk', 'ez3f7', 'ez3fm', 'ez3fh']
    # for i in datas:
    #     (lat,lon,lat_length,lon_length) = gh._decode_c2i(i)
    #     print lat,lon,"\n"
    #
    # print gh.expand("ez3fh")
