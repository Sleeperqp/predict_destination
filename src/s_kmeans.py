#coding=utf-8
__author__ = 'sleeper'

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import geoplotlib

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

def draw_geo():
    thedata = geoplotlib.utils.read_csv('../data/des.csv')
    geoplotlib.dot(thedata)
    geoplotlib.show()


if __name__=="__main__":
    #datas = read_csvfile("../data/train.csv")
    draw_geo()
    #s_kmeans("../data/train.csv")