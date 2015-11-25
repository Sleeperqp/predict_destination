#coding=utf-8

from src.data_deal.readAll import read_csvfile
import time
#取得csv文件,将时间戳转换为时间
#然后根据月,日,周几,一天的时间划为144份进行转换为词向量(word embedding)
#将结果存入list中,以 [
#                     [[trip_id1],[month1,day1,week1,str(hm1)]]
#                     [[trip_id2],[month2,day2,week2,str(hm2)]]
#                       ..
#                   ]
#并且将写入outpath路径的文本中
#以 trip_id month day week str(hm)的形式存入
def deal_time2we(filepath, outpath="../../data/time2we.csv"):
    rowlist = ['TRIP_ID','TIMESTAMP']
    datas = read_csvfile(filepath, rowlist)
    out = open(outpath, "w")

    we = []
    i = 0
    for line in datas['TIMESTAMP']:
        data = []
        data.append([datas['TRIP_ID'][i]])
        try:
            if line:
                mdhm = time.strftime("%m:%d:%H:%M:%U:%w",time.localtime(int(line))).split(":")
                month,day,hour,minute,weeks, week = mdhm[0],mdhm[1],mdhm[2],mdhm[3],mdhm[4],mdhm[5]
                #print month,day,hour,minute,weeks,week
                hm = int(hour)*6 + int(minute)/10
                #print hm
                out.write(datas['TRIP_ID'][i]+" "+month+" "+day+" "+week+" "+str(hm)+"\n")
                data.append([month,day,week,str(hm)])
                we.append(data)
        except:
            print 'error line:',line
        i += 1
    print we
    return  we

if __name__=='__main__':
    deal_time2we("../../data/test.csv")