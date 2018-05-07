import matplotlib
import argparse
import math
import numpy
from numpy import array, zeros, argmin, inf, equal, ndim
from scipy.spatial.distance import cdist

def dist(p1,p2):
    return  math.sqrt(sum([pow(abs(p1[0]-p2[0]),2),pow(abs(p1[1]-p2[1]),2)]))

class DTWDistance(object):

    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2


    def get_DTW_distance(self):
        list1 = self.list1
        list2 = self.list2
        r,c = len(list1),len(list2)
        print r,c
        D0 = zeros((r+1,c+1))
        #D0 input array ; D1 output array
        D0[0,1:] = inf
        D0[1:,0] = inf
        D1 = D0[1:,1:]
        for i in range(r):
            for j in range(c):
                D1[i,j] = dist(list1[i],list2[j])
        C = D1.copy()
        for i in range(r):
            for j in range(c):
                D1[i, j] += min(D0[i, j], D0[i, j+1], D0[i+1, j])
        if len(list1)==1:
            path = zeros(len(list2)), range(len(list2))
        elif len(list2) == 1:
            path = range(len(list1)), zeros(len(list1))
        else:
            path = _traceback(D0)
        return D1[-1, -1] / sum(D1.shape), C, D1, path

    def _traceback(self, D):
        i, j = array(D.shape) - 2
        p, q = [i], [j]
        while ((i > 0) or (j > 0)):
            tb = argmin((D[i, j], D[i, j+1], D[i+1, j])) #return index of the min number
            if (tb == 0):
                i -= 1
                j -= 1
            elif (tb == 1):
                i -= 1
            else: # (tb == 2):
                j -= 1
            p.insert(0, i)
            q.insert(0, j)
        return array(p), array(q)

    def draw_picture(self):
        list1 = self.list1
        list2 = self.list2
        plt.figure()
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        for i in range(len(list1)):
            x1.append(list1[i][0])
            y1.append(list1[i][1])
        for j in range(len(list2)):
            x2.append(list2[j][0])
            y2.append(list2[j][1])
        plt.plot(x1,y1,color='g')
        plt.plot(x2,y2,color='y')
        print y1,y2
        plt.savefig("dtw.png")
