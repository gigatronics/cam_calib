# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:18:10 2018

@author: demoPC
"""


''' 
known: camera model, stitched stereo images with patterns, known distance of the pattern
goal: to estimate the distance of pattern 
steps: 
    1. split images
    2. find corners
    3. matche corners
    4. calculate vertical parallex.. 
    5. calculate distance from camera
'''


import cv2
import numpy as np
import subprocess
import time
import csv
import matplotlib.pyplot as plt
import os
import math
import test_find_best_plane
import glob

def extract_corners(cmd_dir,cmd, img, out): #need dsc file in the current working dir
    full_cmd = cmd_dir+cmd+img+out
    print('extracting corners... %s' % full_cmd)
    subprocess.Popen(full_cmd)
    return out

def read_csv(filename):
    pts = []
    with open(filename) as f:
        reader = csv.reader(f)
 #       print(next(reader))
        for row in reader:
            pt = np.array([row[3],row[4]])
            pt_int = [int(float(x))for x in pt]         # conv str to int
        #    print(pt_int)
            if pt_int != [0, 0]:                        # discard (0,0)
                pts.append(pt_int)
    print('found %g corners' % len(pts))
    return pts


def find_box(corners):
    x =[]
    y =[]
    for pt in corners:
        x.append(pt[0])
        y.append(pt[1])
    xpad = int((max(x)-min(x))*0.05)
    ypad = int((max(y)-min(y))*0.05) 
    # checks to make sure box is within image.. 
    x1 = max(1, min(x)-xpad)
    y1 = max(1, min(y)-ypad)
    x2 = min(W, max(x)+xpad)
    y2 = min(H, max(y)+ypad)
    return((x1, y1),(x2, y2))
#
def crop2(image,pts):
#    x=pts[0][0]
#    y=pts[0][1]
#    dely=pts[1][1]-pts[0][1]
#    delx=pts[1][0]-pts[0][0]
    return image[pts[0][1]:pts[1][1],pts[0][0]:pts[1][0]]

def find_corners_cv(gry):
#    img = cv2.imread('test_img2.png')
#    pattern_size = (6,9)
#    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gry, PATTERN_SIZE)
#    print('findg corners: %s' % (ret, len(corners)))
    print(ret)
    return corners

def find_corners(img):
    ''' RETURNS corners and rect of an image.. 
    this func encapsulates a few other funcs to save repeated calls
    '''   
    
    if os.path.exists('cam0.txt'):
        os.remove('cam0.txt')

    cv2.imwrite('img_temp.png',img)  
    extract_corners(cmd_dir,cmd,'img_temp.png',' cam')
    time.sleep(4)                # takes time to write to file 
      
    while True:
        corners = read_csv('cam0.txt')
        print('found %g corners. ' % len(corners))
        if (len(corners)!=0):        
            rect = find_box(corners) 
            crp = crop2(img, rect)
            break
        time.sleep(4)                # takes time to write to file 
    print('found %g corners' % len(corners))
    return corners, crp


def cam2world(pt2d):  # points in cartisian (x,y) img pixel
    x,y = pt2d
    phi = x/W*math.pi*2    
    theta = y/H*math.pi  # in radians
    return phi, theta  # in radians, radians, meter


def calc_depth(pt2da, pt2db):
    phi1,theta1 = cam2world(pt2da)
    phi2,theta2 = cam2world(pt2db)

    t = 0.060   # camera baseline
    flag=0

    del_phi = (phi2-phi1)
    if del_phi ==0:             # should not be 0, but if no disparity.. assign 0.1-degree
        del_phi = (np.radians(0.1))
        print('non-disparity detected.. flag* raised') 
        flag =1
    rho1 = t/math.sin(del_phi) #* math.sin(phi2)
    rho2 = t/math.sin(del_phi) #* math.sin(phi1)
    depth = abs((rho1+rho2)/2)   
    return rho1, rho2, depth, flag


    
def sphere2cart(pt3d_sphere):
    phi, theta, rho = pt3d_sphere       # phi = [0,2pi], theta = [0,pi]
    x = rho*np.sin(phi)*np.cos(theta)
    y = rho*np.sin(phi)*np.sin(theta)
    z = rho*np.cos(phi)
    pt3d_cart = (x,y,z)
    return pt3d_cart


def cart2sphere(pt3d_cart):
    x,y,z = pt3d_cart
    rho = np.sqrt(x**2+y**2+z**2)
    theta = np.atan(y/x)
    phi = np.atan((np.sqrt(x**2+y**2))/z)
    pt3d_sphere = (rho, theta, phi)
    return pt3d_sphere


def save_to_file(filename,content):
    with open(filename, 'a') as f:
        f.writelines(content)

def save_image(filename,img):
    plt.imwrite(filename,img)
    

if __name__ == "__main__":
    
    os.chdir(r'C:\Users\demoPC\py\cam_calib')

    global W,H, PATTERN_SIZE
    W = 3840
    H = 2160    # 1080 per eye
    PATTERN_SIZE = (9,6)
    
#    cornersL=[]
#    cornersR=[]
#    
#    del cornersL[:]
#    del cornersR[:]

    
    dir = r'C:\Users\demoPC\py\cam_calib\output_stitched\png_tripod\3m\\'
#    file = 'out_1m_sam1s_10.png'        # 1m working
#    file = 'out_1m_sam1s_70.png'        # 2m working
#    file = 'out_1m_sam1s_130.png'        # 3m working
#
#   
    cmd_dir = r'C:\Users\demoPC\Desktop\SuoCalibration_v2.6.0a\oCametry\application\checkerDetect\\'
    cmd = r'FindCodedChecker.exe ' 
    
    col = 'filename, num_corners_imgL, num_corners_imgR, avg_disparity, horizontal_parallax, depth_est, plane_fitting_residual \n'
    save_to_file('output.txt', col)
    
    for file in sorted(glob.glob(dir+'*.png')):  # key=os.path.getmtime
#    while True:
        print(file)   
        basename = os.path.basename(file)[:-4]

        # read in image and split in half
        img = cv2.imread(file)
        imgL = img[0:int(H/2),:]
        imgR = img[int(H/2):H,:]
                
        imgL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
        imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
        
        # extract corners
        # method 1: april tag            
        if os.path.exists('camL0.txt'):
            os.remove('camL0.txt')
        if os.path.exists('camR0.txt'):
            os.remove('camR0.txt')
     
        cv2.imwrite('imgL.png',imgL)  
        extract_corners(cmd_dir,cmd,'imgL.png',' camL')
        time.sleep(4)                # takes time to write to file 
        cornersL = read_csv('camL0.txt')
    
        cv2.imwrite('imgR.png',imgR)  
        extract_corners(cmd_dir,cmd,'imgR.png',' camR')
        time.sleep(4)                # takes time to write to file 
        cornersR = read_csv('camR0.txt')   
#
#        # method 2: using opencv
#        cornersL = find_corners_cv(imgL)
#        cornersR = find_corners_cv(imgR)
    
        
        # draw corners for verification
        for pt in cornersL:
            cv2.circle(imgL, (pt[0],pt[1]), 5, (255,255,0), -1)
        for pt in cornersR:
            cv2.circle(imgR, (pt[0],pt[1]), 5, (255,255,0), -1)
               
        # print # of corners in the output..
 #       print('left eye: found %g corners' % len(cornersL))
 #        print('right eye: found %g corners' % len(cornersR)) 

        isEqualCorners = (len(cornersL)==len(cornersR))
        print('*** found equal number of corners: %s' % isEqualCorners)    # <<<<
 
 
       
        if len(cornersL)==0 or len(cornersR)==0 or (not isEqualCorners): 
            avg_disparity, hor_parallax, depth_est, residual = 0,0,0,0
        #    if len(cornersL)==len(cornersR):

        else:
            # calcluate disparity, offset per corner
            stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)   
            disparity = stereo.compute(imgL,imgR)   
        
            dists = []
            y_paras =[]
            # corner shifts
            for cornerL, cornerR in zip(cornersL, cornersR):
                x1,y1 = cornerL
                x2,y2 = cornerR
                dist = np.sqrt((x1-x2)**2+(y1-y2)**2)
                y_parallax = abs(y1-y2)
                dists.append(dist)
                y_paras.append(y_parallax)
            
            avg_disparity = np.mean(dists)
            hor_parallax = np.mean(y_paras)
            print('avg disparity of corners are %.2f pixels' % avg_disparity)
            print('horizontal parallex are %.2f pixels' % hor_parallax)
            print('*** horizontal parallex is less than 1 pixel: %s' % (hor_parallax<1))   # <<<< 
        
        
            
            # calculate depth using miriam's method    
            centreL = (np.average(cornersL,0))
            centreR = (np.average(cornersR,0))
            
            rho1, rho2, depth_est, flag = calc_depth(centreL, centreR)
    #            depth_est_error = abs((depth_est-DEPTH_EXP)/DEPTH_EXP*100)
            print('*** measured depth is %.2fm, while expecting 1/2/3m' % depth_est)  
            
                        
            # determine if the corners are on the same plane
            # 1 - convert corners to 3d world points
            
            pts3d = []
            for cornerL,cornerR in zip(cornersL, cornersR):
                phi,theta = cam2world(cornerL)
                phi2,theta2 = cam2world(cornerR)
                rho1, rho2, depth, flag = calc_depth(cornerL, cornerR)
                
                pts3d.append((phi,theta,depth, rho1, rho2, flag))
                
           
            # 2 - determine if the pt3ds are on the same plane.. and plot
            pts3d_cart = []
            for pt3d in pts3d:
                pt3d_cart = sphere2cart(pt3d[0:3])
                x,y,z = pt3d_cart
                pts3d_cart.append(pt3d_cart)    
                
            error, residual = test_find_best_plane.find_best_plane(pts3d_cart, basename)
           
            # plot
            plt.figure()
            rect = find_box(cornersL + cornersR) 
            crpL = crop2(imgL, rect)    
            crpR = crop2(imgR, rect)            
            crpD = crop2(disparity, rect)
                
            plt.subplot(311), plt.imshow(crpL)
            plt.subplot(312), plt.imshow(crpR)
            plt.subplot(313), plt.imshow(crpD)
            #plt.imsave()
            #plt.show() 
            fig = plt.gcf()
            fig.savefig(basename+'_plot.png')
                       
        # save to txt file
        output_list = [basename, len(cornersL), len(cornersR), avg_disparity, hor_parallax, depth_est, residual, '\n']
        output = ','.join(map(str,output_list))
        save_to_file('output.txt',output)
