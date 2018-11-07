# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 15:20:11 2018

@author: demoPC

glitchy! doesn't break..

"""

import cv2
import os
from optparse import OptionParser

path =r'C:\Users\demoPC\py\cam_calib\output_ids\\'
file = r'out_4m_tripod.avi'
file = r'out_chrom0.avi'
file = r'out_ext_2m.avi'


# optional argument to specify the avi path and filename
parser = OptionParser()
parser.add_option('-p','--path', action="store", type="string", dest = 'path')
parser.add_option('-f', '--filename', action="store", type="string", dest ='filename')
opt, args = parser.parse_args()
path = opt.path
file = opt.filename
print(path, file)


i=1
cap = cv2.VideoCapture(path+file)
while(cap.isOpened()):
    if i > 50 :
        break
    ret, frame=cap.read()
    if (i%10)==0:           # extract every 10 frames
        cv2.imwrite(path+os.path.splitext(file)[0]+'_'+str(i)+'.png', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    i+=1    
cap.release()