# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:18:36 2018

@author: demoPC
"""

#import matplotlib.pyplot as plt
import pandas as pd

#  pd read in txt
cols = 'filename, num_corners_imgL, num_corners_imgR, avg_disparity, horizontal_parallax, depth_est_error, plane_fitting_residual_sam1m'
cols = cols.split(', ')
filename = 'output_sam1_vs_tripod.txt'
df = pd.read_csv(filename, sep=',', names=cols)  


# clean up 
df1 = df.copy()
for i in [1,2,3,4,5,6]:
    df1[cols[i]] =pd.to_numeric(df[cols[i]], errors = 'coerce')
df1.info()



# add new column for "distance" (1m vs 2m) and "method" (sam vs tripod) 
# ... read the filename, if it contains 1m, assign distance = 1m
# ... if contains sam, assign method = sam
df1.loc[1:6, 'distance']=1  # 1m
df1.loc[8:13, 'distance']=2
df1.loc[15:34, 'distance']=3
df1.loc[36:41, 'distance']=1
df1.loc[43:48, 'distance']=2
df1.loc[50:, 'distance']=3

index = df1['filename'].str.contains('tripod')
df1.loc[index, 'method']=11
index = df1['filename'].str.contains('sam')
df1.loc[index, 'method']=12
index = df1['filename'].str.contains('sam')
df1.loc[index, 'method']=12


# cleaning up, remove na, and remove no-corners detected
df0 = df1[((df1['num_corners_imgL']+df1['num_corners_imgR'])!=0)].dropna()

# add a new column for depth error
err_value = abs(df0['depth_est_error']-df0['distance']) / df0['distance']*100
df0.loc[(df0['depth_est_error']!=0),'depth_err_perc']=err_value

# count match & mismatch
#print(groupby_method.count(), groupby_method.size())
def count_match(df, method, mismatch):
    if mismatch == 1:
        return df[(df['num_corners_imgL']!=df['num_corners_imgR']) & (df['method']==method)]
    else: 
        return df[(df['num_corners_imgL']==df['num_corners_imgR']) & (df['method']==method)]
match_m11 = len(count_match(df0, 11, 0))
match_m12 = len(count_match(df0, 12, 0))
mmatch_m11 = len(count_match(df0, 11, 1))
mmatch_m12 = len(count_match(df0, 12, 1))


# depth error & flatness groupby method... using weigthed function
# feature1 = 0.5*mean(depth_error_1m)+0.5*mean(depth_error_2m) ??
# feature2 = 0.5*mean(res@1m)+0.5*mean(res@2m)  ??
print(df0.groupby(['method', 'distance'])['depth_err_perc', 'horiztonal_parallax'].mean())  #<<<<< 






#
## group data based on 1m vs 2m data..
#col_of_int = ['num_corners_imgL', 'num_corners_imgR']
#col_of_int2 = ['avg_disparity', 'horiztonal_parallax', 'depth_err_perc']
#
#df_1m_sam = df2[(df2['distance']==1) & (df2['method']==12)]#.head()
#df_1m_tri = df2[(df2['distance']==1) & (df2['method']==11)]
#df_2m_sam = df2[(df2['distance']==2) & (df2['method']==12)]
#df_2m_tri = df2[(df2['distance']==2) & (df2['method']==11)]
#
#
#
## compare 1m vs 2m? manual vs tripod? for "depth estimation error" 
#plt.subplot(221)
#x1 = df_1m_sam['depth_err_perc']
#x2 = df_1m_tri['depth_err_perc']
#x3 = df_2m_sam['depth_err_perc']
#x4 = df_2m_tri['depth_err_perc']
#plt.plot(x1,'ro', label='manual @1m')
#plt.plot(x2,'yo', label='tripod @1m')
#plt.plot(x3,'g*', label='manual @2m')
#plt.plot(x4,'b*', label='tripod @2m')
#plt.ylabel('depth estimation error (in %)')
#plt.xticks([])
#plt.title('depth estimation error - expecting 0%')
#
#plt.legend()
#
#
#
## compare 1m vs 2m? manual vs tripod? for "horizontal disparity" 
#plt.subplot(222)
#x11 = df_1m_sam['horiztonal_parallax']
#x12 = df_1m_tri['horiztonal_parallax']
#x13 = df_2m_sam['horiztonal_parallax']
#x14 = df_2m_tri['horiztonal_parallax']
#plt.plot(x11,'ro', label='manual @1m')
#plt.plot(x12,'yo', label='tripod @1m')
#plt.plot(x13,'g*', label='manual @2m')
#plt.plot(x14,'b*', label='tripod @2m')
#plt.ylabel('number of pixels')
#plt.xticks([])
#plt.title('horizontal parallax - ideally 0 pixel')
#
#
#
## compare 1m vs 2m? manual vs tripod? for "planar fit" 
#plt.subplot(223)
#x1 = df_1m_sam['plane_fitting_residual_sam1m']
#x2 = df_1m_tri['plane_fitting_residual_sam1m']
#x3 = df_2m_sam['plane_fitting_residual_sam1m']
#x4 = df_2m_tri['plane_fitting_residual_sam1m']
#plt.plot(x1,'ro', label='manual @1m')
#plt.plot(x2,'yo', label='tripod @1m')
#plt.plot(x3,'g*', label='manual @2m')
#plt.plot(x4,'b*', label='tripod @2m')
#plt.ylabel('residual error')
#plt.xticks([])
#plt.title('reprojected plane fitting residual - expecting 0')
#
#
#
## number of corners found 
#plt.subplot(224)
#x1 = df_1m_sam['num_corners_imgL']
#x2 = df_1m_tri['num_corners_imgL']
#x3 = df_2m_sam['num_corners_imgL']
#x4 = df_2m_tri['num_corners_imgL']
#plt.plot(x1,'ro', label='manual @1m')
#plt.plot(x2,'yo', label='tripod @1m')
#plt.plot(x3,'g*', label='manual @2m')
#plt.plot(x4,'b*', label='tripod @2m')
#plt.ylabel('number of corners')
#plt.xticks([])
#plt.title('number of corners found - expecting 54')
#
#plt.show()