import numpy as np
import cv2
from PyQt5.QtGui import QPixmap,QImage
from PIL.ImageQt import ImageQt
from PIL import Image as PILImage
class ImageExtraction:

    def __init__(self,imagePIL):
        self.imageArr = self.convertPIL2Array(imagePIL)
        self.imageBgr = self.convertArray2BGR(self.imageArr)

    def convertPIL2Array(self,imagePIL):
        return np.array(imagePIL)

    def convertArray2BGR(self,imageArr):
        return cv2.cvtColor(imageArr, cv2.COLOR_RGB2BGR)
   
    def kMeanExtraction(self,mode=0):
        img = cv2.cvtColor(self.imageArr, cv2.COLOR_RGB2BGR)
        img = cv2.blur(img,(3,3))
        Z = img.reshape((-1,3))

        Z = np.float32(Z)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 3
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)
        cenTranspose = center.transpose()[0]
        indexMax = np.argmax(cenTranspose)
        indexMin = np.argmin(cenTranspose)
       
        labelf = label.flatten()
        labelf[labelf != indexMax] = indexMin

        res = center[labelf]
        res2 = res.reshape((img.shape))
        # ret,thresh = cv2.threshold(res2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        image_PIL = PILImage.fromarray(res2)
        
        if mode == 0:
            return QPixmap(QImage(ImageQt(image_PIL.resize((396, 396),PILImage.ANTIALIAS))))
        else:
            return image_PIL
        
       
