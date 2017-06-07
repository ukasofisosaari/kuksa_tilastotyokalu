
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QTextEdit, QWidget
class HelloWorld(QWidget):
    def __init__(self, parent=None):
        super(HelloWorld, self).__init__(parent)

        nameLabel = QLabel("Hello World")


        mainLayout = QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Address Book")