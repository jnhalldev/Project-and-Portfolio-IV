import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ResuHunter")
        self.setWindowIcon(QIcon("images/resu_hunter_icon.png"))
        self.setGeometry(1200,300,500,500)
        self.show()

def main():
    app = QApplication(sys.argv)
    main_Window = MainWindow()
    main_Window.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass  # Suppress the SystemExit exception

if __name__ == "__main__":
    main()