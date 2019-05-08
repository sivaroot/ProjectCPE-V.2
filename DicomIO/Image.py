from os.path import join
from PIL import *
import pydicom
from PyQt5.QtGui import QPixmap,QImage
from PIL.ImageQt import ImageQt
from PIL import Image as PIL_Image

have_PIL = True
try:
    import PIL.Image
except ImportError:
    have_PIL = False

have_numpy = True
try:
    import numpy as np
except ImportError:
    have_numpy = False


class Image:

    IndexImageSelected = -1


    def __init__(self,serieChildren,base_dir):
        self.images = serieChildren
        self.image_files = [join(base_dir, *image.ReferencedFileID)for image in self.images]
        self.image_files = self.sortSliceLocation(self.image_files)

    def setImageSelectedByIndex(self,index):
        Image.IndexImageSelected = index

    def getIndexImageSelected(self):
        return Image.IndexImageSelected
    
    def getImageFiles(self):
        return self.image_files
        
    def getPILSelected(self):
        dataset = pydicom.dcmread(self.image_files[Image.IndexImageSelected])
        return self.get_PIL_image(dataset)
    
    def getQPixmapByIndexSelected(self):
        dataset = pydicom.dcmread(self.image_files[Image.IndexImageSelected])
        return QPixmap(
            QImage(
                ImageQt(
                    self.get_PIL_image(dataset).resize((396, 396),PIL_Image.ANTIALIAS))
                    ))
        
    # Bubble Sort algorithm 
    def sortSliceLocation(self,datasets):
        n = len(datasets)
        for i in range(n):
            for j in range(0,n-i-1):
                loc1 = float(pydicom.dcmread(datasets[j]).SliceLocation)
                loc2 = float(pydicom.dcmread(datasets[j+1]).SliceLocation)
                if loc1 > loc2:
                    datasets[j],datasets[j+1] = datasets[j+1],datasets[j] # Swap if the element found is greater
        
        return datasets
    
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