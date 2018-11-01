# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 15:20:11 2018

@author: demoPC


glitchy! doesn't break..

"""





import cv2
import os


dir =r'C:\Users\demoPC\py\cam_calib\output_stitched\\'
file = r'out_4m_tripod.avi'

i=1
cap = cv2.VideoCapture(dir+file)
while(cap.isOpened()):
    if i > 1000 :
        break
    ret, frame=cap.read()
    if (i%10)==0:           # extract every 10 frames
        cv2.imwrite(os.path.splitext(file)[0]+'_'+str(i)+'.png', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    i+=1    
cap.release()