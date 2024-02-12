from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QMessageBox, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

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

        self.projectNameInput = QLineEdit()
        self.projectNameInput.setPlaceholderText("Category")
        self.projectNameInput.setFixedWidth(500)
        layout.addWidget(self.projectNameInput, alignment=Qt.AlignCenter)

        self.projectNameInput = QLineEdit()
        self.projectNameInput.setPlaceholderText("Job Title")
        self.projectNameInput.setFixedWidth(500)
        layout.addWidget(self.projectNameInput, alignment=Qt.AlignCenter)

        self.projectNameInput = QLineEdit()
        self.projectNameInput.setPlaceholderText("Location")
        self.projectNameInput.setFixedWidth(500)
        layout.addWidget(self.projectNameInput, alignment=Qt.AlignCenter)

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
                return  # Do nothing, keep the existing file
        
        # Open file dialog to select a new ZIP file
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select ZIP File", "",
                                                  "ZIP Files (*.zip)", options=options)
        
        if fileName:
            self.selectedZipFile = fileName  # Update the selected file
            self.uploadResumesButton.setText("File Selected!")  # Update button text

    def saveProject(self):
        # Placeholder for save project logic
        QMessageBox.information(self, "Project Saved", "Your project has been saved successfully.")

    def goBack(self):
        if self.parent():
            self.parent().setGeometry(self.geometry()) 
            self.parent().show()
        self.close()

