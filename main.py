from PyQt5 import QtWidgets
from audit_parser import AuditParser
import os
import typing
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QLine, QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audit Parser")
        self.setFixedWidth(800)
        self.setFixedHeight(500)

        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self.file_content = QLabel("Welcome!")
        self.file_content.setWordWrap(True)
        self.file_content.setStyleSheet("padding: 10px")
        self.file_content.setFixedWidth(750)
        self.file_content.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.file_content.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.file_content)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


        self.layout.addWidget(self.scrollArea)

        self.mainWidget = QWidget(self)
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)


        open_file_btn = QAction(QIcon("bug.png"), "Open file", self)
        open_file_btn.setStatusTip("Open File")
        open_file_btn.triggered.connect(self.on_open_file_btn_clicked)

        convert_file_btn = QAction(QIcon("bug.png"), "Parse audit file", self)
        convert_file_btn.setStatusTip("Parse audit file")
        convert_file_btn.triggered.connect(self.on_parse_audit_clicked)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(open_file_btn)
        file_menu.addSeparator()
        file_menu.addAction(convert_file_btn)


    def on_parse_audit_clicked(self, s):
        dlg = CustomDialog(self)
        if dlg.exec():
            print("Success")
        else:
            print("Cancel")


    # TODO: restrict file type
    def on_open_file_btn_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")
        
        if not path:
            return

        try:
            with open(path, 'r') as file:
                content = file.read()

            self.file_content.setText(content)
            self.file_content.setFixedWidth(750)
         #   self.file_content.setStyleSheet("background-color:red")

            self.file_content.adjustSize()
            
            print(content)
        except Exception as e:
            dlg = QMessageBox(self)
            dlg.setText(str(e))
            dlg.setIcon(QMessageBox.Critical)
            dlg.show()


class CustomDialog(QDialog):
    def __init__(self, parent: typing.Optional[QWidget]) -> None:
        super().__init__(parent=parent)

        self.setWindowTitle("Select file")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

     #   self.accepted.connect(self.save_file)
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()

        select_file_btn = QPushButton("Select File")
        self.select_file_le = QLineEdit()

        save_name_label = QLabel("Save name:")
        self.save_name_le = QLineEdit()

        select_file_btn.clicked.connect(self.on_select_file_button_clicked)

        self.layout.addWidget(select_file_btn, 0, 0)
        self.layout.addWidget(self.select_file_le, 0, 1, 1, 2)

        self.layout.addWidget(save_name_label, 1, 0, Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.save_name_le, 1, 1, 1, 2)

        self.layout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.layout.setHorizontalSpacing(10)
        self.layout.setVerticalSpacing(10)
        
        self.setLayout(self.layout)

    def on_select_file_button_clicked(self):
            path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")
            head, tail = os.path.split(path)
            filename = tail.split('.')[0]
            
            self.path = path
            self.select_file_le.setText(path)
            self.save_name_le.setText(filename + '.json')


    def accept(self):
        input_file_path = self.path
        save_path = self.save_name_le.text()

        try:
            with open(input_file_path, 'r') as file:
                content = file.read()

            parser = AuditParser()
            parsed_content = parser.parse(content)

            with open(save_path, 'w') as file:
                file.write(parsed_content)

            super().accept()
        except Exception as e:
            dlg = QMessageBox(self)
            dlg.setText(str(e))
            dlg.setIcon(QMessageBox.Critical)
            dlg.show()

        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()