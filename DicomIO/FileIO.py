from os.path import dirname
from pydicom.filereader import read_dicomdir

class FileIO:
    
    def __init__(self,filePath):
        self.filePath = filePath
        self.baseDir = dirname(self.filePath)
        self.dicomDir = read_dicomdir(self.filePath)
    
    def getFilePath(self):
        return self.filePath
    
    def getBaseDir(self):
        return self.baseDir

    def getDicomDir(self):
        return self.dicomDir
