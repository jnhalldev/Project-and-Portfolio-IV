import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter

class MainWindow(QMainWindow):

    def __init__(self):

        self.windowWidth = 1200
        self.windowHeight = 1200

        super().__init__()
        self.setWindowTitle("Resu-Hunter")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setGeometry(1200,300,self.windowWidth,self.windowHeight)
        self.background_image = QPixmap("images/resu_hunter_icon.png")

        self.label_title = QLabel("Welcome to Resu-Hunter!", self)
        self.initialFontSize = 25
        self.label_title.setFont(QFont('Arial', self.initialFontSize))
        self.label_title.setAlignment(Qt.AlignCenter) 
        self.updateLabelPosition()

        self.show()
    
    def resizeEvent(self, event):
        self.updateLabelPosition()
        self.adjustLabelFontSize()
        super().resizeEvent(event)

    def updateLabelPosition(self):
        self.label_title.adjustSize()
        self.label_title.move((self.width() - self.label_title.width()) // 2, 
                              (self.height() - self.label_title.height()) // 6)
        
    def adjustLabelFontSize(self):
        scaleFactor = max(self.width() / self.windowWidth, self.height() / self.windowHeight)
        newFontSize = max(self.initialFontSize * scaleFactor, 10)
        maxFontSize = 40
        newFontSize = min(newFontSize, maxFontSize)
        self.label_title.setFont(QFont('Arial', int(newFontSize)))
        self.label_title.adjustSize()
        self.updateLabelPosition()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

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