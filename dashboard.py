from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QFont

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.windowWidth = 1200
        self.windowHeight = 1200
        self.setMinimumSize(800, 600)
        self.setGeometry(100, 100, self.windowWidth, self.windowHeight)
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout()
        welcome_label = QLabel("Welcome!")
        welcome_label.setFont(QFont('Arial', 24))
        layout.addWidget(welcome_label)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
