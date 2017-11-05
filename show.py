from PyQt5 import QtWidgets
from ui_main import Ui_Main
import autorecord

class MainWindow(QtWidgets.QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.pushButton.clicked.connect(self.forgive)

    # Connect buttons

    def forgive(self):
        autorecord.main()