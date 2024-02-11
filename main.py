import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QFont

class ClickableLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(ClickableLineEdit, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)  # Start with no focus

    def mousePressEvent(self, event):
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        super().mousePressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        self.windowWidth = 1200
        self.windowHeight = 1200

        super().__init__()
        self.setWindowTitle("Resu-Hunter")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setGeometry(1200, 300, self.windowWidth, self.windowHeight)
        self.setMinimumSize(800, 600)

        self.label_title = QLabel("Welcome to Resu-Hunter!", self)
        self.initialFontSize = 25
        self.label_title.setFont(QFont('Arial', self.initialFontSize))
        self.label_title.setAlignment(Qt.AlignCenter) 

        self.input_username = ClickableLineEdit(self)
        self.input_username.setPlaceholderText("Enter username")
        self.input_username.setFont(QFont('Arial', 14))
        self.input_username.setAlignment(Qt.AlignCenter)

        self.input_password = ClickableLineEdit(self)
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setFont(QFont('Arial', 14))
        self.input_password.setAlignment(Qt.AlignCenter)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.on_login_clicked)


        self.updateUI()

    def resizeEvent(self, event):
        self.updateUI()  
        super().resizeEvent(event)

    def updateUI(self):
        self.updateLabelPosition()

    def updateLabelPosition(self):
        # Center the title label
        self.label_title.adjustSize()
        self.label_title.move((self.width() - self.label_title.width()) // 2, 
                            (self.height() - self.label_title.height()) // 3)
        
        # Position the username input field (no change needed if its position is already set)
        self.input_username.adjustSize()
        self.input_username.move((self.width() - self.input_username.width()) // 2,
                                self.label_title.y() + self.label_title.height() + 40)  # Example fixed distance from title label

        # Position the password field a fixed distance below the username field
        fixed_distance = 40  # Fixed distance in pixels
        self.input_password.adjustSize()
        self.input_password.move((self.width() - self.input_password.width()) // 2,
                                self.input_username.y() + self.input_username.height() + fixed_distance)

        # Position the login button a fixed distance below the password field
        button_distance = 40  # Fixed distance in pixels
        self.login_button.adjustSize()  # Ensure button size is updated to fit its content
        self.login_button.move((self.width() - self.login_button.width()) // 2,
                            self.input_password.y() + self.input_password.height() + button_distance)
    
    def on_login_clicked(self):
        # Handle button click event
        print("Login button clicked")


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