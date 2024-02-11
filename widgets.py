from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

class ClickableLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)

    def mousePressEvent(self, event):
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        super().mousePressEvent(event)
