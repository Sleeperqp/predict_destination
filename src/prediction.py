#coding=utf-8

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SoftmaxLayer


net = buildNetwork(2, 3, 2, bias=True, outclass=SoftmaxLayer)