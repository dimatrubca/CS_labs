from PyQt5 import QtWidgets
from PyQt5.QtCore import QLine, QSize, Qt

class FileViewer(QtWidgets.QWidget):
    def __init__(self, fpath):
        super(FileViewer, self).__init__()

        self.widget = QtWidgets.QLabel("")

        with open(fpath, 'r') as f:
            content = f.read()

        self.widget = QtWidgets.QLabel(content)
        self.widget.setWordWrap(True)
        self.widget.setStyleSheet("padding: 10px")
        self.widget.setFixedWidth(350)
        self.widget.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.widget.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        