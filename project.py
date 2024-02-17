class Project:
    def __init__(self, name, category, job_title, location, description, skills, education, experience, path):
        self.name = name
        self.category = category
        self.job_title = job_title
        self.location = location
        self.description = description
        self.skills = skills
        self.education = education
        self.experience = experience
        self.projectPath = path

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "job_title": self.job_title,
            "location": self.location,
            "description": self.description,
            "skills": self.skills,
            "education": self.education,
            "experience": self.experience,
            "projectURL": self.projectPath
        }
