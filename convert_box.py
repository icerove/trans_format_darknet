import os
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
    else:
      for _ in range(n):
        xmin, ymin, xmax, ymax = np.fromfile(f, dtype=int, count=4, sep=" ")
        box = (xmin, xmax, ymin, ymax)
        bb = convert(size, b)
        output += str(0) + " " + " ".join([str(a) for a in bb]) + '\n'
  with open('labels/'+fn+'.txt','w') as output:
    f.write(output)

import random
random.shuffle(image_name)

def create_cross_validation_image_sets(image_name, train_indices, test_indices, k):
  with open('train_'+str(k)+'.txt') as f:
    for i in train_indices:
      f.write(os.getcwd()+"/gun_data/"+image_name[i]+".jpg")

  with open('test_'+str(k)+'.txt') as f:
    for i in test_indices:
      f.write(os.getcwd()+"/gun_data"+image_name[i]+".jpg")

from sklearn.model_selection import KFold
k_fold = KFold(n_splits=5)
k = 1
for train_indices, test_indices in k_fold.split(image_name):
  create_cross_validation_image_sets(image_name, train_indices, test_indices, k)
  k += 1
