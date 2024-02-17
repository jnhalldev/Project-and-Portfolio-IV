from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QMessageBox, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import project
import database_manager
import account
import json

class NewProjectWindow(QMainWindow):
    def __init__(self, geometry=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")
        if geometry:
            self.setGeometry(geometry)
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setMinimumSize(800, 600)
        self.selectedZipFile = None
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        # Back Button
        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(self.goBack)
        
        # Top layout for back button
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.backButton, alignment=Qt.AlignLeft)
        layout.addLayout(topLayout)

        # Project Title
        self.title = QLabel("Create a New Project")
        self.title.setFont(QFont('Arial', 24))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Upload Resumes Button
        self.uploadResumesButton = QPushButton("Upload Resumes")
        self.uploadResumesButton.clicked.connect(self.uploadResumes)
        layout.addWidget(self.uploadResumesButton, alignment=Qt.AlignCenter)

        # Input fields
        self.projectNameInput = QLineEdit()
        self.projectNameInput.setPlaceholderText("Project Name")
        self.projectNameInput.setFixedWidth(500)
        layout.addWidget(self.projectNameInput, alignment=Qt.AlignCenter)

        self.projectCategoryInput = QLineEdit()
        self.projectCategoryInput.setPlaceholderText("Category")
        self.projectCategoryInput.setFixedWidth(500)
        layout.addWidget(self.projectCategoryInput, alignment=Qt.AlignCenter)

        self.projectJobTitleInput = QLineEdit()
        self.projectJobTitleInput.setPlaceholderText("Job Title")
        self.projectJobTitleInput.setFixedWidth(500)
        layout.addWidget(self.projectJobTitleInput, alignment=Qt.AlignCenter)

        self.projectLocationInput = QLineEdit()
        self.projectLocationInput.setPlaceholderText("Location")
        self.projectLocationInput.setFixedWidth(500)
        layout.addWidget(self.projectLocationInput, alignment=Qt.AlignCenter)

        self.projectDescriptionInput = QTextEdit()
        self.projectDescriptionInput.setPlaceholderText("Project Description")
        self.projectDescriptionInput.setFixedWidth(700)
        layout.addWidget(self.projectDescriptionInput, alignment=Qt.AlignCenter)

        self.jobSkillsInput = QTextEdit()
        self.jobSkillsInput.setPlaceholderText("Desired Job Skills (separate with commas)")
        self.jobSkillsInput.setFixedWidth(700)
        layout.addWidget(self.jobSkillsInput, alignment=Qt.AlignCenter)

        self.educationInput = QTextEdit()
        self.educationInput.setPlaceholderText("Desired Education (separate with commas)")
        self.educationInput.setFixedWidth(700)
        layout.addWidget(self.educationInput, alignment=Qt.AlignCenter)

        self.experienceInput = QTextEdit()
        self.experienceInput.setPlaceholderText("Desired Experience (separate with commas)")
        self.experienceInput.setFixedWidth(700)
        layout.addWidget(self.experienceInput, alignment=Qt.AlignCenter)

        # Save Project Button
        self.saveProjectButton = QPushButton("Save Project")
        self.saveProjectButton.clicked.connect(self.saveProject)
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.saveProjectButton)
        layout.addLayout(bottomLayout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def uploadResumes(self):
        # Check if a file has already been selected
        if self.selectedZipFile:
            # Confirm if the user wants to change the file
            reply = QMessageBox.question(self, "Confirm", "A ZIP file has already been selected. Do you want to change it?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        # Open file dialog to select a new ZIP file
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select ZIP File", "",
                                                  "ZIP Files (*.zip)", options=options)
        
        if fileName:
            self.selectedZipFile = fileName 
            self.uploadResumesButton.setText("File Selected!")

    def saveProject(self):
        # Instantiate the Project class with input from the UI
        
        project_url_path = f"{account.GetUserID()}/projects/{self.projectNameInput.text()}/"
        createdProject = project.Project(
            self.projectNameInput.text(),
            self.projectCategoryInput.text(),
            self.projectJobTitleInput.text(),
            self.projectLocationInput.text(), 
            self.projectDescriptionInput.toPlainText(),
            self.jobSkillsInput.toPlainText(),
            self.educationInput.toPlainText(),
            self.experienceInput.toPlainText(),
            project_url_path
        )
        
        project_dict = createdProject.to_dict()
        project_json = json.dumps(project_dict)
        

        database_url = account.GetDatabaseURL()
        user_id_token = account.GetUserIDToken()
        database_manager.write_data_to_firebase(database_url, project_url_path, user_id_token, project_json)
        
        # Optionally, if write_data_to_firebase returns the actual URL where the project was saved,
        # you could then set that URL to your project object here
        # createdProject.projectURL = returned_url_from_firebase
        
        QMessageBox.information(self, "Project Saved", "Your project has been saved successfully.")
        self.goBack()


    def goBack(self):
        if self.parent():
            self.parent().setGeometry(self.geometry()) 
            self.parent().show()
        self.close()

