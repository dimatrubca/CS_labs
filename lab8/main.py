import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import PyQt5

from database.models import User
from utils import send_email

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.current_user = None

        register_page = self.create_register_page()
        self.setCentralWidget(register_page)






    def create_register_page(self):
        register_page_layout = QtWidgets.QVBoxLayout()

        login_label = QtWidgets.QLabel("Login:")
        email_label = QtWidgets.QLabel("Email")
        password_label = QtWidgets.QLabel("Password:")

        login_le = QtWidgets.QLineEdit()
        email_le = QtWidgets.QLineEdit()
        password_le = QtWidgets.QLineEdit()
        password_le.setEchoMode(QtWidgets.QLineEdit.Password)

        register_btn = QtWidgets.QPushButton("Register")
        register_btn.clicked.connect(lambda: self.on_register_pressed(login_le.text(), email_le.text(), password_le.text()))

        register_page_layout.addWidget(login_label)
        register_page_layout.addWidget(login_le)
        register_page_layout.addWidget(email_label)
        register_page_layout.addWidget(email_le)
        register_page_layout.addWidget(password_label)
        register_page_layout.addWidget(password_le)
        register_page_layout.addWidget(register_btn)


        register_page_widget = QtWidgets.QWidget()
        register_page_widget.setLayout(register_page_layout)

        return register_page_widget


    def on_register_pressed(self, login, email, password):
        self.current_user = User(login, email, password)
        self.current_user.confirmation_code = send_email(email)

        user_page = self.create_user_page()
        self.setCentralWidget(user_page)


    def create_user_page(self):
        layout = QtWidgets.QVBoxLayout()
        
        login_label = QtWidgets.QLabel("Welcome " + self.current_user.login + "!")
        email_label = QtWidgets.QLabel("Email: " + self.current_user.email)

        layout.addWidget(login_label)
        layout.addWidget(email_label)

        if self.current_user.is_confirmed:
            message = "Congrats! You passed the verification process."

            layout.addWidget(QtWidgets.QLabel(message))
        else:
            message = "An confirmation code has  been sent to your email"
            code_le = QtWidgets.QLineEdit()
            hint_label = QtWidgets.QLabel("")
            confirm_btn = QtWidgets.QPushButton("Confirm")

            confirm_btn.clicked.connect(lambda: self.on_confirmed_pressed(code_le, hint_label))

            hint_label.setVisible(False)

            layout.addWidget(QtWidgets.QLabel(message))
            layout.addWidget(QtWidgets.QLabel("Code :"))
            layout.addWidget(code_le)
            layout.addWidget(hint_label)
            layout.addWidget(confirm_btn)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        return widget


    def on_confirmed_pressed(self, code_le, hint_label: QtWidgets.QLabel):
        code = code_le.text()

        print(code, self.current_user.confirmation_code)
        print(code == self.current_user.confirmation_code)

        if code != self.current_user.confirmation_code:
            hint_label.setVisible(True)
            hint_label.setText("Invalid code!")
            hint_label.setStyleSheet('color: red')
        else:
            hint_label.setVisible(False)
            self.current_user.is_confirmed = True
           # self.centralWidget().update()
            user_page = self.create_user_page()
            self.setCentralWidget(user_page)

    def __next_page(self):
        idx = self.stacked_widget.currentIndex()
        if idx < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(idx + 1)
        else:
            self.stacked_widget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())