import matplotlib
import argparse
import math
import numpy
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from numpy import array, zeros, argmin, inf, equal, ndim
from get_DTW_distance import get_DTW_distance
from models import isOneOfThreeModels

source_file = '/mnt/cephfs/lab/gaosiyi/stock/dataset/rowData.csv'
info_file = '/mnt/cephfs/lab/gaosiyi/stock/dataset/codes_info.csv'


class Dimensionality_reduction(object):
    
    def __init__(self, code, date, high, volumn):
        self.code = code
        self.date = date
        self.high = high
        self.volumn = volumn

    def compute_by_apca(self, y_ori):
        flag = 0.5
        S = y_ori
        left = 0
        right = 1
        c_error = 0
        c_sum = S[0]
        v_list = []
        tr_list = []
        for i,s in enumerate(S[1:]):
            c_sum = c_sum + s
            c_avg = c_sum/(right-left+1)
            c_error = c_error + (abs(s - c_avg))
            if c_error > flag:
                v_list.append(c_avg)
                tr_list.append(i)
                left = right + 1
                right = left
                c_error = 0
                c_sum = s 
            right = right + 1
        return tr_list,v_list

    def extreme_point(self,x,y):
        y_list = []
        i_list = []
        length = len(y)
        for i,yi in enumerate(y):
            if i>1 and i<length-1:
                if  yi>y[i-1] and yi >y[i+1]:
                    y_list.append(yi)
                    i_list.append(x[i])
                elif yi<y[i-1] and yi <y[i+1]:
                    y_list.append(yi)
                    i_list.append(x[i])
                else:
                    continue
        return i_list,y_list

    def important_point(self,x,y):
        y_list = []
        i_list = []
        length = len(y)
        R1 = 1.1
        R2 = 1.4
        pi = 3.1415
        for i,yi in enumerate(y):
            if i>1 and i<length-1:
                y1 = y[i-1]
                y2 = y[i+1]
                x1 = x[i-1]
                x2 = x[i+1]
                if  float(yi)/float(y[i-1]) > R1 or  float(yi)/float(y[i+1]) > R1:
                    if float(yi)/float(y[i-1]) > R2 or  float(yi)/float(y[i+1]) > R2:
                        y_list.append(yi)
                        i_list.append(x[i])
                    else:
                        angle1 = abs(yi-y1)/abs(x[i]-x1)
                        angle2 = abs(yi-y2)/abs(x[i]-x2)
                        l = angle1 + angle2
                        if l < 1.5:
                            y_list.append(yi)
                            i_list.append(x[i])
                        else:
                            pass
                elif float(y[i-1])/float(yi) > R1 or  float(y[i+1])/float(yi) > R1:
                    if float(y[i-1])/float(yi) > R2 or  float(y[i+1])/float(yi) > R2:
                        y_list.append(yi)
                        i_list.append(x[i])
                    else:
                        angle1 = abs(yi-y1)/abs(x[i]-x1)
                        angle2 = abs(yi-y2)/abs(x[i]-x2)
                        l = angle1 + angle2
                        if l < 1.5:
                            y_list.append(yi)
                            i_list.append(x[i])
                        else:
                            pass
        return i_list,y_list 

    def cut_small_angle(point_list):
        pi = 3.1415
        point_result = []
        for i in range(1,len(point_list)-1):
            y = point_list[i][1]
            x = point_list[i][0]
            y1 = point_list[i-1][1]
            x1 = point_list[i-1][0]
            y2 = point_list[i+1][1]
            x2 = point_list[i+1][0]
            angle1 = abs(y-y1)/abs(x-x1)
            angle2 = abs(y-y2)/abs(x-x2)
            l = angle1 + angle2
            if l <2:
                point_result.append(point_list[i])
            else:
                pass
        return point_result

    def show_result(y_ori,y_apca,y_extreme,y_important):
        plt.figure(facecolor = 'white')
        y_ori.plot(color = 'blue' , label = 'Original')
        y_apca.plot(color = 'red', label = 'Apca')
        y_extreme.plot(color = 'orange', label = 'Extreme')
        y_impoer.plot(color = 'green', label = 'Important')
        plt.legend(loc='best')
        plt.title('dimensionality_reduction')
        plt.savefig("dimensionality_reduction.png")


    def dimensionality_reshape(code = self.code,date = self.code,high = self.high,volume = self.volume):
        x_apca, y_apca = compute_by_apca(high)
        x_extreme,y_extreme = extreme_point(x_apca, y_apca)
        x_important,y_important = important_point(x_extreme, y_extreme)
        show_result(high,y_apca,y_extreme,y_important)
        '''
        x_new_1,y_new_1 = important_point(x_new,y_new)
        result = []
        for i in range(len(x_new_1)):
            result.append((x_new_1[i],y_new_1[i]))
        result_list = cut_small_angle(result)
        x_new_2 = []
        y_new_2 = []
        date_2 = []
        volume_2 = []
        for j in range(len(result_list)):
            x_new_2.append(result_list[j][0])
            date_2.append(date[result_list[j][0]])
            volume_2.append(volume[result_list[j][0]])
            y_new_2.append(result_list[j][1])
        '''
        #return x_new_2,y_new_2,date_2,volume_2
        return x_important, y_important

