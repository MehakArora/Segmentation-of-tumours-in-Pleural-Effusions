# -*- coding: utf-8 -*-
"""MP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SH4eZop1fM05wvnz767ng4C4kVNZlhcq
"""

from google.colab import drive
drive.mount('/content/gdrive')

import os
os.chdir('/content/gdrive/My Drive/MP2/')

import numpy as np
import cv2 
import matplotlib.pyplot as plt

img = cv2.imread('benign_4x/_11001.tif')
img_gt = cv2.imread('benign_4x/_11001_gt.png')
img_gt = np.array(img_gt)

fig, (a1,a2) = plt.subplots(1,2, figsize=(25,25))
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

kernels = np.array(kernels)

for i in range(len(df)):
  plt.imshow(df[i])
  plt.show()
  plt.imshow(kernels[i])
  plt.show()
  print("theta: ", thetaAll[i], " sigma: ", sigmaAll[i], " gamme: ", gammaAll[i], " lamda: ", lamdaAll[i])

ksize = 9
#sigma = 1.55
theta = 0.0
#lamda = 4.75
gamma = 1


img_grey= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#plt.imshow(img_grey, cmap = 'gray')
#plt.show()

kernels = []
features = []

for sigma in np.arange(1,2,0.5):
  for lamda in np.arange(3,5,0.25):
    for gamma in np.arange(0.5,1.25,0.25):
      k = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)   
      kernels.append(k) 
      fimg = cv2.filter2D(img_grey, cv2.CV_8UC1, k)
      #fimg = cv2.GaussianBlur(fimg, (15,15), 5, 5)
      fimg = cv2.medianBlur(fimg, 11)
      fimg = fimg.reshape((fimg.shape[0]*fimg.shape[1],))
      features.append(fimg)

features = np.array(features)
features = features.T
#features = features.reshape((len(features[0]), len(features)))
kernels = np.array(kernels)
#fimg1 = cv2.filter2D(img, cv2.CV_8UC1, k1)
#plt.figure(figsize=(10,10))
#plt.imshow(fimg1, cmap = 'gray')
#plt.show()
#plt.figure(figsize = (15,15))
#simg = cv2.GaussianBlur(fimg, (15,15), 5, 5)
#smimg = cv2.medianBlur(fimg, 11)

#plt.imshow(simg)
#plt.show()

#plt.figure(figsize=(15,15))
#plt.imshow(smimg, cmap = 'gray')
#plt.show()

a = np.array([1,2,3])
b = np.array([4,5,6])
a.reshape(1,3)
b.reshape((3,1))
l = []
l.append(a)
l.append(b)
l = np.array(l)
print(a.shape)
print(b.shape)
print(l.shape)
print(features.shape)

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
kmeans.fit(features)
y = kmeans.predict(features)
img_seg = y.reshape((img.shape[0], img.shape[1]))
img_seg_copy = np.copy(img_seg)

plt.figure(figsize= (10,10))
plt.imshow(simg,cmap = 'gray')
plt.show()

plt.figure(figsize = (10,10))
plt.imshow(smimg, cmap = 'gray')
plt.show()

from sklearn.cluster import KMeans


kmeans = KMeans(n_clusters=3)

NI = img.reshape((img.shape[0]*img.shape[1],3))
kmeans.fit(NI)
y_kmeans_n = kmeans.predict(NI)

#Fgrey = cv2.cvtColor(fimg1, cv2.COLOR_BGR2GRAY)
FI = fimg.reshape((fimg.shape[0]*fimg.shape[1],1)) 
kmeans.fit(FI)
y_kmeans_f = kmeans.predict(FI)

#Sgrey = cv2.cvtColor(simg, cv2.COLOR_BGR2GRAY)
#SI = Sgrey.flatten()
SI = simg.reshape((simg.shape[0]*simg.shape[1],1) )
kmeans.fit(SI)
y_kmeans_sg = kmeans.predict(SI)

#SMgrey = cv2.cvtColor(smimg, cv2.COLOR_BGR2GRAY)
#SMI = SMgrey.flatten()
SMI = smimg.reshape((smimg.shape[0]*smimg.shape[1],1)) 
kmeans.fit(SMI)
y_kmeans_smg = kmeans.predict(SMI)

features = np.column_stack((FI,SI, SMI))
kmeans.fit(features)
y_kmeans_all = kmeans.predict(features)

print(y_kmeans_n.shape)
print(y_kmeans_all.shape)

yn = y_kmeans_n.reshape((img.shape[0],img.shape[1]))
yf = y_kmeans_f.reshape((fimg.shape[0],fimg.shape[1]))
ys = y_kmeans_sg.reshape((simg.shape[0],fimg.shape[1]))
ysm = y_kmeans_smg.reshape((smimg.shape[0],fimg.shape[1]))
yall = y_kmeans_all.reshape((img.shape[0],img.shape[1]))

plt.figure(figsize=(15,15))
plt.imshow(ysm)
plt.show()

fig, (a1,a2,a3) = plt.subplots(1,3, figsize=(25,25))
a1.imshow(img)
a2.imshow(img_gt)
a3.imshow(img_seg)
fig.show

img_seg_copy = np.copy(img_seg)
img_seg = np.uint8(img_seg)

img_seg_filt = cv2.medianBlur(np.uint8(img_seg), 15)
fig, (a1,a2,a3) = plt.subplots(1,3, figsize=(25,25))
a1.imshow(img_seg)
a2.imshow(img_gt)
a3.imshow(img_seg_filt)
fig.show

part1 = np.where(img_seg == 1)
img1 = np.zeros(img_seg_filt.shape)
img1[part1] = 255
plt.imshow(img1, cmap = 'gray')
plt.show()

