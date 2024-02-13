from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea, QHBoxLayout, QFrame, QMenu
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import auth_manager
import login_ui
import new_project_ui

class DashboardWindow(QMainWindow):
    def __init__(self, geometry=None):
        super().__init__()
        self.setWindowTitle("Dashboard")
        if geometry:
            self.setGeometry(geometry)
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setFixedSize(1200,1200)
        self.setupUI()

    def setupUI(self):
        mainLayout = QVBoxLayout()
        
        # Menu Button
        self.menuButton = QPushButton('☰')
        self.menuButton.clicked.connect(self.openMenu)
        self.menuButton.setMaximumSize(50, 30)
        
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
        account = menu.addAction("Account")
        settings = menu.addAction("Settings")
        logout = menu.addAction("Logout")
        logout.triggered.connect(self.logout)
        menu.exec_(self.menuButton.mapToGlobal(self.menuButton.rect().bottomLeft()))

    def startNewProject(self):
        self.hide()
        self.newProjectWindow = new_project_ui.NewProjectWindow(self.geometry(), self)
        self.newProjectWindow.show()

    def loadProjects(self):
        #sample projects
        projects = [
            {"title": "Project 1", "description": "Description of Project 1"},
            {"title": "Project 2", "description": "Description of Project 2"},
            {"title": "Project 3", "description": "Description of Project 3"},
            {"title": "Project 4", "description": "Description of Project 4"},
            {"title": "Project 5", "description": "Description of Project 5"},
            {"title": "Project 6", "description": "Description of Project 6"},
            {"title": "Project 7", "description": "Description of Project 7"},
            {"title": "Project 8", "description": "Description of Project 8"},
            {"title": "Project 9", "description": "Description of Project 9"},
            {"title": "Project 10", "description": "Description of Project 10"},
            {"title": "Project 11", "description": "Description of Project 11"},
            {"title": "Project 12", "description": "Description of Project 12"},
            {"title": "Project 13", "description": "Description of Project 13"},
            {"title": "Project 14", "description": "Description of Project 14"},
            {"title": "Project 15", "description": "Description of Project 15"},
            {"title": "Project 16", "description": "Description of Project 16"},
            {"title": "Project 17", "description": "Description of Project 17"},
        ]

        for project in projects:
            # Container for each project
            projectContainer = QFrame()
            projectContainer.setFrameShape(QFrame.StyledPanel)
            projectContainer.setFrameShadow(QFrame.Raised)
            
            # Horizontal layout for the project container
            projectLayout = QHBoxLayout()

            # Project title and description
            projectText = QLabel(f"<b>{project['title']}</b><br>{project['description']}")
            projectText.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            projectText.setWordWrap(True)

            # Button to navigate to the project
            projectButton = QPushButton("Open")
            projectButton.clicked.connect(lambda checked, title=project['title']: self.openProject(title))

            # Add the label and button to the project layout
            projectLayout.addWidget(projectText, 1)  # Add stretch factor to text for it to take up available space
            projectLayout.addWidget(projectButton)

            # Set the project layout to the project container
            projectContainer.setLayout(projectLayout)

            # Add the project container to the projects layout
            self.projectsLayout.addWidget(projectContainer)

    def openProject(self, title):
        # Logic to open the selected project
        print(f"{title} opened")

    def openProject(self, projectIndex):
        # Logic to navigate to the selected project
        print(f"Project {projectIndex+1} opened")

    def logout(self):
        # Call the logout function in auth_manager
        auth_manager.logout()
        # Close the DashboardWindow
        self.hide()
        self.dashboard = login_ui.MainWindow()
        self.dashboard.show()
        #if hasattr(self, 'loginWindow'):
        #    self.loginWindow.show()