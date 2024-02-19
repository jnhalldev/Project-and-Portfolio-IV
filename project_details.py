from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QComboBox, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import account
import requests
import spacy_model
from spacy_model import process_resumes, train_model
import project

class ProjectDetailsWindow(QMainWindow):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self.setupUI()
        self.setGeometry(parent.geometry())

    def setupUI(self):
        self.setWindowTitle("Project Details")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setFixedSize(1200, 1200)

        mainLayout = QVBoxLayout()

        # Back Button
        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(self.goBack)
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.backButton, alignment=Qt.AlignLeft)
        mainLayout.addLayout(topLayout)

        # Form layout for the title, description, and position title
        formLayout = QVBoxLayout()
        formLayout.setSpacing(10)

        # Project Title
        title = QLabel(self.project["title"])
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(title)

        # Project Description
        description = QLabel(self.project["description"])
        description.setFont(QFont('Arial', 18))
        description.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(description)

        # Position Title
        positionTitle = QLabel(self.project["job_title"]) 
        positionTitle.setFont(QFont('Arial', 16))
        positionTitle.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(positionTitle)

        # Edit Project Details Button
        self.editDetailsButton = QPushButton("Edit Project Details")
        formLayout.addWidget(self.editDetailsButton, alignment=Qt.AlignCenter)

        # Add the form layout to the main layout
        mainLayout.addLayout(formLayout)
        mainLayout.addStretch(1)

        # Model Selection Dropdown
        self.modelSelection = QComboBox()
        self.modelSelection.addItems(["Model 1", "Model 2", "Model 3"]) 
        mainLayout.addWidget(self.modelSelection, alignment=Qt.AlignCenter)

        # Analyze Resumes Button
        self.analyzeResumesButton = QPushButton("Analyze Resumes")
        mainLayout.addWidget(self.analyzeResumesButton, alignment=Qt.AlignCenter)

        # Analysis Status Label
        self.analysisStatusLabel = QLabel("Analysis Status: Pending")
        self.analysisStatusLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.analysisStatusLabel)

        # Candidate Analytics Button
        self.candidateAnalyticsButton = QPushButton("Candidate Analytics")
        mainLayout.addWidget(self.candidateAnalyticsButton, alignment=Qt.AlignCenter)

        # View Best Candidates Button
        self.viewCandidatesButton = QPushButton("View Best Candidates")
        mainLayout.addWidget(self.viewCandidatesButton, alignment=Qt.AlignCenter)

        # Download Candidate Resumes Button
        self.downloadResumesButton = QPushButton("Download Candidate Resumes")
        mainLayout.addWidget(self.downloadResumesButton, alignment=Qt.AlignCenter)
        mainLayout.addStretch(2)


        # Archive and Delete Buttons
        bottomLayout = QHBoxLayout()
        self.archiveButton = QPushButton("Archive")
        self.deleteButton = QPushButton("Delete")
        bottomLayout.addWidget(self.archiveButton, alignment=Qt.AlignLeft)
        bottomLayout.addWidget(self.deleteButton, alignment=Qt.AlignRight)
        mainLayout.addLayout(bottomLayout)

        # Connect buttons to their respective methods
        self.archiveButton.clicked.connect(self.confirmArchive)
        self.deleteButton.clicked.connect(self.confirmDelete)
        self.analyzeResumesButton.clicked.connect(self.onAnalyzeResumesClicked)

        central_widget = QWidget()
        central_widget.setLayout(mainLayout)
        self.setCentralWidget(central_widget)

    def onAnalyzeResumesClicked(self):
        resumes = self.fetch_resumes(self.project["path"])
        extracted_info = process_resumes(resumes)
        print(extracted_info)

    def analyzeResumes():
        test = 2
        
    def fetch_resumes(self, url):
        full_url = f"{account.GetDatabaseURL()}{url}resumes.json"
        response = requests.get(full_url)
        resumes = response.json() if response.status_code == 200 else []

        return [resume for resume in resumes.values()]

    def confirmArchive(self):
        #reply = QMessageBox.question(self, 'Confirm Archive',
        #                             "Are you sure you want to Archive this project?",
        #                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #if reply == QMessageBox.Yes:
        #    self.archiveProject()
        #    self.goBack()
        train_model()
        

    def archiveProject(self):
        # Placeholder for archiving logic
        print("Archiving project:", self.project["title"])
        self.goBack()

    def confirmDelete(self):
        reply = QMessageBox.question(self, 'Confirm Delete',
                                     "Are you sure you want to delete this project?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.deleteProject()
            self.goBack()

    def deleteProject(self):
        # Placeholder for delete logic
        print("Deleting project:", self.project["title"])
        self.goBack()

    def goBack(self):
        if self.parent():
            self.parent().setGeometry(self.geometry()) 
            self.parent().show()
        self.close()

