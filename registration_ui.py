from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import auth_manager

class RegistrationWindow(QMainWindow):
    def __init__(self, geometry=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registration")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        if geometry:
            self.setGeometry(geometry)
        self.setFixedSize(1200,1200)
        self.setupUI()

    def setupUI(self):
        # Main layout container
        mainLayout = QVBoxLayout()

        # Form layout for input fields and buttons
        formLayout = QVBoxLayout()

        # Max width for the input fields and buttons
        maxWidth = 400

        # Image Label
        self.imageLabel = QLabel(self)
        pixmap = QPixmap("images/Resu-Hunter_Logo.jpg")  # Replace 'your_image.png' with your actual image path
        self.imageLabel.setPixmap(pixmap.scaled(600, 600, Qt.KeepAspectRatio))  # Adjust scaling as needed
        self.imageLabel.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(self.imageLabel)

        # Name input field
        self.input_name = QLineEdit(self)
        self.input_name.setPlaceholderText("Enter name")
        self.input_name.setFixedWidth(500)
        self.input_name.setFixedHeight(40)
        formLayout.addWidget(self.input_name, alignment=Qt.AlignCenter)

        # Email input field
        self.input_email = QLineEdit(self)
        self.input_email.setPlaceholderText("Enter email")
        self.input_email.setFixedWidth(500)
        self.input_email.setFixedHeight(40)
        formLayout.addWidget(self.input_email, alignment=Qt.AlignCenter)

        # Password input field
        self.input_password = QLineEdit(self)
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setFixedWidth(500)
        self.input_password.setFixedHeight(40)
        formLayout.addWidget(self.input_password, alignment=Qt.AlignCenter)

        # Company name input field
        self.input_company = QLineEdit(self)
        self.input_company.setPlaceholderText("Enter company name")
        self.input_company.setFixedWidth(500)
        self.input_company.setFixedHeight(40)
        formLayout.addWidget(self.input_company, alignment=Qt.AlignCenter)

        # Register button
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.on_register_clicked)
        self.register_button.setMaximumWidth(maxWidth)
        formLayout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.on_back_clicked)
        self.back_button.setMaximumWidth(maxWidth)
        formLayout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        # Align the formLayout in the center of mainLayout
        mainLayout.addStretch()
        mainLayout.addLayout(formLayout)
        mainLayout.addStretch()

        # Setting the main layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(mainLayout)
        self.setCentralWidget(central_widget)

    def on_register_clicked(self):
        name = self.input_name.text()
        email = self.input_email.text()
        password = self.input_password.text()
        company = self.input_company.text()
        result = auth_manager.register(email, password)

        if not all([name, email, password, company]):
            QMessageBox.warning(self, "Registration Failed", "All fields are required.")
            return

        if result.get("success"):
            QMessageBox.information(self, "Registration Successful", "Account created successfully.")
            if self.parent() and hasattr(self.parent(), 'input_username'):
                self.parent().input_username.setText(email)  # Pre-fill the login form with the new email
            self.close()
            if self.parent():
                self.parent().show()  # Show the login window again
        else:
            QMessageBox.warning(self, "Registration Failed", result.get("message", "An error occurred during registration."))

    def on_back_clicked(self):
        self.close()
        if self.parent():
            self.parent().show()
