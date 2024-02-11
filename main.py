import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resu-Hunter")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setGeometry(1200,300,1200,1200)

        self.label_title = QLabel(self)
        self.label_title.setText("Welcome to Resu-Hunter!")
        self.label_title.setFont(QFont('Arial', 25))
        self.label_title.setAlignment(Qt.AlignCenter) 
        self.label_title.resize(self.width(), 100)
        self.updateLabelPosition()

        self.show()
    
    def resizeEvent(self, event):
        self.updateLabelPosition()
        super().resizeEvent(event)

    def updateLabelPosition(self):
        self.label_title.adjustSize()
        self.label_title.move((self.width() - self.label_title.width()) // 2, 
                              (self.height() - self.label_title.height()) // 5)

def main():
    app = QApplication(sys.argv)
    main_Window = MainWindow()
    main_Window.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass  # Suppress the SystemExit exception

if __name__ == "__main__":
    main()