from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

class ClickableLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set focus policy to StrongFocus to accept focus by tabbing
        self.setFocusPolicy(Qt.StrongFocus)

    def mousePressEvent(self, event):
        # Call the parent class's mousePressEvent
        super().mousePressEvent(event)
        # Optionally, you can set focus explicitly, but it's not necessary if the focus policy is set correctly
        self.setFocus()
