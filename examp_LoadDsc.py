"""
"""
import numpy as np
from LoadDscRaw import LoadDscCont, LoadHstFlat

filePathDsc = 'C:\IMGdat\OLTO\C\DSCall\\'
dty         = 'RDG'

#%% --------------   Descriptor Attributes    ------------
DSC = LoadDscCont(filePathDsc, dty)

# we concatenate some attributes:
RDG = np.vstack((DSC.Len, DSC.Str, DSC.Ori)) # [nAtt ntDsc]
RDG = RDG.transpose()                        # [ntDsc nAtt]
RDG = np.hstack((RDG, DSC.Crm))              # [ntDsc nAtt+3]
(ntDsc, nAtt) = RDG.shape;

print('RDG atts: ', ntDsc, 'ntDsc x', nAtt, 'atts')

RDG.max(axis=0)
RDG.min(axis=0)

print('#img ', DSC.IxImg.max())
print('#cat ', DSC.LbCat.max())
print('#lev ', DSC.Lev.max())

#%% --------------   Hist-Of-Atts    ------------
filePathHst = 'C:\IMGdat\OLTO\C\LHST\\'

HST, nBin = LoadHstFlat(filePathHst, dty)

(nImg, nDim) = HST.shape;
print('RDG hist: ', nImg, 'img x', nDim, 'dims')

