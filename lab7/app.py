import collections
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox, QLabel, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
from database import users_collection
from encryption import decrypt


class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        self.table_widget = TableView(4, 2)
        label = QLabel("Decrypt: ")
        self.decrypt_checkbox = QCheckBox()
        self.decrypt_checkbox.stateChanged.connect(self.on_decrypt_pressed)

        layout.addWidget(self.table_widget)
        layout.addWidget(label)
        layout.addWidget(self.decrypt_checkbox)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.resize(900, 400)


    
    def on_decrypt_pressed(self, int):
        if self.decrypt_checkbox.isChecked():
            self.table_widget.show_decrypted()
        else:
            self.table_widget.show_encrypted()
 
 
class TableView(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.__setData()
        self.setColumnWidth(0, 240)
        self.setColumnWidth(1, 600)
        self.resize(500, 200)

 
    def __setData(self, encrypted=True): 
        cursor = users_collection.find({})

        self.data =  {
            'username': [],
            'secret_key': []
        }

        for doc in cursor:
            username = doc['username']
            secret_key = doc['secret_key'] if encrypted else decrypt(doc['secret_key'])
            secret_key = secret_key.decode('utf-8')

            self.data['username'].append(username)
            self.data['secret_key'].append(secret_key)
            #print(doc)

        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys(), reverse=True)):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(str(item))
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)


    def show_decrypted(self):
        self.__setData(False)


    def show_encrypted(self):
        self.__setData(True)
 
 
def main(args):
    app = QApplication(args)
    main_window = AppWindow()
    main_window.show()
    sys.exit(app.exec_())
 
if __name__=="__main__":
    main(sys.argv)