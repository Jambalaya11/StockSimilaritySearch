import pandas as pd
from numpy import array, zeros, argmin, inf, equal, ndim
from DimensionalityReduction import Dimensionality_reduction
from GetDTWDistance import DTWDistance
from TreeStockModel import isOneOfThreeModels 

source_file = '/mnt/cephfs/lab/gaosiyi/stock/dataset/rowData.csv'


if __name__ == '__main__':
    data = pd.read_csv(source_file)   #dataFrame
    data = data.values
    date_list = data[:,1]
    high_list = data[:,4]
    volume_list = data[:,6]
    code_list = data[:,7]
    raw_dict = {}
    last = 0
    for i in range(len(code_list)-1):
        if code_list[i] != code_list[i+1]:
            raw_dict[str(code_list[i])] = {'date':date_list[last:i],"high":high_list[last:i],"volume":volume_list[last:i]}
            last = i+1

    for stock,attr in raw_dict.items():
        dimension_reduction = Dimensionality_reduction(stock,attr['date'],attr['high'],attr['volume'])
        x1,y1 = dimension_reduction.dimensionality_reshape()
        break
    '''
    list1 = []
    list2 = []
    list3 = []
    print x1,x2,x3
    for i in range(len(x1)):
        list1.append((x1[i],y1[i]))
    for i in range(len(x2)):
        list2.append((x2[i],y2[i]))
    for i in range(len(x3)):
        list3.append((x3[i],y3[i]))
    distance,C,D1,path = get_DTW_distance(list3,list2)
    print distance
    '''
