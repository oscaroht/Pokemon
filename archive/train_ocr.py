
import numpy as np
import os
import string
import sys


from skimage.io import imread
import PIL



from sklearn.model_selection import ShuffleSplit
from TFANN import ANNC

def LoadData(FP = '.'):
    '''
    Loads the OCR dataset. A is matrix of images (NIMG, Height, Width, Channel).
    Y is matrix of characters (NIMG, MAX_CHAR)
    FP:     Path to OCR data folder
    return: Data Matrix, Target Matrix, Target Strings
    '''
    TFP = os.path.join(FP, 'Train.csv')
    A, Y, T, FN = [], [], [], []
    with open(TFP) as F:
        for Li in F:
            FNi, Yi = Li.strip().split(',')  # filename,string
            T.append(Yi)
            A.append( np.expand_dims(imread(os.path.join(FP, FNi)),1) )                       # np.array( imread(os.path.join(FP, FNi)) ).reshape(8192,32,640, 3)  )
            Y.append(list(Yi) + [' '] * (MAX_CHAR - len(Yi)))  # Pad strings with spaces
            FN.append(FNi)
    return np.stack(A), np.stack(Y), np.stack(T), np.stack(FN)

CS = list(string.ascii_letters) + list(string.digits)
#Architecture of the neural network
NC = len(string.ascii_letters + string.digits + ' ')
MAX_CHAR = 64
IS = (64, 32, 640, 3)   #(14, 640, 3)       #Image size for CNN
ws = [('C', [4, 4,  3, NC // 2], [1, 2, 2, 1]), ('AF', 'relu'),
      ('C', [4, 4, NC // 2, NC], [1, 2, 1, 1]), ('AF', 'relu'),
      ('C', [8, 5, NC, NC], [1, 8, 5, 1]), ('AF', 'relu'),
      ('R', [-1, 64, NC])]



#Create the neural network in TensorFlow
cnnc = ANNC(IS, ws, batchSize = 64, learnRate = 5e-5, maxIter = 32, reg = 1e-5, tol = 1e-2, verbose = True)
#if not cnnc.RestoreModel('TFModel/', 'ocrnet'):

A,Y,T,FN = LoadData('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\derivatives')

cnnc.fit(A, Y)
#The predictions as sequences of character indices
YH = np.zeros((Y.shape[0], Y.shape[1]), dtype = np.int)
for i in np.array_split(np.arange(A.shape[0]), 32):
    YH[i] = np.argmax(cnnc.predict(A[i]), axis = 2)


#Convert from sequence of char indices to strings
PS = [''.join(CS[j] for j in YHi) for YHi in YH]
for PSi, Ti in zip(PS, T):
    print(Ti + '\t->\t' + PSi)


test=1