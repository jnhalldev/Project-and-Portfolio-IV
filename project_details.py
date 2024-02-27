from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QComboBox, QFileDialog
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import account
import requests
from spacy_model import process_resumes
from database_manager import upload_json_to_storage, download_file_from_firebase
from candidate_analytics import CandidateAnalyticsWindow
import new_project_ui
import database_manager


class ProjectDetailsWindow(QMainWindow):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self.data = self.fetchDataFromFirebase()
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

        # Project Category
        category = QLabel(self.project["category"])
        category.setFont(QFont('Arial', 20))
        category.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(category)

        # Position Title
        positionTitle = QLabel(self.project["job_title"]) 
        positionTitle.setFont(QFont('Arial', 16))
        positionTitle.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(positionTitle)

        # Project location
        location = QLabel(self.project["location"])
        location.setFont(QFont('Arial', 12))
        location.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(location)


        # Edit Project Details Button
        self.editDetailsButton = QPushButton("Edit Project Details")
        formLayout.addWidget(self.editDetailsButton, alignment=Qt.AlignCenter)

        # Add the form layout to the main layout
        mainLayout.addLayout(formLayout)
        mainLayout.addStretch(1)

        # Model Selection Dropdown
        self.modelSelection = QComboBox()
        self.modelSelection.addItems(["SpaCy", "Model 2", "Model 3"]) 
        mainLayout.addWidget(self.modelSelection, alignment=Qt.AlignCenter)

        # Analyze Resumes Button
        self.analyzeResumesButton = QPushButton("Analyze Resumes")
        mainLayout.addWidget(self.analyzeResumesButton, alignment=Qt.AlignCenter)

        # Analysis Status Label
        if self.data:
            self.analysisStatusLabel = QLabel("Analysis Status: Complete")
        else:
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
        self.viewCandidatesButton.clicked.connect(self.showTopFive)
        self.candidateAnalyticsButton.clicked.connect(self.openCandidateAnalytics)
        self.editDetailsButton.clicked.connect(self.editProjectDetails)
        self.downloadResumesButton.clicked.connect(self.downloadTopPDFs)

        central_widget = QWidget()
        central_widget.setLayout(mainLayout)
        self.setCentralWidget(central_widget)

    def showTopFive(self):
        if self.data:
            self.showTopResumesMessage(self.data)

    def downloadTopPDFs(self):
        directory  = self.select_download_location()
        if directory is None:
            self.goBack() #app was exiting for unknown reason - this brings back to dashboard, stopping from losing the app
        else:
            download_file_from_firebase(self.data, f"{account.GetUserID()}/{self.project['title']}/",directory)
            self.goBack() #app was exiting for unknown reason - this brings back to dashboard, stopping from losing the app

    def select_download_location(self):
        widget = QWidget()

        # Open a dialog to select a directory
        directory = QFileDialog.getExistingDirectory(widget, "Select Download Location")
        
        # Check if a directory was selected
        if directory:
            print(f"Selected directory: {directory}")
            return directory
        else:
            print("No directory selected.")
            return None

    def openCandidateAnalytics(self):
        self.data = self.fetchDataFromFirebase()
        if self.data:
            self.analytics_window = CandidateAnalyticsWindow(self.data, self)
            self.analytics_window.show()

    def editProjectDetails(self):
        self.new_project_window = new_project_ui.NewProjectWindow(geometry=self.geometry(),project=self.project, parent=self)
        self.hide()
        self.new_project_window.show()
        

    def fetchDataFromFirebase(self):
        full_url = f"{account.GetDatabaseURL()}{self.project['path']}resume_evaluations.json"
        print(full_url)
        response = requests.get(full_url)
        results = response.json() if response.status_code == 200 else []

        return results


    def onAnalyzeResumesClicked(self):
        resumes = self.fetch_resumes(self.project["path"])
        resume_evaluations = process_resumes(resumes, self.project)

        upload_json_to_storage(account.GetDatabaseURL(),f"{self.project['path']}resume_evaluations/",account.GetUserIDToken(),resume_evaluations)
        top_5_resumes = resume_evaluations[:5]
        self.showTopResumesMessage(top_5_resumes)

        
    def showTopResumesMessage(self, resume_evaluations):
        messageText = "Top 5 Resumes:\n\n"
        for i, resume in enumerate(resume_evaluations[:5]):
            messageText += f"{i+1}. ID: {resume['resume_id']}.pdf, Score: {resume['score']}\n"

        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.setText(messageText)
        self.msgBox.setWindowTitle("Top 5 Resumes")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.exec_()
        
    def fetch_resumes(self, url):
        full_url = f"{account.GetDatabaseURL()}{url}resumes.json"
        response = requests.get(full_url)
        resumes = response.json() if response.status_code == 200 else []

        return [resume for resume in resumes.values()]

    def confirmArchive(self):
        reply = QMessageBox.question(self, 'Confirm Archive',
                                     "Are you sure you want to Archive this project?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.archiveProject()
            self.goBack()
        

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
        url = f"{account.GetDatabaseURL()}{self.project['path']}"
        url = url[:-1]
        url = f"{url}.json"
        database_manager.delete_resumes(self.project['path'])

        response = requests.delete(url)

        if response.status_code == 200:
            print("Node deleted successfully.")
        else:
            print("Failed to delete node.")

        print("Deleting project:", self.project["title"])
        self.goBack()

    def goBack(self):
        if self.parent():
            self.parent().setGeometry(self.geometry()) 
            self.parent().show()
        self.close()