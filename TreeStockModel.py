import numpy as np
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import time
import os

SIM = 2
dest_dir = "/mnt/cephfs/lab/gaosiyi/stocks"

def revert_to_datatime(x):
    x_dt = []
    for xi in x:
        data = time.strptime(xi,"%Y-%m-%d")
        data = time.mktime(data)
        data = data/86400
        x_dt.append(data)
    return x_dt


def isDoublet(x,y,v):
    doublet_list = []
    i = 2
    for i in range(2,len(y)-2):
        if y[i-1]>y[i] and y[i-1]>y[i-2] and y[i+1]>y[i] and y[i+1]>y[i+2] and abs(y[i+1]-y[i-1])<SIM:
            if y[i-2]<y[i] and y[i+2]<y[i]:
                #if y[i]>= 0.1*y[i-1] and y[i]<= 0.2*y[i-1]:
                #    if x[i+2]-x[i-1] > 30 and x[i+2]-x[i-1]<180:
                #        if v[i-1] > v[i+1]:
                doublet_list.append([i-2,i+2,y[i]]) 
    return doublet_list

def isHeadShoulder(x,y,v):
    headshoulder_list = []
    i = 3
    for i in range(3,len(y)-3):
        if y[i]>y[i-1] and y[i]>y[i+1] and y[i-2]>y[i-3] and y[i-2]>y[i-1] and y[i+2]>y[i+1] and y[i+2]>y[i+3] and y[i+2]<y[i] and y[i-2]<y[i]:
            if abs(y[i-1]-y[i+1]) <= SIM and abs(y[i-2]-y[i+2]) <= SIM:
                if y[i-3]<y[i-1] and y[i+3]<y[i-1]:
                   # if y[i+3]-y[i+1]>0.03*y[i+3]:
                   #     if v[i-2] > v[i] and v[i] > v[i+2]:
                    headshoulder_list.append([(i-3),(i+3),[(x[i-1],y[i-1]),(x[i+1],y[i+1])]])
    return headshoulder_list

def isDoubleBottom(x,y,v):
    doublebottom_list = []
    i = 2
    for i in range(2,len(y)-2):
        if y[i]>y[i-1] and y[i]>y[i+1] and y[i-2]>y[i-1] and y[i+2]>y[i+1] and abs(y[i-1]-y[i+1])<SIM:
            #if abs(y[i]-0.11*y[i-1]) <= SIM and abs(y[i-1]-y[i+1]) <= SIM and x[i+1]-x[i-1] >= 30:
            #    if v[i+2] > v[i+1]:
            doublebottom_list.append([i-2,i+2,y[i]])
    return doublebottom_list

def draw_model(rlist,x,y,color):
    if rlist == []:
        pass
    else:
        for r in rlist:
            start = r[0]
            end = r[1]
            plt.plot(x[start:end+1],y[start:end+1],color)

    
def isOneOfThreeModels(code,x_reversed,y_reversed,volume_reversed):
    x_dt = revert_to_datatime(x_reversed)
    plt.figure()
    plt.plot(x_reversed,y_reversed,'b')
    doublet_list = isDoublet(x_dt,y_reversed,volume_reversed)
    draw_model(doublet_list,x_reversed,y_reversed,'r')
    headshoulder_list = isHeadShoulder(x_reversed,y_reversed,volume_reversed)
    draw_model(headshoulder_list,x_reversed,y_reversed,'y')
    doublebottom_list = isDoubleBottom(x_dt,y_reversed,volume_reversed)
    #draw_model(doublebottom_list,x_reversed,y_reversed,'k')
    plt.show()
    plt.savefig(os.path.join(dest_dir,str(code)+".jpg"))
    print doublet_list,headshoulder_list,doublebottom_list

     
