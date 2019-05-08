from PyQt5.QtWidgets import QWidget,QTableWidget, QApplication, QMainWindow, QFileDialog, QPushButton,QHeaderView,QTableWidgetItem,QListView
from PyQt5 import QtCore, QtGui, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import *
from DicomIO.FileIO import *
from DicomIO.Patient import *
from DicomIO.Study import *
from DicomIO.Serie import *
from DicomIO.Image import *
from DicomIO.FileDialog import *
from FeatureExtraction.ImageExtraction import *
from FeatureExtraction.MetaImage import *
from Render.VolumeRender import *
import vtk
class MainWindow(object):

    fileIO = None
    patient = None
    study = None
    serie = None
    image = None
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
        self.dicomView.setStyleSheet("background-color:#000000;")
       
        self.logView = QtWidgets.QListView(self.centralwidget)
        self.logView.setGeometry(QtCore.QRect(330,461,600,172))
        self.logView.setObjectName("imagesView")
        self.logModel = QtGui.QStandardItemModel()
        self.logView.setModel(self.logModel)
      
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralwidget)
        self.vtkWidget.setGeometry(QtCore.QRect(741,50,396,396))
        self.vtkWidget.setStyleSheet("background-color:#000000;")
        self.ren1 = vtk.vtkRenderer()
        self.ren1.SetBackground(0,0,0)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren1)
        iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        iren.Start()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Computer Engineering Project I - Dicom processing"))

    def getMainWindow(self):
        return self.MainWindow
     
    def setPatientView(self):
        self.patientModel.clear()
        dialog = FileDialog()
        filepath = dialog.openFileNameDialog(title="Open DICOMDIR",typeFile=FileDialog.CS_DICOMDIR)
        del dialog
        if filepath:
            self.fileIO = FileIO(filepath)
            self.patient = Patient(self.fileIO.getFilePath())
            for patient in self.patient.getPatients():
                ID = patient.PatientID
                NAME = str(patient.PatientName).replace('^',' ')
                it = QtGui.QStandardItem("%s\t%s"%(ID,NAME))
                self.patientModel.appendRow(it)
     
    def setStudyView(self,index):
        self.studyModel.clear()
        self.patient.setPatientSelectedByIndex(self.patientModel.itemFromIndex(index).index().row())
        self.study = Study(self.patient.getPatientChildren())
        for study in self.study.getStudies():
            StudyID = study.StudyID
            StudyDescription = study.StudyDescription
            it = QtGui.QStandardItem("%s\t%s"%(StudyID,StudyDescription))
            self.studyModel.appendRow(it)

    def setSeriesView(self,index):
        self.seriesModel.clear()
        self.study.setStudySelectedByIndex(self.studyModel.itemFromIndex(index).index().row())
        self.serie = Serie(self.study.getStudyChildren())
        for serie in self.serie.getSeries():
            image_count = len(serie.children)
            plural = ('', 's')[image_count > 1]
            if 'SeriesDescription' not in serie:
                serie.SeriesDescription = "N/A"
            it = QtGui.QStandardItem("Series {}: {} ({} image{})".format(serie.Modality, serie.SeriesDescription,image_count, plural))
            self.seriesModel.appendRow(it)

    def setImagesView(self,index):
        self.imagesModel.clear()
        self.serie.setSerieSelectedByIndex(self.seriesModel.itemFromIndex(index).index().row())
        self.image = Image(self.serie.getSerieChildren(),self.fileIO.getBaseDir())
        for img in self.image.getImageFiles():
            it = QtGui.QStandardItem(img)
            self.imagesModel.appendRow(it)

    def setDicomView(self,index):
        self.image.setImageSelectedByIndex(self.imagesModel.itemFromIndex(index).index().row())
        # self.dicomView.setPixmap(self.image.getQPixmapByIndexSelected())
        kmeanImage = ImageExtraction(self.image.getPILSelected())
        self.dicomView.setPixmap(kmeanImage.kMeanExtraction())

    def writeMetaimage(self):
        imageFiles = self.image.getImageFiles()
        metaImage = MetaImage()
        metaImage.writeMetaimage(imageFiles)
        render = VolumeRender(self.vtkWidget)


        return 0