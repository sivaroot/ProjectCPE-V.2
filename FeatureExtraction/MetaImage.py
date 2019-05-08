import numpy as np
import pydicom
import cv2
from FeatureExtraction.ImageExtraction import *
from DicomIO.Image import *
class MetaImage:



    def writeMetaimage(self,imageFiles):
        slices = []
        

        for imageFile in imageFiles:
            data = pydicom.dcmread(imageFile)
            imageExtraction = ImageExtraction(self.get_PIL_image(data))
            imgArray = np.array(imageExtraction.kMeanExtraction(mode=1))
            BGR = cv2.cvtColor(imgArray, cv2.COLOR_RGB2BGR)
            imageGray = cv2.cvtColor(BGR,cv2.COLOR_BGR2GRAY)
            ret,thresh1 = cv2.threshold(imageGray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            slices.append(thresh1)
            del imageExtraction
        
        slices = np.array(slices).transpose(2,1,0) 
        self.writeMHA('FullHead.mha',imageFiles,slices.shape)
        print('FullHead.mha shape : ',slices.shape)
        slices = slices.flatten('F').astype('short')
        slices.tofile('FullHead.raw')

    def writeMHA(self,fn,datasets,dimSize):
            
        dataset = pydicom.dcmread(datasets[0])
        sliceThickness = dataset.SliceThickness
        spacing = dataset.PixelSpacing
        print(dimSize)

    
        if fn.endswith('.mha'):
            f=open(fn, 'w')
            f.write('ObjectType = Image\n')
            print("ObjectType = Image")
            f.write('NDims = 3\n')
            print("NDims = 3")
            f.write('BinaryData = True\n')
            print("BinaryData = True")
            f.write('BinaryDataByteOrderMSB = False\n')
            print("BinaryDataByteOrderMSB = False")
            f.write('CompressedData = False\n')
            print("CompressedData = False")
            f.write('TransformMatrix = -1 0 0 0 1 0 0 0 -1\n')
            print("TransformMatrix = -1 0 0 0 1 0 0 0 -1")
            f.write('Offset = 0 0 0\n')
            print("Offset = 0 0 0")
            f.write('CenterOfRotation = 0 0 0\n')
            print("CenterOfRotation = 0 0 0")
            f.write('AnatomicalOrientation = LAS\n')
            print("AnatomicalOrientation = LAS")
            f.write('ElementSpacing = %.4f %.4f %.1f\n'%(spacing[0],spacing[1],sliceThickness))
            print('ElementSpacing = %.4f %.4f %.1f'%(spacing[0],spacing[1],sliceThickness))
            f.write('ITK_InputFilterName = MetaImageIO\n')
            print("ElementType = MET_SHORT")
            f.write('DimSize = %d %d %d\n'%(dimSize[0],dimSize[1],dimSize[2]))
            print('DimSize = %d %d %d'%(dimSize[0],dimSize[1],dimSize[2]))
            f.write('ElementType = MET_SHORT\n')
            print("ElementType = MET_SHORT")
            f.write('ElementDataFile = %s\n'%fn.replace('.mha','.raw'))
            print('ElementDataFile = %s'% fn.replace('.mha','.raw'))
            f.close()
        elif not fn.endswith('.mha'): ## File extension is not ".mha"
            raise NameError('The input file name is not a mha file!')
    def get_LUT_value(self,data, window, level):
        """Apply the RGB Look-Up Table for the given data and window/level value."""
        if not have_numpy:
            raise ImportError("Numpy is not available. See http://numpy.scipy.org/"
                            " to download and install")

        return np.piecewise(data,
                            [data <= (level - 0.5 - (window - 1) / 2),
                            data > (level - 0.5 + (window - 1) / 2)],
                            [0, 255, lambda data: ((data - (level - 0.5)) \
                            / (window - 1) + 0.5) * (255 - 0)])
    
    def get_PIL_image(self,dataset):
        """Get Image object from Python Imaging Library(PIL)"""
        if not have_PIL:
            raise ImportError("Python Imaging Library is not available. "
                            "See http://www.pythonware.com/products/pil/ "
                            "to download and install")

        if ('PixelData' not in dataset):
            raise TypeError("Cannot show image -- DICOM dataset does not have "
                            "pixel data")
        # can only apply LUT if these window info exists
        if ('WindowWidth' not in dataset) or ('WindowCenter' not in dataset):
            bits = dataset.BitsAllocated
            samples = dataset.SamplesPerPixel
            if bits == 8 and samples == 1:
                mode = "L"
            elif bits == 8 and samples == 3:
                mode = "RGB"
            elif bits == 16:
                # not sure about this -- PIL source says is 'experimental'
                # and no documentation. Also, should bytes swap depending
                # on endian of file and system??
                mode = "I;16"
            else:
                raise TypeError("Don't know PIL mode for %d BitsAllocated "
                                "and %d SamplesPerPixel" % (bits, samples))

            # PIL size = (width, height)
            size = (dataset.Columns, dataset.Rows)

            # Recommended to specify all details
            # by http://www.pythonware.com/library/pil/handbook/image.htm
            im = PIL.Image.frombuffer(mode, size, dataset.PixelData,
                                    "raw", mode, 0, 1)

        else:
            image = self.get_LUT_value(dataset.pixel_array, dataset.WindowWidth,
                                dataset.WindowCenter)
            # Convert mode to L since LUT has only 256 values:
            #   http://www.pythonware.com/library/pil/handbook/image.htm
            im = PIL.Image.fromarray(image).convert('L')

        return im
            