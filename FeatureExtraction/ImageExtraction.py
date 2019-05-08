import numpy as np
import cv2
from PyQt5.QtGui import QPixmap,QImage
from PIL.ImageQt import ImageQt
from PIL import Image as PILImage
class ImageExtraction:

    def __init__(self,imagePIL):
        self.imageArr = self.convertPIL2Array(imagePIL)
        self.imageBgr = self.convertArray2BGR(self.imageArr)
        self.kMeanExtraction(self.imageBgr)

    def convertPIL2Array(self,imagePIL):
        return np.array(imagePIL)

    def convertArray2BGR(self,imageArr):
        return cv2.cvtColor(imageArr, cv2.COLOR_RGB2BGR)
    


    def kMeanExtraction(self,PIL_Image):
        img = cv2.cvtColor(np.array(PIL_Image), cv2.COLOR_RGB2BGR)
        img = cv2.blur(img,(3,3))
        # img = cv2.imread('home.jpg')
        Z = img.reshape((-1,3))

        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 3
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        cenTranspose = center.transpose()[0]
        indexMax = np.argmax(cenTranspose)
        indexMin = np.argmin(cenTranspose)
       
        labelf = label.flatten()
        labelf[labelf != indexMax] = indexMin

        res = center[labelf]
        res2 = res.reshape((img.shape))
        image_PIL = PILImage.fromarray(res2).resize((396, 396),PILImage.ANTIALIAS)
        return QPixmap(QImage(ImageQt(image_PIL)))
        # cv2.imshow('res2',res2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()