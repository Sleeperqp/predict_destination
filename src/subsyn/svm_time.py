# coding=utf-8
from sklearn import svm
from sklearn.externals import joblib
import geohash as gh
import random


def class_by_time(svm_data, grid_2_id):
    print 'svm'
    trips = []
    labels = []
    for datas in svm_data:
        trip = datas[0]
        time = datas[1]
        data = []
        # 时间特征
        for i in time:
            data.append(int(i))

        p = random.randint(40, 70)

        (lat1, lon1, lat_length, lon_length) = gh._decode_c2i(trip[0])
        (lat2, lon2, lat_length, lon_length) = gh._decode_c2i(trip[int(len(trip) * float(p) / 100.0)])
        data.append(lat1)
        data.append(lon1)
        data.append(lat2)
        data.append(lon2)

        print data
        trips.append(data)
        labels.append(grid_2_id[trip[-1]])
    # print len(trips)
    # print trips

    lin_clf = svm.LinearSVC()
    lin_clf.fit(trips, labels)

    joblib.dump(lin_clf, "../../data/lin_clf.model")
    print 'finish svm'
    return lin_clf


def predict_by_svm(modelpath="../../data/lin_clf.model", data=[[2, 1, 3, 5, 4, 2, 1, 0]]):
    print data
    lin_clf = joblib.load(modelpath)
    print lin_clf.intercept_
    print lin_clf.decision_function(data)
    return lin_clf.predict(data)


if __name__ == "__main__":
    predict_by_svm()
