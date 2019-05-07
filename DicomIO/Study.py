class Study:

    def __init__(self,patientChildren):
        self.studies = patientChildren
    
    def getStudies(self):
        return self.studies

    def getStudyIdByIndex(self,index):
        if self.checkIndexInRange(index) : 
            return self.studies[index].StudyID

    def getStudyDescriptionByIndex(self,index):
        if checkIndexInRange(index) : 
            return self.studies[index].StudyDescription

    def checkIndexInRange(self,index):
        return index >=0 or index <  len(self.studies) 
