#coding=utf-8
__author__ = 'sleeper'

from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth
from src.data_deal.deal_des import deal_des

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from geoplotlib.colors import create_set_cmap
import pyglet
import geoplotlib
from geoplotlib.layers import BaseLayer
from geoplotlib.core import BatchPainter
from geoplotlib.utils import BoundingBox


class KMeansLayer(BaseLayer):

    def __init__(self, data):
        self.data = data


    def invalidate(self, proj):
        self.painter = BatchPainter()
        x, y = proj.lonlat_to_screen(self.data['lon'], self.data['lat'])

        k_means = KMeans()
        k_means.fit(np.vstack([x,y]).T)
        labels = k_means.labels_

        self.cmap = create_set_cmap(set(labels), 'hsv')
        for l in set(labels):
            try:
                self.painter.set_color(self.cmap[l])
                self.painter.convexhull(x[labels == l], y[labels == l])
                self.painter.points(x[labels == l], y[labels == l], 2)
            except Exception:
                print '=============',l,'=============='

    def draw(self, proj, mouse_x, mouse_y, ui_manager):
        self.painter.batch_draw()


    def on_key_release(self, key, modifiers):
        return False

def read_csvfile(filepath):
    datas = pd.read_csv(filepath)

    f = open("../../data/des.csv", "w")
    print datas.shape,type(datas['POLYLINE'])
    trip = []
    for line in datas['POLYLINE']:
        tmplist = json.loads(line)
        #print tmplist[-1]
        try:
            if tmplist:
                x, y = tmplist[-1][0], tmplist[-1][1]
                f.write(str(x)+","+str(y)+"\n")
                trip.append(tmplist[-1])
        except IndexError:
            print tmplist
    #print trip
    return trip

def draw_kmeans(tor,datas):
    x_min, x_max = datas[:, 0].min() , datas[:, 0].max()
    y_min, y_max = datas[:, 1].min() , datas[:, 1].max()
    h = 0.001
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
    Z = tor.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(datas[:, 0], datas[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = tor.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=100, linewidths=1,
                color='w', zorder=1)
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()


def s_kmeans(filepath):
    datas = deal_des(filepath)
    datas = np.array(datas[:,1])
    #print datas.shape

    tor = KMeans(random_state=170)

    tor.fit(datas)

    #print tor.labels_
    draw_kmeans(tor, datas)

def s_meanshif(filepath,labelpath="../../data/label.csv", label_despath="../../data/label_des.csv"):
    #datas = deal_des(filepath)
    #提取目的地坐标
    #des = []
    #for it in datas:
    #    des.append(it[1])

    #从des文件中读取目的地信息
    des = []
    tripid = []
    file = open("../../data/des.csv","r")
    for line in file:
        try:
            if len(line) > 1:
                data = line.strip("\n").split(" ")
                x,y = float(data[1]),float(data[2])
                tripid.append(data[0])
                des.append([x, y])
        except:
            #print line
            pass
    print len(des),len(tripid)
    #将list转换为numpy的矩阵格式
    des = np.array(des)
    # The following bandwidth can be automatically detected using
    #得到meanshift所需的bandwidth
    bandwidth = estimate_bandwidth(des, quantile=0.2, n_samples=100000)
    #print bandwidth
    bandwidth = 0.005
    #得到meanShift模型并进行训练
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, min_bin_freq=5)
    ms.fit(des)

    #得到训练的标签以及类别中心点坐标
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    #存储每个类别对应的中心坐标
    out = open(labelpath,"w")
    i = 0
    ress = []
    for cluster_center in cluster_centers:
        #print cluster_center
        out.write(str(i)+" "+str(cluster_center[0])+" "+str(cluster_center[1])+"\n")
        i += 1
    out.close()

    #存储目的地对应的类别
    label_des = open(label_despath, "w")
    i = 0
    for label in labels:
        #print tripid[i],label
        label_des.write(str(tripid[i])+" "+str(label)+" "+str(cluster_centers[int(label)][0])+" "+str(cluster_centers[int(label)][1])+"\n")
        i += 1

    label_des.close()
    #print ress
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    print 'cluster num:',n_clusters_, labels_unique

    #对聚类效果进行可视化
    geo_data = {'lat':[],'lon':[]}
    for xy in cluster_centers:
        x, y = xy[0],xy[1]
        geo_data['lon'].append(x)
        geo_data['lat'].append(y)

    #print geo_data
    geoplotlib.dot(geo_data)
    geoplotlib.show()


def draw_geo():
    data = geoplotlib.utils.read_csv('../data/des.csv')
    geoplotlib.add_layer(KMeansLayer(data))
    geoplotlib.set_smoothing(True)
    geoplotlib.show()


if __name__=="__main__":
    #datas = read_csvfile("../data/train.csv")
    #draw_geo()
    #s_kmeans("../data/train.csv")
    s_meanshif("../../data/test.csv")