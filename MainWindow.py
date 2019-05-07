from PyQt5.QtWidgets import QWidget,QTableWidget, QApplication, QMainWindow, QFileDialog, QPushButton,QHeaderView,QTableWidgetItem,QListView
from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import *
from DicomIO.Patient import *
from DicomIO.Study import *
from DicomIO.FileDialog import *
class MainWindow(object):

    patient = None
    study = None
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1152, 648)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.button = QPushButton('Open DICOM', self.centralwidget)
        self.button.setToolTip('Open the DICOM file or DICOMDIR')
        self.button.setFixedSize(100, 25)
        self.button.move(15, 15)
        self.button.clicked.connect(self.setPatientView)

        self.btnMetafile = QPushButton('Gen Metaimage', self.centralwidget)
        self.btnMetafile.setToolTip('Generate Metaimage')
        self.btnMetafile.setFixedSize(190, 50)
        self.btnMetafile.move(945, 461)
        self.btnMetafile.clicked.connect(self.writeMetaimage)

        self.patientView = QtWidgets.QListView(self.centralwidget)
        self.patientView.setGeometry(QtCore.QRect(15, 50, 300, 70))
        self.patientView.setObjectName("patientView")
        self.patientModel = QtGui.QStandardItemModel()
        self.patientView.setModel(self.patientModel)
        self.patientView.clicked[QtCore.QModelIndex].connect(self.setStudyView)

        self.studyView = QtWidgets.QListView(self.centralwidget)
        self.studyView.setGeometry(QtCore.QRect(15, 130, 300, 120))
        self.studyView.setObjectName("studyView")
        self.studyModel = QtGui.QStandardItemModel()
        self.studyView.setModel(self.studyModel)
        self.studyView.clicked[QtCore.QModelIndex].connect(self.setSeriesView)

        self.seriesView = QtWidgets.QListView(self.centralwidget)
        self.seriesView.setGeometry(QtCore.QRect(15, 260, 300, 150))
        self.seriesView.setObjectName("seriesView")
        self.seriesModel = QtGui.QStandardItemModel()
        self.seriesView.setModel(self.seriesModel)
        self.seriesView.clicked[QtCore.QModelIndex].connect(self.setImagesView)


        self.imagesView = QtWidgets.QListView(self.centralwidget)
        self.imagesView.setGeometry(QtCore.QRect(15,420,300,210))
        self.imagesView.setObjectName("imagesView")
        self.imagesModel = QtGui.QStandardItemModel()
        self.imagesView.setModel(self.imagesModel)
        self.imagesView.clicked[QtCore.QModelIndex].connect(self.setDicomView)

        self.dicomView = QtWidgets.QLabel(self.centralwidget)
        self.dicomView.setGeometry(QtCore.QRect(330, 50, 396, 396))
        self.dicomView.setObjectName("dicomView")

        self.segmentView = QtWidgets.QLabel(self.centralwidget)
        self.segmentView.setGeometry(QtCore.QRect(741,50,396,396))
        self.segmentView.setObjectName('segmentView')

        self.logView = QtWidgets.QListView(self.centralwidget)
        self.logView.setGeometry(QtCore.QRect(330,461,600,172))
        self.logView.setObjectName("imagesView")
        self.logModel = QtGui.QStandardItemModel()
        self.logView.setModel(self.logModel)
      
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralwidget)
        self.vtkWidget.setGeometry(QtCore.QRect(741,50,396,396))

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Computer Engineering Project I - Dicom processing"))

    def getMainWindow(self):
        return self.MainWindow
    
    
    
    def setPatientView(self):
        dialog = FileDialog()
        filepath = dialog.openFileNameDialog(title="Open DICOMDIR",typeFile=FileDialog.CS_DICOMDIR)
        del dialog
        if filepath:
            self.patient = Patient(filepath)
            for patient in self.patient.getPatients():
                ID = patient.PatientID
                NAME = str(patient.PatientName).replace('^',' ')
                it = QtGui.QStandardItem("%s\t%s"%(ID,NAME))
                self.patientModel.appendRow(it)
        

    
    def setStudyView(self,index):
        self.studyModel.clear()
        self.patient.setPatientSelectedByIndex(self.patientModel.itemFromIndex(index).index().row())
        self.study = Study(self.patient.getPatientChildrenByIndex(self.patient.getIndexPatientSelected()))
        for study in self.study.getStudies():
            StudyID = study.StudyID
            StudyDescription = study.StudyDescription
            it = QtGui.QStandardItem("%s\t%s"%(StudyID,StudyDescription))
            self.studyModel.appendRow(it)

    def setSeriesView(self):

        return 0

    def setImagesView(self):

        return 0
    
    def setDicomView(self):

        return 0
    
    def writeMetaimage(self):

        return 0