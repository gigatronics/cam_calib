'''
repeat the frames 30 times, so the stitched avi can be used by suostitch 
with depth estimation option on.. note also, the codec needs to be mjpeg
'''


import cv2
#import numpy as np
import glob
import os

dir = r'C:\Users\demoPC\py\cam_calib\data_framesout\frames_out_oct23_4m-5m\suo\\'
#h,w = 2160,3840
h,w = 2076,3088
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(dir+'suo.avi', fourcc, 30, (w,h))
counter=0

#def pad_filename(dir):
for file in glob.glob(dir+'*.jpg'):
    basename = os.path.basename(file)
    if len(basename)==10:                # if basename is frame9.jpg
        print(basename) 
        new_basename = basename[0:5]+'0'+basename[5:]      # change it to frame09.jpg
        os.rename(file,dir+new_basename)              
        

for file in sorted(glob.glob(dir+'*.jpg')):  
    print(file)
    img=cv2.imread(file)
    for i in range(10):            # repeat 10 times, for stitching w/ depth...5 may be sufficient.. can change ini file depth section
        out.write(img)
print('jpeg to video conversion complete.')
out.release()