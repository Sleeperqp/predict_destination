#coding=utf-8

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SoftmaxLayer
from pybrain.datasets.classification import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities import percentError
import json

def import_data(train_file_path='../data/train_trip.csv'):
    dataset = ClassificationDataSet(26, 1, nb_classes=3456, class_labels='class')
    train_file = open(train_file_path, "r")

    for line in train_file:
        try:
            datas = json.loads(line)
            data = []
            #CALL_TYPE:         1
            data.append(datas[2])
            #TAXI_ID:           1
            data.append(ord(datas[1].lower()) - ord('a'))
            #time embedding:    4
            for i in datas[3]:
                data.append(int(i))
            #trip:  10*2 =     20
            for i in datas[4]:
                data.append(i[0])
                data.append(i[1])
            dataset.addSample(data, [int(datas[5])])
        except:
            print 'error line:', line
    return dataset


def mlp():
    mlp = buildNetwork(26, 500, 3456, bias=True, outclass=SoftmaxLayer)
    #print net['in'], net['hidden0'],  net['out']
    ds = import_data()
    trndata, tstdata = ds.splitWithProportion(0.8)
    trndata._convertToOneOfMany()
    tstdata._convertToOneOfMany()


    print "Number of training patterns: ", len(trndata)
    print "Input and output dimensions: ", trndata.indim, trndata.outdim
    print "First sample (input, target, class):"
    print trndata['input'][0], trndata['target'][0], trndata['class'][0]


    trainer = BackpropTrainer(mlp, trndata, verbose = True, learningrate=0.01)
    trainer.trainUntilConvergence(maxEpochs=1000)

    trnresult = percentError( trainer.testOnClassData(),
                              trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )

    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult

if __name__=='__main__':
    mlp()