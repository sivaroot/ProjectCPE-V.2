import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from MainWindow import MainWindow
class MainApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApp()
    mainApp.show()
sys.exit(app.exec_())