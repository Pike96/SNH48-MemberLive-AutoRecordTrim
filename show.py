from PyQt5 import QtWidgets
from ui_main import Ui_Main
import autorecord

class MainWindow(QtWidgets.QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.pushButton.clicked.connect(self.forgive)
        self.recording = False

    # Connect buttons

    def forgive(self):
        if self.recording is False:
            name = self.plainTextEdit.toPlainText()
            self.recording = True
            while 1:
                autorecord.record(name, 10)
                if self.recording is False:
                    break
        else:
            self.recording = False
