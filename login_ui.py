from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QMessageBox, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
from widgets import ClickableLineEdit 
from auth_manager import login
from account import SaveUserIDToken,SaveUserID
from dashboard import DashboardWindow
from registration_ui import RegistrationWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windowWidth = 1200
        self.windowHeight = 1200
        self.setupUi()
        self.installEventFilter(self)

    def setupUi(self):
        self.setWindowTitle("Resu-Hunter")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setGeometry(1200, 300, self.windowWidth, self.windowHeight)
        self.setFixedSize(self.windowWidth, self.windowHeight)
        self.setFocus()

        # Main layout for vertically aligning widgets
        mainLayout = QVBoxLayout()

        # Image Label
        self.imageLabel = QLabel(self)
        pixmap = QPixmap("images/Resu-Hunter_Logo.jpg") 
        self.imageLabel.setPixmap(pixmap.scaled(600, 600, Qt.KeepAspectRatio))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.imageLabel)

        # Title Label
        self.label_title = QLabel("Welcome, please log in!", self)
        self.label_title.setFont(QFont('Arial', 25))
        self.label_title.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.label_title)

        # Username Input
        self.input_username = ClickableLineEdit(self)
        self.input_username.setPlaceholderText("Enter email")
        self.input_username.setFont(QFont('Arial', 14))
        self.input_username.setAlignment(Qt.AlignCenter)
        self.input_username.setFixedWidth(600)
        self.input_username.setFixedHeight(40)
        mainLayout.addWidget(self.input_username)

        # Password Input
        self.input_password = ClickableLineEdit(self)
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setEchoMode(ClickableLineEdit.Password)
        self.input_password.setFont(QFont('Arial', 14))
        self.input_password.setAlignment(Qt.AlignCenter)
        self.input_password.setFixedWidth(600)
        self.input_password.setFixedHeight(40)
        mainLayout.addWidget(self.input_password)

        # Login Button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.on_login_clicked)
        self.login_button.setFixedWidth(120)
        self.login_button.setFixedHeight(30)
        mainLayout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        # Register Button
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.on_register_clicked)
        self.register_button.setFixedWidth(120)
        self.register_button.setFixedHeight(30)
        mainLayout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        # Adjusting spacing
        mainLayout.setSpacing(10)
        mainLayout.setAlignment(Qt.AlignCenter)

        # Set the main layout to a central widget
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Set the tab order explicitly
        self.setTabOrder(self.input_username, self.input_password)
        self.setTabOrder(self.input_password, self.login_button)
        self.setTabOrder(self.login_button, self.register_button)


    def resizeEvent(self, event):
        self.updateUI()
        super().resizeEvent(event)

    def updateUI(self):
        self.label_title.adjustSize()
        self.label_title.move((self.width() - self.label_title.width()) // 2, (self.height() - self.label_title.height()) // 3)
        self.input_username.move((self.width() - self.input_username.width()) // 2, self.label_title.y() + self.label_title.height() + 40)
        self.input_password.move((self.width() - self.input_password.width()) // 2, self.input_username.y() + self.input_username.height() + 40)
        self.login_button.move((self.width() - self.login_button.width()) // 2, self.input_password.y() + self.input_password.height() + 40)

    def on_login_clicked(self):
        # Extract username and password from input fields
        username = self.input_username.text()
        password = self.input_password.text()
        response_data = login(username, password)
        if response_data['success']:
            SaveUserIDToken(response_data['idToken'])
            testing = response_data['localId']
            SaveUserID(testing)
            self.hide()
            self.dashboard = DashboardWindow(self.geometry())
            self.dashboard.show()
        else:
            QMessageBox.warning(self, "Login Failed", "The account does not exist or the password is incorrect.")

    def on_register_clicked(self):
        self.hide()
        self.registrationWindow = RegistrationWindow(self.geometry(), parent=self)
        self.registrationWindow.show()
