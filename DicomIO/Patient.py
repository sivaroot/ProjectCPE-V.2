
from pydicom.filereader import read_dicomdir
from os.path import dirname

class Patient:

    IndexPatientSelected = -1

    def __init__(self,filepath):
        self.filepath = filepath
        self.baseDir = dirname(self.filepath)
        self.dicomDir = read_dicomdir(self.filepath)
        self.patientRecords = self.dicomDir.patient_records

    def setPatientSelectedByIndex(self,index):
        Patient.IndexPatientSelected = index

    def getIndexPatientSelected(self):
        return Patient.IndexPatientSelected

    def getFilepath(self):
        return self.filepath
    
    def getBaseDir(self):
        return self.baseDir
    
    def getDicomDir(self):
        return self.dicomDir
    
    def getPatients(self):
        return self.patientRecords

    def getPatientChildren(self):
        if Patient.IndexPatientSelected  != -1:
            return self.getPatientByIndex(Patient.IndexPatientSelected).children
    
    def getPatientByIndex(self,index):
        lenRecord = len(self.patientRecords) 
        if self.checkIndexInRange(index) : 
            return self.dicomDir.patient_records[index]
        else :
            return -1
    def getPatientChildrenByIndex(self,index):
        lenRecord = len(self.patientRecords) 
        if self.checkIndexInRange(index) : 
            return self.dicomDir.patient_records[index].children
        else :
            return -1

    def getPatientIdByIndex(self,index):
        lenRecord = len(self.patientRecords) 
        if self.checkIndexInRange(index) : 
            return self.dicomDir.patient_records[index].PatientID
        else :
            return -1
    def getPatientNameByIndex(self,index):
        lenRecord = len(self.patientRecords) 
        if self.checkIndexInRange(index) : 
            return self.dicomDir.patient_records[index].PatientName
        else :
            return -1

    def checkIndexInRange(self,index):
        return index >=0 or index <  len(self.patientRecords)  
        