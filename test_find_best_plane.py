# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 15:59:41 2018

@author: demoPC
"""

pts3d_cart = [(-0.2539635399831244, -0.23339514152377222, -0.9590406571030256),
(-0.31368118704980524, -0.28743585039652697, -0.8957621194729685),
(-0.37740562652963466, -0.3448200670641994, -0.8497465176736435),
(-0.43803813177279366, -0.40021750434266784, -0.7945776074214501),
(-0.4936530245035946, -0.4523496555006306, -0.7314994944986516),
(-0.5567647511438067, -0.5101808980671229, -0.6844400754160144),
(-0.2359275668096303, -0.238688804080965, -0.9331510423883909),
(-0.29908953057050064, -0.3025899996782232, -0.8957621194729685),
(-0.35087694031788985, -0.35498351632492087, -0.8265968760864808),
(-0.4186343099636167, -0.42230361715808223, -0.793605695129099),
(-0.47222365026055113, -0.4763626651383531, -0.730402947202255),
(-0.5324337714531463, -0.5371005248024817, -0.6832035267600293),
(-0.22937578093384367, -0.2554939315462754, -0.9596037493508877),
(-0.29063445796296555, -0.32467660647363644, -0.9213286421020552),
(-0.3418867519743133, -0.38193210539219163, -0.8489089147723661),
(-0.3974692907332182, -0.444025052628786, -0.7926316581154771),
(-0.44816945783723205, -0.5006637537599337, -0.7293044443973642),
(-0.5067244667388532, -0.56442326077634, -0.6807249453392499),
(-0.21646609969749747, -0.26651984094572884, -0.9596037493508877),
(-0.2742301330083447, -0.33864601148823376, -0.9213286421020552),
(-0.3220098466364827, -0.3988337284809382, -0.8489089147723661),
(-0.37517510286556904, -0.464682948897568, -0.7916554989883693),
(-0.4236237761082799, -0.5231317965567559, -0.7282039890249964),
(-0.49345567513861976, -0.6057556182537649, -0.6988745702422468),
(-0.20383177220564744, -0.27630238250056505, -0.9596037493508877),
(-0.25766672401851554, -0.351413070730486, -0.9213286421020552),
(-0.30332302772974734, -0.41494466580098033, -0.8480690390864566),
(-0.3524484279027144, -0.48214801303669735, -0.7916554989883693),
(-0.41061630999106125, -0.5583053086187194, -0.7472745024699836),
(-0.4531634955133752, -0.6124153158947298, -0.6769934127418983)]



import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def find_best_plane(pts3d_cart, basename):
    xs=[]
    ys=[]
    zs=[]
    for pt3d in pts3d_cart:
        x,y,z =pt3d
        xs.append(x)
        ys.append(y)
        zs.append(z)
        
    
    # plot raw data
    plt.figure()
    ax = plt.subplot(111, projection='3d')
    ax.scatter(0,0,0)
    ax.scatter(xs, ys, zs, color='b')
    
    
    # find  fit
    tmp_A=[]
    tmp_b=[]
    for i in range(len(xs)):
        tmp_A.append([xs[i],ys[i],1])
        tmp_b.append(zs[i])
     
    A = np.matrix(tmp_A)
    b = np.matrix(tmp_b).T

#   method 1: using linear algebra mehtod.. probly the fastest
#   coeff = (A.T*A).I*A.T*b
    
#   method 2: using psudo inverse
    Aplus = np.linalg.pinv(tmp_A)
    coeff = Aplus*b
    
    error = b-A*coeff
    res = np.linalg.norm(error)         # norm = min distance...
    
    print("plane fitting solution: %f x + %f y + %f = z" % (coeff[0], coeff[1], coeff[2]))
    print("error: %s" % (error.T))
    print("*** residual error for flatness: %.3f" % res)
    
    
    # plot plane
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    X,Y = np.meshgrid(np.linspace(xlim[0], xlim[1],10),np.linspace(ylim[0], ylim[1],10))
    Z = np.zeros(X.shape)
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            Z[i,j]=coeff[0]*X[i,j]+coeff[1]*Y[i,j]+coeff[2]
    ax.plot_wireframe(X,Y,Z, color='k')
    #plt.show()
    
    fig = plt.gcf()
    fig.savefig(basename+'_fig.png')

    return error, res

