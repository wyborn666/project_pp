import sys, sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import uic
from UserInterface import UserInterfaceClass
from MenuAdmin import MyWidget


class EnterMenu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.register_window = None
        self.enter_interface_name = "EnterMenu Interface.ui"
        self.users_table_name = "Users_Admins.bd"
        self.indicator_reg = None
        self.conn = sqlite3.connect(self.users_table_name)
        self.curs = self.conn.cursor()

        self.labelChange()

        self.enter_pushButton.clicked.connect(self.clickedEnterBut)
        self.label.linkActivated.connect(self.clickedRegistrationBut)
    

    def labelChange(self):

        uic.loadUi(self.enter_interface_name, self)
        self.label_id = QLabel("KEY FOOD", self)
        self.label_id.setGeometry(80, 0, 300, 100)

        self.label_id_2 = QLabel("ID", self)
        self.label_id_2.setGeometry(232, -1, 300, 100)
        self.label_id_2.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 25px;
            }
        """)

        font_path = "Sonic Logo Bold RUS by vania5617sonfan.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 16)
        self.label_id.setFont(font)
        self.label_id.setStyleSheet("color: red;")

        self.label = self.findChild(QLabel, 'label')

        self.label.setText('<a style="color: #0864C5;" href="#">Зарегистрироваться</a>')
        self.label.setTextFormat(Qt.RichText)
        self.label.setOpenExternalLinks(False)

        self.label.setStyleSheet("""
            QLabel {
                font-size: 18px;
            }
        """)
        self.label.setGeometry(200, 257, 300, 50)

        self.enter_pushButton.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 16;
                border-radius: 12;
            }
        """)
        self.password_lineEdit.setStyleSheet("""
            QLineEdit {
                border-radius: 5;
                border: 2px solid gray;
            }
        """)
        self.login_lineEdit.setStyleSheet("""
            QLineEdit {
                border-radius: 5;
                border: 2px solid gray;
            }
        """)


    def messageWrongAnswer(self, name = "Предупреждение", text = "Неверный пароль или логин"):
        message = QMessageBox.information(self, f'{name}', f'{text}')


    def clickedEnterBut(self):

        current_login = self.login_lineEdit.text()
        current_password = self.password_lineEdit.text()

        if len(current_login) != 0 and len(current_password) != 0:
            
            try:
                password = list(*self.curs.execute(f"""SELECT password FROM 'Logins and passwords' 
                                                        WHERE (login = '{current_login}')"""))[0]
                author_status = list(*self.curs.execute(f"""SELECT status FROM 'Logins and passwords'
                                                        WHERE (login = '{current_login}')"""))[0]
            except Exception:
                password = None

            if current_password == password:
                try:
                    self.main_window = UserInterfaceClass(self) if author_status == 2 else MyWidget('test.db')
                    self.main_window.show()
                except Exception:
                    self.messageWrongAnswer()

            else: 
                self.messageWrongAnswer()

        else:
            self.messageWrongAnswer("Предупреждение", "Введите логин и пароль")


    def clickedRegistrationBut(self):

        if self.indicator_reg is None:
            self.indicator_reg = RegistrationWindow(self)
            self.indicator_reg.show()

        else:
            self.indicator_reg = None


class RegistrationWindow(QMainWindow):


    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent

        uic.loadUi(self.parent.enter_interface_name, self)
        self.label.setText("Регистрация")
        self.label.setGeometry(25, 0, 300, 100)

        self.enter_pushButton.setText("Зарегистрироваться")
        self.enter_pushButton.setGeometry(80, 270, 180, 28)
        self.enter_pushButton.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 16;
                border-radius: 12;
            }
        """)
        self.password_lineEdit.setStyleSheet("""
            QLineEdit {
                border-radius: 5;
                border: 2px solid gray;
            }
        """)
        self.login_lineEdit.setStyleSheet("""
            QLineEdit {
                border-radius: 5;
                border: 2px solid gray;
            }
        """)

        self.enter_pushButton.clicked.connect(self.clickedRegistrateBut)
        

    def clickedRegistrateBut(self):
        
        conn = sqlite3.connect(str(self.parent.users_table_name))
        curs = conn.cursor()

        current_login = self.login_lineEdit.text()
        current_password = self.password_lineEdit.text()


        login_for_check = curs.execute(f"""SELECT login FROM 'Logins and Passwords' WHERE login = '{current_login}'""")

        for i in login_for_check:
            login_for_check = i[0]

        if isinstance(login_for_check, str):
            message = self.parent.messageWrongAnswer("Предупреждение", "Пользователь с таким логином уже существует")

        else:
            
            if len(current_password) != 0:
                
                curs.execute(f"""INSERT INTO 'Logins and passwords'(login, password, status) 
                                VALUES ('{current_login}', '{current_password}', '2')""")
                conn.commit()
                
                message = self.parent.messageWrongAnswer("Регистрация завершена", "Вы успешно зарегистрировались")
                self.close()

            else:
                message = self.parent.messageWrongAnswer("Предупреждение", "Введите пароль")
        
    
class MyWindow(QMainWindow):

    def closeEvent(self, event):
        event.accept()


app = QApplication(sys.argv)
ex = EnterMenu()
window = MyWindow()
window.setCentralWidget(ex)
window.show()
sys.exit(app.exec_())