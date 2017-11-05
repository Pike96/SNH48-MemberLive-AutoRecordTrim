import sys
from PyQt5.QtWidgets import QApplication
from show import MainWindow

app = QApplication(sys.argv)

execution = MainWindow()

sys.exit(app.exec())