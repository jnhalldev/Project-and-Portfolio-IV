from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class DashboardWindow(QMainWindow):
    def __init__(self, geometry=None):
        super().__init__()
        self.setWindowTitle("Dashboard")
        if geometry:
            self.setGeometry(geometry)
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setMinimumSize(800, 600)
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout()
        welcome_label = QLabel("Welcome!")
        welcome_label.setFont(QFont('Arial', 24))
        welcome_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(welcome_label)

        layout.setContentsMargins(10,10,10,10)
        layout.setSpacing(10)

        layout.addStretch()
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
