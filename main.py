import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(1200,300,500,500)
    win.setWindowTitle("ResuHunter")
    win.show()
    sys.exit(app.exec_())

window()