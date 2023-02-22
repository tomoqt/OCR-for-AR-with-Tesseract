# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 18:41:20 2022

@author: epick
"""
#import re
#import cv2 
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#from Bio import SeqIO
from Bio.Align import MultipleSeqAlignment
#from pytesseract import Output
#from matplotlib import pyplot as plt
#from Bio import pairwise2
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
#import pkg_resources
import preprocessing

def ocr_handler (images,thresh = [False,0] ,denoise= [False,0],config='--oem 1 -c tessedit_char_whitelist=0123456789 --psm 7'): #maybe pre-processing could be optional
  #images = pre_process(images)
  #inserire test per il format di thresh e denoise
  images=preprocessing.pre_processing(images,thresh,denoise)
  strings = [(pytesseract.image_to_string(image, config=config).strip('\n\x0c').strip('C.S.X.').strip('0.').strip('9.')) for image in images]
  return strings


def aligner(strings):
  '''
  we pairwise align the strings to the longest one ( we assume the strings are somehow similar, and the longest one caputerd the most information)
  '''

  
  longest_length = max(len(s) for s in strings)
  sequences = [s.ljust(longest_length, '-') for s in strings]
  
  sequences = list(map(Seq,sequences))
  sequences=list(map(SeqRecord,sequences))
  aligned = MultipleSeqAlignment(sequences)#[pairwise2.align.globalxx(sequences[n-1], i ,gap_char='-',one_alignment_only = True)[0].seqB for i in sequences[:n] ]
  return aligned


def string_to_ascii (string):
    return[ord(i) for i in string]
        
def ascii_to_string (L):
    return ''.join(chr(i) for i in L)

#function taking in aligned strings and outputting a single, aggregated string representing the majority vote foor each entry 
def string_voter(strings):

    strings = [np.asarray(string_to_ascii(j)) for j in strings] 
    return ascii_to_string([np.bincount(np.asarray(strings)[:,i]).argmax() for i in range(len(strings[0]))])

#remove unwanted letters, replace them w/ blanks
def letter_filter(string):
    copy=[]
    for (i,s) in enumerate(string [:]) : 
        if (not(s.isdigit())):
            copy.append('0') # continue we are directly removing characters, without substitution
        else:
            copy.append(string[i])
    return ''.join(copy)

def range_filter(string): 
    for i in range(len(string),5,-1): 
        if (int(string[i-5:i])<79999 and int(string[i-5:i])>61000): #should work backwards!
            return (string[i-5:i])
    return('-----')
        #must think of a way of removing blanks
def string_filter (strings , length_check = 5, range_string = [61000,79999]):


    processed = list(map(letter_filter,strings))
    print(strings)
    processed = list(map(range_filter,processed))
    return string_voter(aligner(processed))