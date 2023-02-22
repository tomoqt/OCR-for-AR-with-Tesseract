# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 18:33:21 2022

@author: epick
"""
#import re
import cv2 
#import numpy as np
from matplotlib import pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



# preprocessing
def denoise(radius,images):
  images = [cv2.GaussianBlur(image, (radius,radius), 0) for image in images ]
  return images

def threshold(level,images):
    
  images = [ cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), level , 255, 0)[1] for image in images ] #image is fed in gray scale 
  return images

def adaptive_threshold(images):
    
  images = [ cv2.adaptiveThreshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,45,0.7) for image in images ] #image is fed in gray scale 
  return images


def pre_processing (images, thresholding, denoising ): 
  # both parameters take a tuple containing a boolean and a number parametrizing the effect of the filtering
  if (denoising[0]):
    if ((denoising[1]) < 0 ):
      print('Warning: the selected radius for denoising is negative, hence the absolute value is taken')
      denoising[1]=abs(denoising[1])
    images = denoise(denoising[1],images) 

  if (thresholding[0]):
      if (type(thresholding[1]) != int):
        print('The level must be an integer')
        return 0
      if ((thresholding[1]) < 0 ):
        print('Warning: the selected threshold level is negative, hence the absolute value is taken')
        thresholding[1]=abs(thresholding[1])   
      if ((thresholding[1]) > 255 ):
        print('Warning: the selected threshold level is above 255, a threshold of level 255 is used instead ')
        thresholding[1]=255   
    
      images = threshold(thresholding[1],images) 
  if (not(thresholding[0]) and thresholding[1]==0 ):  
      images = adaptive_threshold(images)

  print("hello")
  return images


##############################







