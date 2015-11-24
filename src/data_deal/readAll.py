#coding=utf-8
import json
import pandas as pd


#一次性读取所有数据
#filepath 表示读取的文本路径
#输出文本的大小并返回读取的csv文本
def read_csvfile(filepath, rowlist):
    try:
        print rowlist
        datas = pd.read_csv(filepath, header=0, usecols=rowlist)
        print datas.shape
        return datas
    except:
        print 'error rowlist:',rowlist
