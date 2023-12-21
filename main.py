import sys
import pymongo
from PyQt5 import QtGui, QtCore, QtWidgets
from start_window import Ui_MainWindow as start_window_class
from login_window import Ui_MainWindow as login_window_class
from regis_window import Ui_MainWindow as regis_window_class
from PyQt5.QtGui import QPixmap
from arg import *


class StartWindow(QtWidgets.QMainWindow, start_window_class):
    def __init__(self, parent=None):
        super(StartWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openLoginWindow)
        self.pushButton_2.clicked.connect(self.openRegisWindow)
        self.pushButton_3.clicked.connect(self.openCloseWindow)

    def openLoginWindow(self):
        self.LogWindow = LoginWindow(self)
        self.LogWindow.show()

    def openRegisWindow(self):
        self.ResWindow = RegisWindow(self)
        self.ResWindow.show()

    def openCloseWindow(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText("Закрытие программы")
        msg_box.setInformativeText("Вы уверены, что хотите выйти?")

        # Загрузка и установка картинки
        image = QPixmap("C:/projects/My_window/close_cat.jpg")
        msg_box.setIconPixmap(image.scaled(300, 300)) 
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # Проверка выбора пользователя
        choice = msg_box.exec_()
        if choice == QtWidgets.QMessageBox.Yes:
            self.close()


class LoginWindow(QtWidgets.QMainWindow, login_window_class):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)

        self.authorization_status = False
        self.client = pymongo.MongoClient(MongoLink)
    
        self.pushButton.clicked.connect(self.login)

    def check_data(self):
        login = self.lineEdit.text()
        passw = self.lineEdit_2.text()

        if login and passw:
            search_login = self.client.testdb.users.find_one({"nickname": login})
            if search_login:
                return "value_exists"
            else:
                return "value_not_found"
        else:
            return "no_data_available"

    def login(self):
        if self.authorization_status is False:
            result = self.check_data()

            if result == "value_exists":
                login = self.lineEdit.text()
                passw = self.lineEdit_2.text()
                user_document = self.client.testdb.users.find_one({"nickname": login})

                if user_document and passw == user_document["password"]:
                    message = "Успешная авторизация!"
                    QtWidgets.QMessageBox.about(self, "Уведомление", message)
                    self.authorization_status = True
                else:
                    message = "Данные введены не коректно!"
                    QtWidgets.QMessageBox.about(self, "Ошибка", message)

            elif result == "value_not_found":
                message = "Такой пользователь не зарегистрирован!"
                QtWidgets.QMessageBox.about(self, "Уведомление", message)

            elif result == "no_data_available":
                message = "Необходимо ввести данные!"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)
        
        else:
            message = "Вы уже авторизованы"
            QtWidgets.QMessageBox.about(self, "Ошибка", message)



class RegisWindow(QtWidgets.QMainWindow, regis_window_class):
    def __init__(self, parent=None):
        super(RegisWindow, self).__init__(parent)
        self.setupUi(self)
        self.authorization_status = False
        self.client = pymongo.MongoClient(MongoLink)
    
        self.pushButton.clicked.connect(self.register)

    def check_data(self):
        name = self.lineEdit.text()
        login = self.lineEdit_2.text()
        passw = self.lineEdit_3.text()

        if name and login and passw:
            search_login = self.client.testdb.users.find_one({"nickname": login})
            if search_login:
                return "value_exists"
            else:
                return "value_not_found"
        else:
            return "no_data_available"

    def register(self):
        if self.authorization_status is False:
            result = self.check_data()

            if result == "value_exists":
                message = "Такой логин уже существует!"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)

            elif result == "value_not_found":
                data = {
                    "name": self.lineEdit.text(),
                    "nickname": self.lineEdit_2.text(),
                    "password": self.lineEdit_3.text()
                }
                self.client.testdb.users.insert_one(data)
                message = "Поздравляю! Вы зарегистрированы!"
                QtWidgets.QMessageBox.about(self, "Уведомление", message)
                self.authorization_status = True

            elif result == "no_data_available":
                message = "Необходимо ввести данные!"
                QtWidgets.QMessageBox.about(self, "Ошибка", message)
        else:
            message = "Вы уже авторизованы!"
            QtWidgets.QMessageBox.about(self, "Ошибка", message)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())