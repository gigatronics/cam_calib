# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 15:51:04 2018

@author: demoPC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


file = r'C:\Users\demoPC\py\cam_calib\output_stitched\output.txt'

col = 'filename, num_corners_imgL, num_corners_imgR, avg_disparity, horizontal_parallax, depth_est, plane_fitting_residual \n'
cols = col.split()

df = pd.read_csv(file, usecols = cols)

data = pd.read_csv(file, delimiter=',')
data.head()



with open(file, 'r') as f:
    for row in csv.reader(f):
        print(row)