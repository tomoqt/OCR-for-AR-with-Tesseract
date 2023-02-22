

import re
import cv2 
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#from Bio import SeqIO
from Bio.Align import MultipleSeqAlignment
#from pytesseract import Output
from matplotlib import pyplot as plt
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

#import pkg_resources
print(pytesseract.get_tesseract_version() )
"""# Example"""

path = 'C:/Users/epick/OneDrive/Desktop/uni/Magistrale_primo_anno/Challenge/pics/pics3/Immagine 2022-04-29 192823.png'
image = cv2.imread(path)
image1=cv2.imread(path)
custom_config ='--oem 1  --psm 7 '


"""# Pre-processing functions"""

def denoise(radius,images):
  images = [cv2.GaussianBlur(image, (radius,radius), 0) for image in images ]
  return images

def adaptive_threshold(images):
    
  images = [ cv2.adaptiveThreshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,45,0.7) for image in images ] #image is fed in gray scale 
  return images

def threshold(level,images):
    
  images = [ cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), level , 255, 0)[1] for image in images ] #image is fed in gray scale 
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
    
      images = threshold(thresholding[1],images) 
  if (not(thresholding[1]) and thresholding[1]==0 ):  
      images = adaptive_threshold(images)
         
  return images

"""
```

# OCR"""

custom_config ='--oem 1 -c tessedit_char_whitelist=0123456789 --psm 6'
#remember deskewing
#we want to build a python script containing a list of png images, capable of performing pre-processing on each, aswell as aggrgating extracted strings toghether.
def ocr_handler (images,thresh = [False,0] ,denoise= [False,0]): #maybe pre-processing could be optional
  #images = pre_process(images)
  #inserire test per il format di thresh e denoise
  images=pre_processing(images,thresh,denoise)
  
  plt.imshow(images[0])
  strings = [(pytesseract.image_to_string(image, config=custom_config).strip('\n\x0c')) for image in images]
  return strings

images_example = [cv2.imread(path) for i in range(10)]

examples=ocr_handler(images_example)    
#print(examples)

a= ['caccc','asdac','as']
#print(sorted(a, key=len))

"""# Alignment and post-processing"""

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

print(aligner(examples))



# Creating sample sequences
seq1 = Seq("ACCGT")
seq2 = Seq("ACG")
  
# Finding similarities
alignments = pairwise2.align.globalxx(seq1, seq2,gap_char='-' ,one_alignment_only = True)

# Showing results
for match in alignments:
    print(match.seqB)
    print(match.seqA)

#si potrebbe allineare la più lunga e poi tutte con quella, poi andare a maggioranza ( in realtà si dovrebbero allineare tutte le èossibile coppie e scegliere quella col fit migliore?? ma sicuramente ci vuole un botto )

#b=aligner(a)
#print(b)

images= [cv2.imread("C:/Users/epick/OneDrive/Desktop/uni/Magistrale primo anno/Challenge/pics/1.jpeg"),cv2.imread("C:/Users/epick/OneDrive/Desktop/uni/Magistrale primo anno/Challenge/pics/2.jpeg"),cv2.imread("C:/Users/epick/OneDrive/Desktop/uni/Magistrale primo anno/Challenge/pics/3.jpeg")]
ciao=ocr_handler(images,[True,50],[False,0])


test = ['cciao',' biai',' bbai']

def string_to_ascii (string):
    return[ord(i) for i in string]
        
def ascii_to_string (L):
    return ''.join(chr(i) for i in L)

#function taking in aligned strings and outputting a single, aggregated string representing the majority vote foor each entry 
def string_voter(strings):

    strings = [np.asarray(string_to_ascii(j)) for j in strings] 
    return ascii_to_string([np.bincount(np.asarray(strings)[:,i]).argmax() for i in range(len(strings[0]))])

aligned = aligner(ciao)
print([aligned[i,:].seq.__str__() for i in range(int(len(ciao)))])
aligned= (string_voter(([aligned[i,:].seq.__str__() for i in range(len(ciao))])))
print(aligned)

#function filtering ranges

def range_filter(string): 
    for i in range(len(string)): 
        if (int(string[i:i+5])<79999 and int(string[i:i+5])>61000):
            return (string[i:i+5])
    return('-----')
        
def string_filter (strings , length_check = 5, range_string = [61000,79999]):
    processed = list(map(range_filter,strings))
    return string_voter(aligner(processed))

def letter_filter(string):
    copy=[]
    for (i,s) in enumerate(string [:]) : 
        if (not(s.isdigit())):
            continue # copy.append('-')
        else:
            copy.append(string[i])
    return ''.join(copy)
                
a= ['888868512432','1234568512432','8454468512432','685124327777']
b = 'abcd1234656'
string_filter(a)
letter_filter(b)
