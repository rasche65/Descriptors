"""
Reading attribute arrays (for an entire collection) and histogram-
of-attributes.
"""
import struct
import numpy as np

# FFFFFFFFFFFFFFFFFFFFF   Unpack1AttFlt   FFFFFFFFFFFFF
# The following three functions load one attribute (column):
# one for float type, one for int type and one for
# uint8 type
def Unpack1AttFlt(fo, nDsc):
    A = np.zeros((nDsc), dtype=float)
    for i in range(0,nDsc):
        A[i] = struct.unpack('f', fo.read(4))[0]
    return A

def Unpack1AttInt(fo, nDsc):
    A = np.zeros((nDsc), dtype=int)
    for i in range(0,nDsc):
        A[i] = int.from_bytes(fo.read(4),'little')
    return A

def Unpack1AttUin(fo, nDsc):
    A = np.zeros((nDsc), dtype=np.uint8)
    for i in range(0,nDsc):
        A[i] = int.from_bytes(fo.read(1),'little')
    return A

""" FFFFFFFFFFFFFFFFFFFFF   LoadDscCont   FFFFFFFFFFFFFFF
Loads attributes & info for contours as a structure. Most
attributes are float values. Uses the 3 functions above to 
unpack the values. 
      
Note 1: RGB values (.Crm) were written [RGBRGB] and not
         as [RRGGBB], hence we reshape
Note 2: different indexing for labels and categories
    
   S.Attributes [nDsc]  (RGB as [3 nDsc])
   S.IxImg [nDsc 1] E [0..nImg-1] (0-indexing)
   S.LbCat [nDsc 1] E [1..nCat]   (1-indexing)
   S.Lev   [nDsc 1] E [0..nLev-1] (0-indexing)

    USE    DSC = LoadDscRawGen('C:\IMG\DSC\', 'RDG')
"""
def LoadDscCont(filePath, dty):
    class S:    # returning as structure
        pass    
    
    fo   = open(filePath+'RAW_'+dty, 'rb')
    
    # =====  Header  =====
    nDsc = int.from_bytes(fo.read(4),'little')
    #nDim = int.from_bytes(fo.read(4),'little')
    
    # =====  Vectors  =====
    #S.VEC  = np.zeros((nDsc,nDim), dtype=float, order='C')
    #for i in range(0,nDsc):
    #    for j in range(0,nDim):
    #        S.VEC[i][j] = struct.unpack('f', fo.read(4))[0]
    
    # =====  Attributes   =====
    S.Len   = Unpack1AttFlt(fo, nDsc)
    S.Str   = Unpack1AttFlt(fo, nDsc)

    S.Ori   = Unpack1AttFlt(fo, nDsc)
    S.PosV  = Unpack1AttFlt(fo, nDsc)
    S.PosH  = Unpack1AttFlt(fo, nDsc)
    
    S.Red   = Unpack1AttFlt(fo, nDsc)
    S.Grn   = Unpack1AttFlt(fo, nDsc)
    S.Blu   = Unpack1AttFlt(fo, nDsc)

    # =====  Zugehoer  =====
    S.IxImg = Unpack1AttInt(fo, nDsc) # image index
    S.LbCat = Unpack1AttInt(fo, nDsc) # category label
    S.Lev   = Unpack1AttUin(fo, nDsc) # (pyramid) level (or scale)
    
    # =====  Trailer  =====
    S.nGeo = int.from_bytes(fo.read(4),'little')
        
    fo.close()
    
    return S 

""" FFFFFFFFFFFFFFFFFFFFF   LoadHstFlat  FFFFFFFFFFFFFFF
Loads histograms as integer values. The variable nBin is loaded for
info only, it is not necessary for proper loading the matrix.

   USE    HST, nBin = LoadHstFlat(filePathHst, 'RDG')
"""
def LoadHstFlat(filePath, dty):
    
    fo   = open(filePath+'H_'+dty, 'rb')
    
    # =====  Header  =====
    nImg = int.from_bytes(fo.read(4),'little')
    nDim = int.from_bytes(fo.read(4),'little')
    nBin = int.from_bytes(fo.read(4),'little')

    # =====  Vectors  =====
    HST  = np.zeros((nImg,nDim), dtype=int, order='C')
    for i in range(0,nImg):
        for j in range(0,nDim):
            HST[i][j] = int.from_bytes(fo.read(4),'little')
    
    fo.close()
    
    return HST, nBin 
