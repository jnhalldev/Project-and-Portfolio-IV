from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea, QHBoxLayout, QFrame, QMenu
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import auth_manager
import login_ui
import new_project_ui
import project_details
from account import ClearUserIDToken, GetDatabaseURL, GetUserID, ClearUserID
import project
import requests
import json

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

    def fetchProjectsKeys(self):
        userID = GetUserID()
        databaseURL = GetDatabaseURL()
        projectsURL = f"{databaseURL}/{userID}/projects.json"

        response = requests.get(projectsURL)
        if response.status_code == 200 and response.json() is not None:
            # Extract project keys
            project_keys = list(response.json().keys())
        else:
            project_keys = []
        return project_keys

    def loadProjects(self):

        self.clearLayout(self.projectsLayout)
        
        projects = []
        userID = GetUserID()
        databaseURL = GetDatabaseURL()
        project_keys = self.fetchProjectsKeys()

        for project_key in project_keys:
            projectDetailURL = f"{databaseURL}/{userID}/projects/{project_key}.json"

            # Fetch the project details
            response = requests.get(projectDetailURL)
            if response.status_code == 200:
                try:
                    # Attempt to parse the JSON string to a dictionary
                    print(type(response.text))
                    print(response.text)

                    project_data = json.loads(response.text)

                    # Now access project_data as a dictionary
                    title = project_data.get("name", project_key)
                    description = project_data.get("description", "No description available")
                    projects.append({"title": title, "description": description})
                except json.JSONDecodeError as e:
                    print(f"Failed to parse project data for {project_key}: {e}")
                    continue  # Skip this project on parsing error
            else:
                print(f"Failed to fetch details for project {project_key}")

        for project in projects:
            # Container for each project
            projectContainer = QFrame()
            projectContainer.setFrameShape(QFrame.StyledPanel)
            projectContainer.setFrameShadow(QFrame.Raised)
            
            # Horizontal layout for the project container
            projectLayout = QHBoxLayout()
            self.projectsLayout.setAlignment(Qt.AlignTop)



            # Project title and description
            projectText = QLabel(f"<b>{project['title']}</b><br>{project['description']}")
            projectText.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            projectText.setWordWrap(True)

            # Button to navigate to the project
            projectButton = QPushButton("Open")
            projectButton.clicked.connect(lambda checked, p=project: self.openProjectDetails(p))

            # Add the label and button to the project layout
            projectLayout.addWidget(projectText, 1)
            projectLayout.addWidget(projectButton)

            # Set the project layout to the project container
            projectContainer.setLayout(projectLayout)

            # Add the project container to the projects layout
            self.projectsLayout.addWidget(projectContainer)

    def openProjectDetails(self, title):
        self.projectDetailsWindow = project_details.ProjectDetailsWindow(project=title, parent=self)
        self.projectDetailsWindow.show()
        self.hide()

    def openProject(self, projectIndex):
        # Logic to navigate to the selected project
        print(f"Project {projectIndex+1} opened")

    def logout(self):
        ClearUserIDToken()
        ClearUserID()
        auth_manager.logout()
        # Close the DashboardWindow
        self.hide()
        self.dashboard = login_ui.MainWindow()
        self.dashboard.show()

    def clearLayout(self, layout):
        # Safely remove all widgets from a layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
