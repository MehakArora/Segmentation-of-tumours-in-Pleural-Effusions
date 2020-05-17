# -*- coding: utf-8 -*-
"""MP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SH4eZop1fM05wvnz767ng4C4kVNZlhcq
"""

#from google.colab import drive
#%drive.mount('/content/gdrive')

#import os
#os.chdir('/content/gdrive/My Drive/MP2/')

import numpy as np
import cv2 
import matplotlib.pyplot as plt

img = cv2.imread('benign_4x/_11001.tif')
img_gt = cv2.imread('benign_4x/_11001_gt.png')
img_gt = np.array(img_gt)

fig, (a1,a2) = plt.subplots(1,2, figsize=(15,15))
a1.imshow(img)
a2.imshow(img_gt)
fig.show

df = []
thetaAll = []
sigmaAll = []
gammaAll = []
lamdaAll = []
num = 1  #To count numbers up in order to give Gabor features a lable in the data frame
kernels = []  #Create empty list to hold all kernels that we will generate in a loop
for theta in range(2):   #Define number of thetas. Here only 2 theta values 0 and 1/4 . pi 
    theta = theta / 4. * np.pi
    for sigma in (1, 3):  #Sigma with values of 1 and 3
        for lamda in np.arange(0, np.pi, np.pi / 4):   #Range of wavelengths
            for gamma in (0.05, 0.5):   #Gamma values of 0.05 and 0.5
                           
                gabor_label = 'Gabor' + str(num)  #Label Gabor columns as Gabor1, Gabor2, etc.
#                print(gabor_label)
                ksize=9
                kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)    
                kernels.append(kernel)
                #Now filter the image and add values to a new column 
                fimg = cv2.filter2D(img, cv2.CV_8UC3, kernel)
                #filtered_img = fimg.reshape(-1)
                #df[gabor_label] = filtered_img  #Labels columns as Gabor1, Gabor2, etc.
                df.append(fimg)
                thetaAll.append(theta)
                sigmaAll.append(sigma)
                lamdaAll.append(lamda)
                gammaAll.append(gamma)
                print(gabor_label, ': theta=', theta, ': sigma=', sigma, ': lamda=', lamda, ': gamma=', gamma)
                num += 1  #Increment for gabor column label
                

#df.to_csv("Gabor.csv")

df = np.array(df)
thetaAll = np.array(thetaAll)
sigmaAll = np.array(sigmaAll)
gammaAll = np.array(gammaAll)
lamdaAll = np.array(lamdaAll)

print(df.shape)

for i in range(len(df)):
  plt.imshow(df[i])
  plt.show()
  print("theta: ", thetaAll[i], " sigma: ", sigmaAll[i], " gamme: ", gammaAll[i], " lamda: ", lamdaAll[i])

