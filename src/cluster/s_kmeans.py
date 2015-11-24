#coding=utf-8
__author__ = 'sleeper'

from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth

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

    f = open("../data/des.csv", "w")
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
    datas = read_csvfile(filepath)
    datas = np.array(datas)
    #print datas.shape

    tor = KMeans(random_state=170)

    tor.fit(datas)

    #print tor.labels_
    draw_kmeans(tor, datas)

def s_meanshif(filepath):
    datas = read_csvfile(filepath)
    datas = np.array(datas)
    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(datas, quantile=0.2, n_samples=100000)
    print bandwidth
    bandwidth = 0.005
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, min_bin_freq=5)
    ms.fit(datas)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    print 'cluster num:',n_clusters_, labels_unique
    geo_data = {'lat':[],'lon':[]}
    for xy in cluster_centers:
        x, y = xy[0],xy[1]
        geo_data['lon'].append(x)
        geo_data['lat'].append(y)

    #print geo_data
    geoplotlib.dot(geo_data)
    #geoplotlib.show()

    print("number of estimated clusters : %d" % n_clusters_)


def draw_geo():
    data = geoplotlib.utils.read_csv('../data/des.csv')
    geoplotlib.add_layer(KMeansLayer(data))
    geoplotlib.set_smoothing(True)
    geoplotlib.show()


if __name__=="__main__":
    #datas = read_csvfile("../data/train.csv")
    #draw_geo()
    #s_kmeans("../data/train.csv")
    s_meanshif("../data/train.csv")