# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:18:36 2018

@author: demoPC
"""

#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from parser import OptionParse

# read in filename
filename = 'output_model_pert.txt'

# optional arg to provide alternative filename
parser = OptionParse()
parser.add_option('-f', '--filename', action='store', type='string', dest='filename')
opt, args = parser.parse_args()
filename = opt.filename

#  pd read in txt
#cols = 'filename, num_corners_imgL, num_corners_imgR, avg_disparity, horizontal_parallax, depth_est_error, plane_fitting_residual_sam1m'
#cols = cols.split(', ')
#df = pd.read_csv(filename, sep=',', names=cols)  

df = pd.read_csv(filename, sep=',')
cols = df.columns


# clean up... remove no-corners detected, remove na values
df0 = df.copy()
for i in [1,2,3,4,5,6]:
    df0[cols[i]] =pd.to_numeric(df[cols[i]], errors = 'coerce')


# assignment "method" and 'distance'
index = df0['filename'].str.contains('tripod')
df0.loc[index, 'method']=91
index = df0['filename'].str.contains('sam')
df0.loc[index, 'method']=92
index = df0['filename'].str.contains('int')
df0.loc[index, 'method']=93
index = df0['filename'].str.contains('ext')
df0.loc[index, 'method']=94

index = df0['filename'].str.contains('1m')
df0.loc[index, 'distance']=1
index = df0['filename'].str.contains('2m')
df0.loc[index, 'distance']=2
index = df0['filename'].str.contains('3m')
df0.loc[index, 'distance']=3


#df0 = df1[((df1['num_corners_imgL']+df1['num_corners_imgR'])!=0)].dropna()

# add a new column for depth error
err_value = abs(df0['depth_est_error']-df0['distance']) / df0['distance']*100
df0.loc[(df0['depth_est_error']!=0),'depth_err_perc']=err_value


# count match & mismatch
#print(groupby_method.count(), groupby_method.size())


def count_match(df, method, mismatch):
    if mismatch == 1:
        return df[(df['num_corners_imgL']!=df['num_corners_imgR']) & (df['method']==method) & ((df['num_corners_imgL']+df['num_corners_imgR'])!=0)] 
    else: 
        return df[(df['num_corners_imgL']==df['num_corners_imgR']) & (df['method']==method) & ((df['num_corners_imgL']+df['num_corners_imgR'])!=0)]
#print results
print('methods legned: 91-tripod, 92-manual, 93-intrinsic perterb, 94-extrinsic pertub')
passed =[]
methods = [91, 92, 93, 94]

for i in methods:
    total = len(df0[df0['method']==i])
    match = len(count_match(df0, i, 0))
    mmatch = len(count_match(df0, i, 1))
    passed.append((match/total >= 0.5))
    print('using method %g, a total of %g images were analyzed, corners were found in %g images, among which %g are matched' % (i, total, match+mmatch, match))


# depth error & flatness groupby method... using weigthed function
print(df0.groupby(['method', 'distance'])['depth_err_perc', 'horizontal_parallax'].mean())  #<<<<< 

# results intepretation
a = np.array(methods)
print('calibration model(s) %s are good' % str(a[passed]))

    

'''
results intepretation:
    four methods were compared here. 
    1) we want majority of images provided be analyzed, say 75%. so method 91 and 92 both pass.
    2) we look at the depth_error_perc, and horizontal_parallax.. 
    eg. we aim for less than 30% depth error and under 5 px mean residual.. so method 91 @1m is good.
'''