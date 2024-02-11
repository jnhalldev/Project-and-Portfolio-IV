import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        self.windowWidth = 1200
        self.windowHeight = 1200

        super().__init__()
        self.setWindowTitle("Resu-Hunter")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setGeometry(1200, 300, self.windowWidth, self.windowHeight)

        self.label_title = QLabel("Welcome to Resu-Hunter!", self)
        self.initialFontSize = 25
        self.label_title.setFont(QFont('Arial', self.initialFontSize))
        self.label_title.setAlignment(Qt.AlignCenter) 

        self.input_username = QLineEdit(self)
        self.input_username.setPlaceholderText("Enter username")
        self.input_username.setFont(QFont('Arial', 14))
        self.input_username.setAlignment(Qt.AlignCenter)
        self.input_username.adjustSize()  # Adjust size to content

        self.input_password = QLineEdit(self)
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setFont(QFont('Arial', 14))
        self.input_password.setAlignment(Qt.AlignCenter)
        self.input_password.adjustSize()  # Adjust size to content

        self.input_username.setFocusPolicy(Qt.NoFocus)
        self.input_password.setFocusPolicy(Qt.NoFocus)

        self.updateUI()  # Initial update to sync background and label

    def resizeEvent(self, event):
        self.updateUI()  # Update on window resize
        super().resizeEvent(event)

    def updateUI(self):
        self.updateLabelPosition()

    def updateLabelPosition(self):
        # Center the title label
        self.label_title.adjustSize()
        self.label_title.move((self.width() - self.label_title.width()) // 2, 
                              (self.height() - self.label_title.height()) // 5)
        
        # Position the username label relative to the title label and bottom of the window
        title_bottom = self.label_title.y() + self.label_title.height()
        space_below_title = self.height() - title_bottom
        self.input_username.move((self.width() - self.input_username.width()) // 2,
                                 title_bottom + space_below_title // 6 - self.input_username.height() // 2)
        
        # Position the username label relative to the title label and bottom of the window
        username_bottom = self.label_title.y() + self.label_title.height()
        space_below_title = self.height() - username_bottom
        self.input_password.move((self.width() - self.input_password.width()) // 2,
                                 title_bottom + space_below_title // 3 - self.input_password.height() // 2)

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