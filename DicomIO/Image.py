from os.path import join
import pydicom
class Image:

    IndexImageSelected = -1


    def __init__(self,serieChildren,base_dir):
        self.images = serieChildren
        self.image_filenames = [join(base_dir, *image.ReferencedFileID)for image in self.images]
        self.image_filenames = self.sortSliceLocation(self.image_filenames)

    def setStudySelectedByIndex(self,index):
        Image.IndexImageSelected = index

    def getIndexStudySelected(self):
        return Image.IndexImageSelected
    
    def getImage_filenames(self):
        return self.image_filenames

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