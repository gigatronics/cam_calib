# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:17:22 2018

@author: demoPC
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2 
import glob
import os

#
#import matplotlib.style
#import matplotlib as mpl
#mpl.style.use('classic')
#mpl.style.use('viridis')

# evaluate


dir = r'D:\data\frames_out_nov1_axis\out_chrom0_png\\'
dir = r'D:\data\181101_chrom_aber\\'

file = 'test2.png'
h,w = 2160,3840

#for file in sorted(glob.glob(dir+'*.png')):  # key=os.path.getmtime
#    basename = os.path.basename(file)[:-4]
#    print(file)

# read in image and split in half
img = cv2.imread(dir+file)
#h,w = img.shape[0:2]
img = img[0:int(h/4),:]
img = img[310:365,790:850]
b,g,r = img[:,:,0], img[:,:,1],img[:,:,2]

bline = b[20,:]
gline = g[20,:]
rline = r[20,:]

# 
gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edg = cv2.Laplacian(gry, cv2.CV_64F)

b2 = cv2.GaussianBlur(b,(3,3),0)
g2 = cv2.GaussianBlur(g,(3,3),0)
r2 = cv2.GaussianBlur(r,(3,3),0)

dff_bg = b2-g2
dff_gr = g2-r2
dff_rb = r2-b2


#for i, value in enumerate(diff_gr):
    


plt.subplot(311), plt.imshow(b), plt.title('blue')
plt.subplot(312), plt.imshow(g), plt.title('green')
plt.subplot(313), plt.imshow(r), plt.title('red')

plt.figure()
plt.subplot(411), plt.imshow(edg, cmap='gray'), plt.title('edge detection')
plt.subplot(412), plt.imshow(dff_bg, cmap='gray'), plt.title('difference of gaussian')
plt.subplot(413), plt.plot(bline, 'b', gline, 'g', rline, 'r')


plt.show()

