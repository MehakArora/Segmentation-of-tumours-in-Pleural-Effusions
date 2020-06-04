# -*- coding: utf-8 -*-
"""FeatExtract_Segment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Fw4gvJ_elGPbG4sZnxoYqUlGPoNf_Xbt
"""

from google.colab import drive
drive.mount('/content/gdrive')

import numpy as np
import cv2 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import scipy
import os
os.chdir('/content/gdrive/My Drive/MP2/')

#Read Images
img1 = cv2.imread('benign_4x/_11064.tif')
img2 = cv2.imread('benign_4x/_11016.tif')
img3 = cv2.imread('benign_4x/_11001.tif')
img_gt1 = cv2.imread('benign_4x/_11064_gt.png')
img_gt2 = cv2.imread('benign_4x/_11016_gt.png')
img_gt3 = cv2.imread('benign_4x/_11001_gt.png')
img_gt1 = np.array(img_gt1)
img_gt2 = np.array(img_gt2)
img_gt3 = np.array(img_gt3)

def cvt2LAB(img, show):
  lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
  plt.imshow(lab)
  if(show):
    plt.show()
  
  l, a, b = cv2.split(lab)
  plt.imshow(l, cmap ='gray')
  if(show):
    plt.show()
  plt.imshow(a, cmap= 'gray')
  if(show):
    plt.show()  
  plt.imshow(b, cmap = 'gray')
  if(show):
    plt.show()

  labm = cv2.medianBlur(lab, 9)
  plt.imshow(labm)
  if(show):
    plt.show()

  return lab, labm, l, a, b


lab1,labm1, l1, a1, b1 = cvt2LAB(img1,1)
lab2,labm2, l2, a2, b2 = cvt2LAB(img2,1)
lab3,labm3, l2, a3, b3 = cvt2LAB(img3,1)

def extractGabor(img, ksizeRange, sigmaRange, thetaRange, gammaRange, lamdaRange, show):

  features = []
  channels = len(img.shape)
  
  for ksize in np.arange(ksizeRange[0], ksizeRange[1], ksizeRange[2]):
    for sigma in np.arange(sigmaRange[0], sigmaRange[1], sigmaRange[2]):
      for lamda in np.arange(lamdaRange[0], lamdaRange[1], lamdaRange[2]):
        for gamma in np.arange(gammaRange[0], gammaRange[1], gammaRange[2]):
          for theta in np.arange(thetaRange[0], thetaRange[1], thetaRange[2]):
            k = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)   
            fimg = cv2.filter2D(img, cv2.CV_8UC1, k)
            fimg = cv2.medianBlur(fimg, 5)
            
            if(show):
              plt.figure(figsize = (8,8))
              plt.imshow(fimg)
              plt.show()
              print(ksize, sigma, gamma, lamda, theta)
            
            if(channels == 1):
              fimg = fimg.reshape((fimg.shape[0]*fimg.shape[1],))
              features.append(fimg)
            elif(channels == 3):
              fimg = fimg.reshape((fimg.shape[0]*fimg.shape[1],3))
              features.append(fimg[:,0])
              features.append(fimg[:,1])
              features.append(fimg[:,2])
            else:
              print("Channels error")
              return 0

  
  features = np.array(features)
  features = features.T
  return features

#extractGabor(img, ksizeRange, sigmaRange, thetaRange, gammaRange, lamdaRange, show)
features1 = extractGabor(lab1, [9,10,2], [1,2,1], [0,1,1], [0.5,1.25,0.25], [3.25,4.1,0.25], 0)
features2 = extractGabor(lab2, [9,10,2], [1,2,1], [0,1,1], [0.5,1.25,0.25], [3.25,4.1,0.25], 0)
features3 = extractGabor(lab3, [9,10,2], [1,2,1], [0,1,1], [0.5,1.25,0.25], [3.25,4.1,0.25], 0)

def addLABfeatures(features, labm):
  features = np.hstack((features,labm[:,:,0].reshape((labm.shape[0]*labm.shape[1]),1)))
  features = np.hstack((features,labm[:,:,1].reshape((labm.shape[0]*labm.shape[1]),1)))
  features = np.hstack((features,labm[:,:,2].reshape((labm.shape[0]*labm.shape[1]),1)))
  return features

features1 = addLABfeatures(features1, labm1)
features2 = addLABfeatures(features2, labm2)
features3 = addLABfeatures(features3, labm3)

def kmeansClustering(features, n_clusters):
  kmeans = KMeans(n_clusters=3, init = 'k-means++')
  kmeans.fit(features)
  y = kmeans.predict(features)
  return kmeans, y

[kmeans1, y1] = kmeansClustering(features1, 3)
img_seg1 = y1.reshape((img1.shape[0], img1.shape[1]))
img_seg_copy1 = np.copy(img_seg1) 

[kmeans2, y2] = kmeansClustering(features2, 3)
img_seg2 = y2.reshape((img2.shape[0], img2.shape[1]))
img_seg_copy2 = np.copy(img_seg2) 

[kmeans3, y3] = kmeansClustering(features3, 3)
img_seg3 = y3.reshape((img3.shape[0], img3.shape[1]))
img_seg_copy3 = np.copy(img_seg3)

#Removing small regions of cytoplasm
img_seg1 = cv2.medianBlur(np.uint8(img_seg1), 9)
img_seg2 = cv2.medianBlur(np.uint8(img_seg2), 9)
img_seg3 = cv2.medianBlur(np.uint8(img_seg3), 9)

#Plotting Segmented Image

fig, (a1,a2,a3) = plt.subplots(1,3, figsize=(30,30))
a1.imshow(img1, cmap = 'gray')
a2.imshow(img_gt1 , cmap = 'gray')
a3.imshow(img_seg1, cmap = 'gray')
fig.show()

fig, (a1,a2,a3) = plt.subplots(1,3, figsize=(30,30))
a1.imshow(img2, cmap = 'gray')
a2.imshow(img_gt2 , cmap = 'gray')
a3.imshow(img_seg2, cmap = 'gray')
fig.show()

fig, (a1,a2,a3) = plt.subplots(1,3, figsize=(30,30))
a1.imshow(img3, cmap = 'gray')
a2.imshow(img_gt3 , cmap = 'gray')
a3.imshow(img_seg3, cmap = 'gray')
fig.show()

#Find Background Class as most populated class and setting it to zero

def bgToZero(img_seg):
  counts = np.bincount(img_seg.flatten())
  background = np.argmax(counts)
  if(background):
    print("Changing BG")
    img_seg[img_seg == background] = 255
    img_seg[img_seg == 0] = background
    img_seg[img_seg == 255] = 0
  return img_seg

img_seg1 = bgToZero(img_seg1)
img_seg2 = bgToZero(img_seg2)
img_seg3 = bgToZero(img_seg3)

#Finding Cell and Cytoplasm Clusters

def findCorrectLabel(img_seg, lab):

  clusters = np.unique(img_seg)
  clusters = clusters[1:]   #As label zero is background
  #Masks for each label
  mask1 = np.zeros(img_seg.shape)
  mask2 = np.zeros(img_seg.shape)
  mask1[img_seg == clusters[0]] = 255
  mask2[img_seg == clusters[1]] = 255
  
  #Finding histogram for a space
  hist1 = cv2.calcHist([lab],[1],np.uint8(mask1),[255],[0,256])
  peak1 = np.argsort(-hist1.flatten())[0]
  hist2 = cv2.calcHist([lab],[1],np.uint8(mask2),[255],[0,256])
  peak2 = np.argsort(-hist2.flatten())[0]

  if(peak1 > peak2):
    cell = clusters[0]
    cyto = clusters[1]
  else:
    cell = clusters[1]
    cyto = clusters[0]
  
  return cell, cyto

cell1, cyto1 = findCorrectLabel(img_seg1, lab1)
cell2, cyto2 = findCorrectLabel(img_seg2, lab2)
cell3, cyto3 = findCorrectLabel(img_seg3, lab3)

def find_tumors(img, cell, cyto, background):
  contours, heirarchy = cv2.findContours(np.uint8(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  n = len(contours)
  areas = []
  for cnt in contours:
    area = cv2.contourArea(cnt)
    areas.append(area)

  areas = np.array(areas)
  ind = np.argsort(-1*areas)
  thresh = np.mean(areas) + np.std(areas)
  z = np.zeros(img_seg1.shape)
  tumor = []
  check = 0

  for i in np.arange(0,n,1):
    z = np.zeros(img.shape)
    if(areas[i]>=thresh):
      cv2.drawContours(z,contours[i], -1,(255,255,255), 3 )
      masked_image = scipy.ndimage.morphology.binary_fill_holes(z)
      z[masked_image] = img[masked_image]
      counts = np.bincount(img_seg2.flatten())
      if(counts[cell] >= counts[cyto]):
        tumor.append(i)
        img[masked_image] = cell
      else:
        img[z == cyto] = background
        check = 1

  imgr = np.copy(img) 
  if(check):
    print("again")
    imgr = find_tumors(img, cell, cyto, background)

  return imgr

img_seg3_copy = np.copy(img_seg3)
imgr3 = find_tumors(img_seg3_copy, cell3, cyto3, background3)
fig, (p1,p2) = plt.subplots(1,2,figsize = (20,20))
p1.imshow(imgr3, cmap = 'gray')
p2.imshow(img_gt3)
plt.show()

"""Dice Score"""

num_clusters = 4
gray_values=[]
img_shape = img_gt_gray.shape
img_gt_gray.reshape(img_shape[0]*img_shape[1])
isolatedMask.reshape(img_shape[0]*img_shape[1])
for i in range(num_clusters-1):
  gray_values.append(int(np.mean(img_gt_gray[(img_gt_gray>=255*i/4) & (img_gt_gray<255*(i+1)/4)])))
gray_values.append(255)
print(gray_values)
for i in range(num_clusters):
  img_gt_gray[img_gt_gray==gray_values[i]]=i

gt_pixel_ratios=[]
seg_pixel_ratios=[]
for i in range(num_clusters):
  seg_pixel_ratios.append(np.sum(isolatedMask[isolatedMask==i]==i))
  gt_pixel_ratios.append(np.sum(img_gt_gray[img_gt_gray==i]==i))

print(seg_pixel_ratios)
print(gt_pixel_ratios)

seg_order = np.argsort(seg_pixel_ratios)
print(seg_order)

gt_order = np.argsort(gt_pixel_ratios)
print(gt_order)

for i in range(num_clusters):
  isolatedMask[isolatedMask==seg_order[i]]= -gt_order[i]
for i in range(num_clusters):
  isolatedMask[isolatedMask==(-i)]= i 
isolatedMask.reshape((img_shape[0],img_shape[1]))
plt.imshow(isolatedMask,cmap='gray')

img_gt_gray.reshape((img_shape[0],img_shape[1]))

dice = []
for k in range(num_clusters):
  dice.append(np.sum(isolatedMask[img_gt_gray==k]==k)*2.0 / (np.sum(isolatedMask[isolatedMask==k]==k) + np.sum(img_gt_gray[img_gt_gray==k]==k)))
print(dice)

"""HISTOGRAM"""

color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([lab3],[i],np.uint8(mask1),[255],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,255])
    print(i)
plt.show()

hist = cv2.calcHist([lab1],[1],np.uint8(mask2),[255],[0,256])
plt.plot(hist)
plt.xlim([0,255])
plt.show()
#a = np.correlate(hist.flatten(), hist.flatten(), mode = 'full')
print(np.argsort(-hist.flatten()))

plt.imshow(lab3[:,:,1], cmap = 'gray')
plt.show()

"""PCA"""

from sklearn.decomposition import PCA

pca = PCA(n_components = 10)
pca.fit(features.T)
X = pca.components_
var = pca.explained_variance_
print(var)
Xt = X.T

fig, (a1,a2,a3,a4) = plt.subplots(1,4,figsize = (25,25))
a1.imshow(X[0].reshape(1440,1920), cmap = 'gray')
a2.imshow(X[1].reshape(1440,1920), cmap = 'gray')
a3.imshow(X[2].reshape(1440,1920), cmap = 'gray')
a4.imshow(X[3].reshape(1440,1920), cmap = 'gray')
fig.show()

"""ANALYSIS"""

#Finding top n contours with maximum areas
n = len(contours1)
areas = []

for cnt in contours1:
  area = cv2.contourArea(cnt)
  areas.append(area)

areas = np.array(areas)
ind = np.argsort(-1*areas)


z = np.zeros(img_seg1.shape)
thresh = np.mean(areas)+np.std(areas)
for i in np.arange(0,n,1):
  if(areas[i]>=0):
    cv2.drawContours(z,contours1[i], -1,(255,255,255), 3 )

plt.imshow(z, cmap = 'gray')
plt.show()
print(thresh)

masked_image = scipy.ndimage.morphology.binary_fill_holes(z)
plt.imshow(masked_image, cmap = 'gray')
plt.show()
print(np.unique(masked_image))

mask = img_seg !=2
view = np.copy(lab)
view[mask] = 0
plt.figure(figsize = (15,15))
plt.imshow(view[:,:,0], cmap = 'gray')
plt.show()

masinv = img_seg != 2
mask1 = np.copy(justlab1)
mask1[masinv] = 0
mask1[img_seg == 2] = 255
plt.figure(figsize = (15,15))
#plt.imshow(mask1, cmap = 'gray')
hist = cv2.calcHist([view],[0], np.uint8(mask1), [256], [0,256] )
plt.plot(hist)
plt.show()

plt.figure(figsize = (15,15))
plt.hist(areas,len(areas))
plt.show()
print(np.mean(areas) + np.std(areas))

#Labelling the image

(labels, counts) = np.unique(img_seg[masked_image], return_counts= True)
cellClusterLabel = labels[np.argmax(counts)]
print(cellClusterLabel)
masked_img_inv = masked_image == False
backgroundMask = (img_seg == 0)
isolatedMask = ((img_seg *masked_img_inv) == 2).astype(int)
isolatedMask[masked_image] = 2

isolatedMask[backgroundMask] = 0

img_gt_gray = cv2.cvtColor(img_gt, cv2.COLOR_BGR2GRAY)

#Plotting correctly labelled Segmented Image
fig, (a1,a2,a3) = plt.subplots(1,3, figsize=(25,25))
a1.imshow(img)
a2.imshow(img_gt_gray, cmap = 'gray')
a3.imshow(isolatedMask, cmap = 'gray')
fig.show

#Calculate dice score 

dice = []
for k in (0,1,2):
  dice.append(np.sum(isolatedMask[img_gt==k])*2.0 / (np.sum(isolatedMask) + np.sum(img_gt)))

print(dice)

#Benign - 4x - 011
#img11 = np.copy(img)
#img_gt_gray11 = np.copy(img_gt_gray)
#isolatedMask11 = np.copy(isolatedMask)
#img_seg11 = np.copy(img_seg)
img11 = cv2.imread('benign_4x/_11001.tif')
fig, (a1,a2,a3, a4) = plt.subplots(1,4, figsize=(25,25))
a1.imshow(img11)
a2.imshow(img_gt_gray11, cmap = 'gray')
a3.imshow(isolatedMask11, cmap = 'gray')
a4.imshow(img_seg11)
fig.show
fig.savefig('b_011.png')

#Benign - 4x - 016
#img16 = np.copy(img)
#img_gt_gray16 = np.copy(img_gt_gray)
#isolatedMask16 = np.copy(isolatedMask)
#img_seg16 = np.copy(img_seg)
fig, (a1,a2,a3, a4) = plt.subplots(1,4, figsize=(25,25))
a1.imshow(img16)
a2.imshow(img_gt_gray16, cmap = 'gray')
a3.imshow(isolatedMask16, cmap = 'gray')
a4.imshow(img_seg16)
fig.show
fig.savefig('b_016.png')

#Benign - 4x - 064
#img64 = np.copy(img)
#img_gt_gray64 = np.copy(img_gt_gray)
#isolatedMask64 = np.copy(isolatedMask)
#img_seg64 = np.copy(img_seg_copy)
fig, (a1,a2,a3, a4) = plt.subplots(1,4, figsize=(25,25))
a1.imshow(img64)
a2.imshow(img_gt_gray64, cmap = 'gray')
a3.imshow(isolatedMask64, cmap = 'gray')
a4.imshow(img_seg64)
fig.show
fig.savefig('b_064.png')

#Malignant - 4x - 017
img17m = np.copy(img)
img_gt_gray17m = np.copy(img_gt_gray)
isolatedMask17m = np.copy(isolatedMask)
img_seg17m = np.copy(img_seg_copy)
fig, (a1,a2,a3, a4) = plt.subplots(1,4, figsize=(25,25))
a1.imshow(img17m)
a2.imshow(img_gt_gray17m, cmap = 'gray')
a3.imshow(isolatedMask17m, cmap = 'gray')
a4.imshow(img_seg17m)
fig.show
fig.savefig('m_017.png')

#Malignant - 4x - 018
img18m = np.copy(img)
img_gt_gray18m = np.copy(img_gt_gray)
isolatedMask18m = np.copy(isolatedMask)
img_seg18m = np.copy(img_seg_copy)
fig, (a1,a2,a3, a4) = plt.subplots(1,4, figsize=(25,25))
a1.imshow(img18m)
a2.imshow(img_gt_gray18m, cmap = 'gray')
a3.imshow(isolatedMask18m, cmap = 'gray')
a4.imshow(img_seg18m)
fig.show
fig.savefig('m_018.png')

#Malignant - 4x - 020
img20m = np.copy(img)
img_gt_gray20m = np.copy(img_gt_gray)
isolatedMask20m = np.copy(isolatedMask)
img_seg20m = np.copy(img_seg_copy)
fig, (a1,a2,a3, a4) = plt.subplots(1,4, figsize=(25,25))
a1.imshow(img20m)
a2.imshow(img_gt_gray20m, cmap = 'gray')
a3.imshow(isolatedMask20m, cmap = 'gray')
a4.imshow(img_seg20m)
fig.show
fig.savefig('m_020.png')

img1gnb = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img1g = cv2.GaussianBlur(img1gnb, (15,15), 5, 5)
val = np.ceil(np.mean(img1g) - np.std(img1g))
ret,imgthresh1 = cv2.threshold(img1g,val,255,cv2.THRESH_BINARY)
mask1 = imgthresh1 == 255
img1_clean = np.copy(img1)
img1_clean[mask1] = 255

img2gnb = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img2g = cv2.GaussianBlur(img2gnb, (15,15), 5, 5)
val = np.ceil(np.mean(img2g) - np.std(img2g))
ret,imgthresh2 = cv2.threshold(img2g,val,255,cv2.THRESH_BINARY)
mask2 = imgthresh2 == 255
img2_clean = np.copy(img2)
img2_clean[mask2] = 255

img3gnb = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
img3g = cv2.GaussianBlur(img3gnb, (15,15), 5, 5)
val = np.ceil(np.mean(img3g) - np.std(img3g))
ret,imgthresh3 = cv2.threshold(img3g,val,255,cv2.THRESH_BINARY)
mask3 = imgthresh3 == 255
img3_clean = np.copy(img3)
img3_clean[mask3] = 255


###

lab= cv2.cvtColor(img3, cv2.COLOR_BGR2LAB)
plt.imshow(lab)
plt.show()

#-----Splitting the LAB image to different channels-------------------------
l, a, b = cv2.split(lab)
plt.imshow(l, cmap ='gray')
plt.show()
plt.imshow(a, cmap= 'gray')
plt.show()
plt.imshow( b, cmap = 'gray')
plt.show()

#-----Applying CLAHE to L-channel-------------------------------------------
clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8))
cl = clahe.apply(l)
plt.imshow(cl)
plt.show()

#-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
limg = cv2.merge((cl,a,b))
plt.imshow(limg)
plt.show()

#-----Converting image from LAB Color model to RGB model--------------------
final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
plt.imshow(final)
plt.show()


###
#img1gnb = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#img1g = cv2.GaussianBlur(img1gnb, (15,15), 5, 5)
val = np.ceil(np.mean(l) - np.std(l))
ret,imgthresh1 = cv2.threshold(l,val,255,cv2.THRESH_BINARY)
mask1 = imgthresh1 == 255
imgcl_clean = np.copy(l)
imgcl_clean[mask1] = 255
imgcl_clean = cv2.medianBlur(imgcl_clean, 9)

#img2gnb = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#img2g = cv2.GaussianBlur(img2gnb, (15,15), 5, 5)
val = np.ceil(np.mean(a) + np.std(a))
ret,imgthresh2 = cv2.threshold(a,val,255,cv2.THRESH_BINARY_INV)
maska = imgthresh2 == 255
img1_clean = np.copy(a)
img1_clean[maska] = 0
img1m_clean = cv2.medianBlur(img1_clean, 9)

#img3gnb = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
#img3g = cv2.GaussianBlur(img3gnb, (15,15), 5, 5)
val = np.ceil(np.mean(b) - np.std(b))
ret,imgthresh3 = cv2.threshold(b,val,255,cv2.THRESH_BINARY)
mask3 = imgthresh3 == 255
imgb_clean = np.copy(b)
imgb_clean[mask3] = 255
imgb_clean = cv2.medianBlur(imgb_clean, 9)

#Extract Gabor Features

ksize = 9  # Size of Gabor kernel
theta = 0.0 
gamma = 1
sigma = 1
#converting to grayscale
#img_gray= cv2.cvtColor(img2_clean, cv2.COLOR_BGR2GRAY)
kernels = []
features = []
i = 0
for sigma in np.arange(1,1.2,0.5):
  for lamda in np.arange(3.25,4.1,0.25):
    for gamma in np.arange(0.5,1.25,0.25):
      k = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)   
      kernels.append(k) 
      fimg = cv2.filter2D(lab3, cv2.CV_8UC1, k)
      #fimg = cv2.GaussianBlur(fimg, (15,15), 5, 5)
      fimg = cv2.medianBlur(fimg, 5)
      #plt.imshow(fimg)
      #plt.show()
      plt.figure(figsize = (8,8))
      plt.imshow(fimg)
      plt.show()
      print(ksize, lamda, gamma, i)
      i = i+1
      #fimg = fimg.reshape((fimg.shape[0]*fimg.shape[1],))
      #features.append(fimg)
      #ColourImage
      #fimg = cv2.filter2D(imgHSV[:,:,2], cv2.CV_8UC1, k)
      #fimg = cv2.GaussianBlur(fimg, (15,15), 5, 5)
      #fimg = cv2.medianBlur(fimg, 11)

      fimg = fimg.reshape((fimg.shape[0]*fimg.shape[1],3))
      features.append(fimg[:,0])
      features.append(fimg[:,1])
      features.append(fimg[:,2])

transF3 = kmeans.transform(features3)
dist = transF3[:,2]
dist[y!=2] = 0
plt.hist(dist[dist!=0], 200)
plt.xlim([0,250])
#plt.plot(dist)
plt.show()

#dist[dist  60] = 0
ind_change = np.where(dist != 0)[0]
img_check = np.zeros(dist.shape)
listimg = lab3[:,:,1].reshape(lab3[:,:,1].shape[0]* lab3[:,:,1].shape[1],)
print(listimg.shape)
img_check[ind_change] = 255
img_check = img_check.reshape(img3.shape[0],img3.shape[1])
img_see = np.copy(lab3)
img_see[img_check == 0] = 0  
plt.figure(figsize = (20,20))
plt.imshow(img_see, cmap = 'gray')
plt.show()

counts = np.bincount(img_seg2.flatten())
background2 = np.argmax(counts)
if(background2):
  print("Changing 2")
  img_seg2[img_seg2 == background2] = 255
  img_seg2[img_seg2 == 0] = background2
  img_seg2[img_seg2 == 255] = 0

counts = np.bincount(img_seg3.flatten())
background3 = np.argmax(counts)
if(background3):
  print("Changing 3")
  img_seg3[img_seg3 == background3] = 255
  img_seg3[img_seg3 == 0] = background3
  img_seg3[img_seg3 == 255] = 0

#img2
clusters = np.unique(img_seg2)
clusters = clusters[1:]
mask1 = np.zeros(img_seg2.shape)
mask2 = np.zeros(img_seg2.shape)
mask1[img_seg2 == clusters[0]] = 255
mask2[img_seg2 == clusters[1]] = 255

hist1 = cv2.calcHist([lab2],[1],np.uint8(mask1),[255],[0,256])
peak1 = np.argsort(-hist1.flatten())[0]
hist2 = cv2.calcHist([lab2],[1],np.uint8(mask2),[255],[0,256])
peak2 = np.argsort(-hist2.flatten())[0]

if(peak1 > peak2):
  cell2 = clusters[0]
  cyto2 = clusters[1]
else:
  cell2 = clusters[1]
  cyto2 = clusters[0]

#Img3
clusters = np.unique(img_seg3)
clusters = clusters[1:]
mask1 = np.zeros(img_seg3.shape)
mask2 = np.zeros(img_seg3.shape)
mask1[img_seg3 == clusters[0]] = 255
mask2[img_seg3 == clusters[1]] = 255

hist1 = cv2.calcHist([lab3],[1],np.uint8(mask1),[255],[0,256])
peak1 = np.argsort(-hist1.flatten())[0]
hist2 = cv2.calcHist([lab3],[1],np.uint8(mask2),[255],[0,256])
peak2 = np.argsort(-hist2.flatten())[0]

if(peak1 > peak2):
  cell3 = clusters[0]
  cyto3 = clusters[1]
else:
  cell3 = clusters[1]
  cyto3 = clusters[0]