class Study:

    IndexStudySelected = -1

    def __init__(self,patientChildren):
        self.studies = patientChildren

    def setStudySelectedByIndex(self,index):
        Study.IndexStudySelected = index

    def getIndexStudySelected(self):
        return Study.IndexStudySelected
    
    def getStudyChildren(self):
        if Study.IndexStudySelected  != -1:
            return self.getStudyByIndex(Study.IndexStudySelected).children
    
    def getStudies(self):
        return self.studies

    def getStudyByIndex(self,index):
        if self.checkIndexInRange(index) : 
            return self.studies[index]

    def getStudyIdByIndex(self,index):
        if self.checkIndexInRange(index) : 
            return self.studies[index].StudyID

    def getStudyDescriptionByIndex(self,index):
        if checkIndexInRange(index) : 
            return self.studies[index].StudyDescription

    def checkIndexInRange(self,index):
        return index >=0 or index <  len(self.studies) 
