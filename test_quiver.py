# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:55:45 2018

@author: demoPC
"""


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np




def plot_vector(v):  # v = [start x,y,z, end x,y,z]
#    X,Y,Z,U,V,W = zip(*v)
  #  fig = plt.figure()
    ax = plt.gca(projection='3d')
    ax.quiver(v[0],v[1],v[2],v[3],v[4],v[5])
    ax.set_xlim(-1, 1), ax.set_ylim(-1, 1), ax.set_zlim(-1, 1)
    plt.show()
    
    
if __name__ == '__main__':
    # camera extrinsic matrix pararmeters
    t1,p1,r1,r1b = 0.000644642, -0.00408379, 0.00251538, -0.00133061
    t2,p2,r2,r2b = 0.00021955, 0.00253898, 2.09217, 0.0100985
    t3,p3,r3,r3b = -0.00091583, -0.00227629, 4.18497, -0.00837335
    
    #p1 = (np.sin(t1)*np.cos(p1), np.sin(t1)*np.sin(p1), cos(t1))
    
    #x1,y1,z1,z1b = np.cos(y1)*np.cos(x1), np.cos(y1)*np.sin(x1), np.cos(z1), z1b
    #x2,y2,z2,z2b = np.cos(z2)*np.cos(x2), np.cos(z2)*np.sin(x2), np.cos(z2), z2b
    #x3,y3,z3,z3b = np.cos(z3)*np.cos(x3), np.cos(z3)*np.sin(x3), np.cos(z3), z3b
    #print(x1,y1,z1)
    #print(x2,y2,z2)
    
    
    x1,y1,z1 = 0.3, 0, np.sqrt(1-0.3*0.3)
    x2,y2,z2 = -0.3, 0, np.sqrt(1-0.3*0.3)
    x3,y3,z3 = 0, 0.6, np.sqrt(1-0.6*0.6)
    
    # scatter plot
    p0 = [0],[0],[0]
    p00 = [0,0,0]
    p1 = [0,0,0,x1,y1,z1]           # start x,y,z and end x,y,z
    p2 = [0,0,0,x2,y2,z2]
    p3 = [0,0,0,x3,y3,z3]
    
    plot_vector(p1)
#    p = np.array([p1, p2, p3])
#    X,Y,Z,U,V,W = zip(*p)    #X=(0,0,0)...U=(x1,x2,x3..),V=(y1,y2,y3..),W=(z1,z2,z3...)
#    
    
#    
#    fig = plt.figure()
#    #ax=fig.add_subplot(111, projection='3d')
#    ax2=fig.gca(projection='3d')
#    ax2.quiver(X,Y,Z,U,V,W,color=['r','g','b'], normalize=True) #scale_units='xyz',
#    ax2.set_xlim([-1, 2])
#    ax2.set_ylim([-1, 2])
#    ax2.set_zlim([-1, 2])
#    plt.show()
#    
    
        



#
#line1 = np.cross(np.transpose(p0),np.transpose(p1))
#
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#
#ax.scatter(x1, y1, z1, c='r', marker='o')
#ax.scatter(x2, y2, z2, c='g', marker='o')
#ax.scatter(x3, y3, z3, c='b', marker='o')
#
#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')
#plt.show()

#
## quiver plot
#fig = plt.figure()
#ax2 = fig.gca(projection='3d')
#
## Make the grid
#x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.2),
#                      np.arange(-0.8, 1, 0.2),
#                      np.arange(-0.8, 1, 0.8))
#
## Make the direction data for the arrows
#u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
#v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
#w = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
#     np.sin(np.pi * z))
#
#
#ax2.quiver(x, y, z, u, v, w, length=0.1, normalize=True)
#plt.show()
#
## quiver2
#fig = plt.figure()
#ax3 = fig.gca(projection='3d')
#
#ax3.quiver(u,v,p0,p1) #,  units = 'xy', scale = 1)
#plt.show()
