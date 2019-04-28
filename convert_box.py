import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil
import numpy as np
import cv2

sets=[]

classes = ["gun"]

file_name = []
for root, dirs, files in os.walk("gun_data"):  
  for filename in files:
    file_name.append(filename)

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

image_name = []
for fn in file_name:
  if ".jpg" in fn:
    image_name.append(fn[:-4])

for fn in image_name:
  oriimg = cv2.imread('gun_data/'+fn+'.jpg',cv2.IMREAD_UNCHANGED)
  size = oriimg.shape[1], oriimg.shape[0]

  output = ''
  with open('gun_data/'+fn+'.txt','r') as f:
    try:
      n = int(f.readline())
    except Exception:
      pass
    for _ in range(n):
      xmin, ymin, xmax, ymax = np.fromfile(f, dtype=int, count=4, sep=" ")
      box = (xmin, xmax, ymin, ymax)
      bb = convert(size, b)
      output += str(0) + " " + " ".join([str(a) for a in bb]) + '\n'
  with open('gun_data/'+fn+'.trans.txt','w') as output:
    f.write(output)

import random
random.shuffle(image_name)

def copy_image_and_annot_dir(image_name, train_indices, test_indices, k):
  train_img = 'gun_data_cross_validation/'+str(k)+"/"+"train_img/"
  train_annot = 'gun_data_cross_validation/'+str(k)+"/"+"train_annot/"
  test_img = 'gun_data_cross_validation/'+str(k)+"/"+"test_img/"
  test_annot = 'gun_data_cross_validation/'+str(k)+"/"+"test_annot/"

  os.makedirs(train_img)
  os.makedirs(train_annot)
  os.makedirs(test_img)
  os.makedirs(test_annot)
  
  for i in train_indices:
    shutil.copyfile('gun_data/'+image_name[i]+'.jpg',
                    train_img+image_name[i]+'.jpg')
    shutil.copyfile('gun_data/'+image_name[i]+'.trans.txt',
                    train_annot+image_name[i]+'.trans.txt')
  for i in test_indices:
    shutil.copyfile('gun_data/'+image_name[i]+'.jpg',
                    test_img+image_name[i]+'.jpg')
    shutil.copyfile('gun_data/'+image_name[i]+'.trans.txt',
                    test_annot+image_name[i]+'.trans.txt')


from sklearn.model_selection import KFold
k_fold = KFold(n_splits=5)
k = 1
for train_indices, test_indices in k_fold.split(image_name):
  copy_image_and_annot_dir(image_name, train_indices, test_indices, k)
  k += 1

