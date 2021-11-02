# GUI viewer to view JSON data as tree in PyQT.

# Std
import argparse
import collections
import json
import sys
from typing import OrderedDict

# External
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QLine, QSize, Qt
import subprocess
import re

class TextToTreeItem:
    def __init__(self):
        self.text_list = []
        self.titem_list = []

    def append(self, text_list, titem):
        for text in text_list:
            self.text_list.append(text)
            self.titem_list.append(titem)

    # Return model indices that match string
    def find(self, find_str):

        titem_list = []
        for i, s in enumerate(self.text_list):
            if find_str in s:
                self.titem_list[i].setHidden(True)
                titem_list.append(self.titem_list[i])

        return titem_list



class JsonView(QtWidgets.QWidget):

    def __init__(self, fpath):
        super(JsonView, self).__init__()

        self.find_box = None
        self.tree_widget = None
        self.text_to_titem = TextToTreeItem()
        self.found_titem_list = []
        self.found_idx = 0

        jfile = open(fpath)
        jdata = json.load(jfile, object_pairs_hook=collections.OrderedDict)


        # from pprint import pprint
        # pprint(jdata)
        # print(type(jdata))

        # Find UI

        find_layout = self.make_find_ui()

        # Tree

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabels(["Key", "Value"])
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tree_widget.header().setStretchLastSection(True)
        self.tree_widget.horizontalScrollBar().setEnabled(True)
        self.tree_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tree_widget.setColumnWidth(0, 3000)
        self.tree_widget.resizeColumnToContents(0)
        
        self.tree_widget.header().setStretchLastSection(False)
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        root_item = QtWidgets.QTreeWidgetItem(["Root"])
        self.recurse_jdata(jdata, root_item)
        self.tree_widget.addTopLevelItem(root_item)

        # Add table to layout

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tree_widget)

        # Group box

        gbox = QtWidgets.QGroupBox(fpath)
        gbox.setLayout(layout)

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addLayout(find_layout)
        layout2.addWidget(gbox)

        self.setLayout(layout2)

        self.find_checked()

    def make_find_ui(self):

        # Text box
        self.find_box = QtWidgets.QLineEdit()
        self.find_box.returnPressed.connect(self.find_button_clicked)

        # Find Button
        find_button = QtWidgets.QPushButton("Find")
        find_button.clicked.connect(self.find_button_clicked)

        # Select_all 
        select_all_button = QtWidgets.QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all_button_clicked)

        deselect_all_button = QtWidgets.QPushButton("Deselect All")
        deselect_all_button.clicked.connect(self.deselect_all_button_clicked)

        audit_button = QtWidgets.QPushButton("Audit")
        audit_button.clicked.connect(self.audit_workstation)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.find_box)
        layout.addWidget(find_button)
        layout.addWidget(select_all_button)
        layout.addWidget(deselect_all_button)
        layout.addWidget(audit_button)

        return layout

    def find_button_clicked(self):

        find_str = self.find_box.text()
        self.find(find_str)


    def select_all_button_clicked(self):
        self.set_check_state_all(Qt.CheckState.Checked)


    def deselect_all_button_clicked(self):
        self.set_check_state_all(Qt.CheckState.Unchecked)


    def set_check_state_all(self, state):
        root = self.tree_widget.invisibleRootItem().child(0)
        items_count = root.childCount()

        for i in range(items_count):
            option_item = root.child(i)
            option_item.setCheckState(0, state)


    def recurse_jdata(self, jdata, tree_widget):

        if isinstance(jdata, dict):
            for key, val in jdata.items():
                self.tree_add_row(key, val, tree_widget)
        elif isinstance(jdata, list):
            for i, val in enumerate(jdata):
                key = str(i)
                self.tree_add_row(key, val, tree_widget)
        else:
            print("This should never be reached!")

    def tree_add_row(self, key, val, tree_widget):

        text_list = []

        if isinstance(val, dict) or isinstance(val, list):
            text_list.append(key)
            row_item = QtWidgets.QTreeWidgetItem([key])
            row_item.setCheckState(0,Qt.CheckState.Checked)
            self.recurse_jdata(val, row_item)
        else:
            text_list.append(key)
            text_list.append(str(val) )
            row_item = QtWidgets.QTreeWidgetItem([key, str(val)])

       # row_item.setBackground(0, QtGui.QColor('red'))

        tree_widget.addChild(row_item)
        self.text_to_titem.append(text_list, row_item)


    def find_checked(self):
        checked_options = []
        root = self.tree_widget.invisibleRootItem().child(0)
        items_count = root.childCount()
        

        for i in range(items_count):
            option = OrderedDict()
            option_item = root.child(i)
            #print(option_item.text(0))

            if option_item.checkState(0) == Qt.CheckState.Checked:
                for j in range(option_item.childCount()):
                    child = option_item.child(j)

                   # print(child.text(0), child.text(1))
                    option[child.text(0)] = child.text(1)

                checked_options.append(option)

        return checked_options


    def find(self, find_str):
        root = self.tree_widget.invisibleRootItem().child(0)
        items_count = root.childCount()

        for i in range(items_count):
            option_item = root.child(i)
            option_item.setHidden(True)

            for j in range(option_item.childCount()):
                child = option_item.child(j)
                key, val = child.text(0), child.text(1)

                if find_str in key or find_str in val or find_str == "":
                    option_item.setHidden(False)
                    child.setSelected(True)
                else:
                    child.setSelected(False)


    def audit_workstation(self):
        root = self.tree_widget.invisibleRootItem().child(0)
        items_count = root.childCount()
        

        for i in range(items_count):
            option = OrderedDict()
            option_item = root.child(i)
            #print(option_item.text(0))

            if option_item.checkState(0) == Qt.CheckState.Checked:
                for j in range(option_item.childCount()):
                    child = option_item.child(j)

                   # print(child.text(0), child.text(1))
                    option[child.text(0)] = child.text(1)

            if "cmd" not in option:
                continue

            try:

                import ast
                command = option['cmd'][1:-1]
                expect = ast.literal_eval(f"""\"{option['expect'][1:-1]}\"""")


                output = subprocess.getoutput("sudo " + command)
                regexp = re.compile(f"{expect}", re.MULTILINE)

                if regexp.search(output):
                    option_item.setBackground(0, QtGui.QColor('green'))
                    option_item.setText(0, option_item.text(0) + " (Passed)")
                else:
                    option_item.setBackground(0, QtGui.QColor('red'))
            except Exception as e:
                print(e)




class JsonViewer(QtWidgets.QMainWindow):

    def __init__(self, fpath):
        super(JsonViewer, self).__init__()

        json_view = JsonView(fpath)

        self.setCentralWidget(json_view)
        self.setWindowTitle("JSON Viewer")
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


def main():
    qt_app = QtWidgets.QApplication(sys.argv)
    json_viewer = JsonViewer()
    sys.exit(qt_app.exec_())


if "__main__" == __name__:
    main()
