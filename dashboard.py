from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea, QVBoxLayout, QHBoxLayout, QMenu
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
        mainLayout = QVBoxLayout()
        
        # Menu Button
        self.menuButton = QPushButton('☰')  # Using a simple text-based "hamburger" icon
        self.menuButton.clicked.connect(self.openMenu)
        self.menuButton.setMaximumSize(50, 30)  # Small button size
        
        # Top layout for menu and other possible top-right controls
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.menuButton, alignment=Qt.AlignRight)
        mainLayout.addLayout(topLayout)

        # Welcome label
        welcome_label = QLabel("Welcome!")
        welcome_label.setFont(QFont('Arial', 24))
        welcome_label.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(welcome_label)

        # Start New Project button
        self.newProjectButton = QPushButton("Start New Project")
        self.newProjectButton.clicked.connect(self.startNewProject)
        mainLayout.addWidget(self.newProjectButton, alignment=Qt.AlignCenter)

        # Scroll area for existing projects
        self.projectsScrollArea = QScrollArea()
        self.projectsScrollArea.setWidgetResizable(True)
        self.projectsLayout = QVBoxLayout()
        self.projectsScrollAreaWidget = QWidget()
        self.projectsScrollAreaWidget.setLayout(self.projectsLayout)
        self.projectsScrollArea.setWidget(self.projectsScrollAreaWidget)
        mainLayout.addWidget(self.projectsScrollArea)

        # Set the margins and spacing
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(mainLayout)
        self.setCentralWidget(central_widget)

        # Populate the scroll area with projects
        self.loadProjects()

    def openMenu(self):
        menu = QMenu(self)
        action1 = menu.addAction("Option 1")
        action2 = menu.addAction("Option 2")
        # ... add more actions as needed
        menu.exec_(self.menuButton.mapToGlobal(self.menuButton.rect().bottomLeft()))

    def startNewProject(self):
        # Logic to start a new project
        pass

    def loadProjects(self):
        # This method should populate the scroll area with projects
        # For demonstration, let's create dummy buttons for projects
        for i in range(10):  # Assume there are 10 projects
            projectButton = QPushButton(f"Project {i+1}")
            projectButton.clicked.connect(lambda checked, i=i: self.openProject(i))
            self.projectsLayout.addWidget(projectButton, alignment=Qt.AlignCenter)

    def openProject(self, projectIndex):
        # Logic to navigate to the selected project
        print(f"Project {projectIndex+1} opened")