from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import auth_manager

class RegistrationWindow(QMainWindow):
    def __init__(self, geometry=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registration")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        if geometry:
            self.setGeometry(geometry)
        self.setMinimumSize(800, 600)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        self.input_name = QLineEdit(self)
        self.input_name.setPlaceholderText("Enter name")
        layout.addWidget(self.input_name)

        self.input_email = QLineEdit(self)
        self.input_email.setPlaceholderText("Enter email")
        layout.addWidget(self.input_email)

        self.input_password = QLineEdit(self)
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        self.input_company = QLineEdit(self)
        self.input_company.setPlaceholderText("Enter company name")
        layout.addWidget(self.input_company)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.on_register_clicked)
        layout.addWidget(self.register_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.on_back_clicked)
        layout.addWidget(self.back_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_register_clicked(self):
        name = self.input_name.text()
        email = self.input_email.text()
        password = self.input_password.text()
        company = self.input_company.text()
        result = auth_manager.register(email, password, name, company)
        if result["success"]:
            QMessageBox.information(self, "Registration Successful", "Account created successfully.")
            self.parent().input_username.setText(email)  # Pre-fill the login form with the new email
            self.close()
            self.parent().show()  # Show the login window again
        else:
            QMessageBox.warning(self, "Registration Failed", result["message"])

    def on_back_clicked(self):
        self.close()
        self.parent().show()