# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 18:46:38 2022

@author: epick
"""
from matplotlib import pyplot as plt

import cv2 
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import os
import postprocessing
import sys 

image_path  = "C:/Users/epick/My project/Assets/Snapshots"

if not(len(sys.argv)==1) :
   image_path = sys.argv[1]
files = os.listdir(image_path)

for fi in files[:]: # removes non-png
    if not(fi.endswith(".png")):
        files.remove(fi)
print(files)

images =  [cv2.imread(image_path + '/' + file) for file in files]

string= postprocessing.ocr_handler(images,[True,43],config='--oem 3 -c tessedit_char_whitelist=0123456789CSX. --psm 7')
print(string)
plt.imshow(images[0])
string= postprocessing.string_filter(string)
print(string)
with open('string.txt', 'w') as f:
    f.write(string)

